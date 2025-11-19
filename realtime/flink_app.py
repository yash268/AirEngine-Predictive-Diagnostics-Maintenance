"""PyFlink streaming app (simplified) for Kinesis Data Analytics.

This script assumes the Flink/KDA runtime provides the Kinesis connector.
For local testing, adapt the connectors accordingly.
"""
import os, json
from datetime import datetime
from pyflink.datastream import StreamExecutionEnvironment, TimeCharacteristic
from pyflink.common.serialization import SimpleStringSchema
from pyflink.datastream.connectors import FlinkKinesisConsumer, FlinkKinesisProducer
from pyflink.common.typeinfo import Types
from pyflink.common.watermark_strategy import WatermarkStrategy
from pyflink.datastream.window import SlidingEventTimeWindows
from pyflink.common.time import Time

REGION = os.getenv('AWS_REGION', '********')
INPUT = os.getenv('INPUT_STREAM', '********')
OUTPUT = os.getenv('OUTPUT_STREAM', '********')
SAGEMAKER_ENDPOINT = os.getenv('SAGEMAKER_ENDPOINT', '********')

def safe_parse(x):
    try:
        return json.loads(x)
    except:
        return None

def compute_health_score(vib, egt, n1, oil):
    score = (vib/5.0)*30 + max(0, (egt-700)/50)*30 + max(0, (n1-11000)/1000)*20 + max(0, (oil-30)/30)*20
    return round(score,2)

def is_anomaly(vib, egt, oil):
    return vib > 6.0 or egt > 720 or oil < 25

def to_tuple(rec):
    if rec is None:
        return None
    return (
        rec.get('engine_id'),
        rec.get('timestamp'),
        float(rec.get('n1_rpm') or 0.0),
        float(rec.get('n2_rpm') or 0.0),
        float(rec.get('egt') or 0.0),
        float(rec.get('fuel_flow') or 0.0),
        float(rec.get('vibration') or 0.0),
        float(rec.get('oil_pressure') or 0.0),
    )

def main():
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_parallelism(2)
    env.set_stream_time_characteristic(TimeCharacteristic.EventTime)

    props = {'aws.region': REGION, 'flink.stream.initpos': 'LATEST'}
    consumer = FlinkKinesisConsumer(INPUT, SimpleStringSchema(), props)
    ds = env.add_source(consumer).map(lambda x: safe_parse(x), output_type=Types.MAP(Types.STRING(), Types.STRING()))

    parsed = ds.map(lambda r: to_tuple(r), output_type=Types.TUPLE([Types.STRING(), Types.STRING(), Types.FLOAT(), Types.FLOAT(), Types.FLOAT(), Types.FLOAT(), Types.FLOAT(), Types.FLOAT()]))

    # assign timestamps & watermarks - simplified (production: robust watermarking)
    wm = WatermarkStrategy.for_monotonous_timestamps().with_timestamp_assigner(lambda e, ts: int(datetime.fromisoformat(e[1].replace('Z','')).timestamp() * 1000) if e and e[1] else 0)
    parsed = parsed.assign_timestamps_and_watermarks(wm)

    keyed = parsed.key_by(lambda x: x[0])

    windowed = keyed.window(SlidingEventTimeWindows.of(Time.seconds(30), Time.seconds(10))).reduce(
        lambda a,b: (
            a[0], b[1],
            (a[2]+b[2])/2.0, (a[3]+b[3])/2.0, (a[4]+b[4])/2.0,
            (a[5]+b[5])/2.0, (a[6]+b[6])/2.0, (a[7]+b[7])/2.0
        ),
        output_type=Types.TUPLE([Types.STRING(), Types.STRING(), Types.FLOAT(), Types.FLOAT(), Types.FLOAT(), Types.FLOAT(), Types.FLOAT(), Types.FLOAT()])
    )

    def enrich(x):
        engine_id, ts, n1, n2, egt, fuel, vib, oil = x
        health = compute_health_score(vib, egt, n1, oil)
        anomal = is_anomaly(vib, egt, oil)
        out = {
            "engine_id": engine_id,
            "timestamp": ts,
            "avg_vibration": round(vib,3),
            "avg_egt": round(egt,3),
            "health_score": health,
            "anomaly": anomal
        }
        return json.dumps(out)

    enriched = windowed.map(lambda x: enrich(x), output_type=Types.STRING())

    producer = FlinkKinesisProducer(SimpleStringSchema(), {'aws.region': REGION})
    producer.set_stream(OUTPUT)
    enriched.add_sink(producer)

    env.execute("air-engine-flink")
if __name__ == '__main__':
    main()
