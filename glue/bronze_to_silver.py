from awsglue.context import GlueContext
from pyspark.context import SparkContext
from pyspark.sql.functions import to_timestamp, date_format
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

bucket = "********"
raw_path = f"s3://{bucket}/raw/"

df = spark.read.json(raw_path)
df2 = df.selectExpr(
  "event_id",
  "to_timestamp(timestamp) as ts",
  "engine_id",
  "cast(n1_rpm as double) as n1_rpm",
  "cast(n2_rpm as double) as n2_rpm",
  "cast(egt as double) as egt",
  "cast(fuel_flow as double) as fuel_flow",
  "cast(vibration as double) as vibration",
  "cast(oil_pressure as double) as oil_pressure",
  "altitude",
  "speed",
  "flight_phase"
)
df2 = df2.withColumn("dt", date_format("ts","yyyy-MM-dd"))
df2.write.mode("append").partitionBy("dt").parquet(f"s3://{bucket}/silver/")
