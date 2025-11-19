#!/usr/bin/env python3
"""Telemetry simulator: publishes synthetic engine telemetry to Kinesis Stream."""
import json, time, random, uuid, argparse
from datetime import datetime, timezone
import boto3
import numpy as np

np.random.seed(42)
random.seed(42)

parser = argparse.ArgumentParser()
parser.add_argument("--stream", required=True, help="Kinesis stream name")
parser.add_argument("--rate", type=float, default=50, help="events per second")
parser.add_argument("--duration", type=int, default=600, help="seconds to run")
parser.add_argument("--anomaly-rate", type=float, default=0.02, help="fraction of events to inject anomaly")
args = parser.parse_args()

kinesis = boto3.client("kinesis")
engines = ["ENG001","ENG002","ENG003","ENG004"]

def generate_event(engine_id):
    return {
        "event_id": str(uuid.uuid4()),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "engine_id": engine_id,
        "n1_rpm": round(np.random.normal(9500, 300),2),
        "n2_rpm": round(np.random.normal(14500, 400),2),
        "egt": round(np.random.normal(650, 25),2),
        "fuel_flow": round(np.random.normal(1200, 80),2),
        "vibration": round(abs(np.random.normal(3.5, 0.7)),2),
        "oil_pressure": round(np.random.normal(45, 5),2),
        "altitude": round(np.random.normal(30000, 1500),2),
        "speed": round(np.random.normal(480,20),2),
        "flight_phase": random.choice(["taxi","takeoff","climb","cruise","descent","landing"])
    }

interval = 1.0 / args.rate
end = time.time() + args.duration
print(f"Streaming to {args.stream} @ {args.rate} eps for {args.duration}s")
while time.time() < end:
    eng = random.choice(engines)
    ev = generate_event(eng)
    if random.random() < args.anomaly_rate:
        ev["vibration"] = round(ev["vibration"] * random.uniform(2.5,5.0),2)
        ev["anomaly"] = True
    kinesis.put_record(StreamName=args.stream, Data=json.dumps(ev), PartitionKey=ev["engine_id"])
    time.sleep(interval)
