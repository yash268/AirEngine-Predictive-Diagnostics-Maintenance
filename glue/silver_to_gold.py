from awsglue.context import GlueContext
from pyspark.context import SparkContext
from pyspark.sql.functions import avg
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

bucket = "********"
silver = f"s3://{bucket}/silver/"

df = spark.read.parquet(silver)
agg = df.groupBy("engine_id").agg(
    avg("vibration").alias("avg_vibration"),
    avg("egt").alias("avg_egt"),
    avg("fuel_flow").alias("avg_fuel_flow"),
    avg("n1_rpm").alias("avg_n1"),
    avg("n2_rpm").alias("avg_n2")
)
agg.write.mode("overwrite").parquet(f"s3://{bucket}/gold/features/")
