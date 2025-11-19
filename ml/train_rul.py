import pandas as pd
import joblib
from xgboost import XGBRegressor
import boto3
import os

S3_BUCKET = "********"
FEATURE_PATH = "gold/features/"

# read parquet into pandas (small demo only)
df = pd.read_parquet(f"s3://{S3_BUCKET}/{FEATURE_PATH}")

# synthetic label if not present
if "label_rul" not in df.columns:
    df["label_rul"] = 1000 - (df.groupby("engine_id").cumcount())

X = df.drop(columns=["label_rul","engine_id"], errors='ignore')
y = df["label_rul"]

model = XGBRegressor(n_estimators=200, max_depth=6)
model.fit(X, y)

os.makedirs("/tmp/model", exist_ok=True)
joblib.dump(model, "/tmp/model/rul_model.pkl")

s3 = boto3.client("s3")
s3.upload_file("/tmp/model/rul_model.pkl", S3_BUCKET, "models/rul_model.pkl")
print("Model uploaded to s3://{}/models/rul_model.pkl".format(S3_BUCKET))
