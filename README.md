
#  AirEngine PDM — Real-Time Aircraft Engine Alerting & Predictive Maintenance System (AWS + Terraform)

AirEngine PDM is a real-time, cloud-native data engineering & predictive maintenance platform for the aeronautical industry.  
It processes live aircraft engine telemetry, predicts failures using ML, and alerts engineering teams automatically.

This project demonstrates expertise in **AWS Data Engineering**, **Terraform IaC**, **Real-Time Analytics**, **Machine Learning**, and **Observability**.

---

##  System Architecture

![aws (8)](https://github.com/user-attachments/assets/ce891774-f18b-4b9b-9eaf-dc0eb434ab23)


---

##  Key Capabilities

###  Real-Time Engine Data Ingestion
Aircraft IoT sensors send events such as:
- Exhaust Gas Temperature (EGT)  
- Engine Pressure Ratio (EPR)  
- Fuel Flow  
- Vibration Metrics  
- Altitude, Airspeed, Outside Air Temperature  

Data is streamed into **Kinesis Data Streams**.

---

###  Data Lake & ETL
- Raw data → **Amazon S3 (Raw Zone)**  
- ETL via **AWS Glue Jobs (PySpark)**  
- Processed & cleaned data → **S3 Processed Zone**  
- Partitioned & optimized using **Parquet** for analytics  

---

###  Feature Engineering for Predictive Maintenance
- Aggregation windows  
- Derived features (temp gradients, deltas, moving averages)  
- Techniques for anomaly detection  
- ML-ready dataset stored in **S3 ML Zone**

---

###  Machine Learning Model (Failure Prediction)
- Training + tuning using **Amazon SageMaker**
- ML model deployed as a **real-time inference endpoint**
- Predicts:
  -  High engine temperature risk  
  -  Early fault signals  
  -  Maintenance needed in next X hours  

---

###  Automated Alerting Pipeline
- Model output written back to **Kinesis / S3**
- **Lambda** monitors prediction scores
- Severity > threshold → Notification sent via SNS/Slack

---

###  Monitoring & Observability (Grafana)
Dashboards show:
- Engine live telemetry  
- Prediction confidence  
- Alert frequency  
- Feature drift  
- Kinesis ingestion rate  
- Lambda errors  

---

##  Infrastructure Deployment (Terraform)

The infra is deployed using:
```
cd infra/envs/dev
terraform init
terraform plan
terraform apply
```

---

##  Sample Dataset (20,000 Records)

Dataset includes:
- timestamp  
- aircraft_id  
- engine_id  
- egt  
- vibration  
- fuel_flow  
- altitude  
- airspeed  
- maintenance_flag  

---

##  ETL (Glue PySpark)

- Cleaning  
- Transforming  
- Feature engineering  
- Parquet write  

---

##  Machine Learning Workflow (SageMaker)

- Training  
- Tuning  
- Deploying  
- Real-time inference  

---

##  Monitoring (Grafana)

- Real-time dashboards  
- Alerts visualization  
- Performance monitoring  

---

##  End-to-End Workflow Summary

1. Sensors → Kinesis  
2. Raw → S3  
3. Glue ETL  
4. ML features → S3  
5. Train + deploy model  
6. Alerts  
7. Dashboards  

---

##  Skills Demonstrated

- AWS Glue  
- Kinesis  
- Lambda  
- SageMaker  
- Terraform  
- Data Engineering  
- ML Engineering  
- Observability  

