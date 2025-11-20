
#  AirEngine PDM — Real-Time Aircraft Engine Alerting & Predictive Maintenance System (AWS + Terraform)

AirEngine PDM is a real-time, cloud-native predictive maintenance and anomaly detection system built for the aeronautical industry.  
It processes high-frequency aircraft engine telemetry, detects anomalies in real time using PyFlink, builds a historical dataset using a Bronze → Silver → Gold data lakehouse, and trains predictive ML models using Amazon SageMaker.  
The system provides both real-time and ML-driven insights through Grafana dashboards.

This project demonstrates comprehensive expertise in AWS Data Engineering, Streaming Analytics, Machine Learning, Data Lakehouse Architecture, and Terraform-driven Infrastructure as Code.

---

##  System Architecture


![aws (4)](https://github.com/user-attachments/assets/eb95bc6e-f9d2-4215-b83b-381afe0c8b9d)


---

## Key Capabilities

### Real-Time Engine Data Ingestion

Aircraft engine IoT sensors publish continuous telemetry, including:

- Exhaust Gas Temperature (EGT)  
- Engine Pressure Ratio (EPR)  
- Vibration metrics  
- Fuel flow  
- Altitude and airspeed  
- Outside air temperature  

Data is ingested via MQTT into AWS IoT Core and forwarded to Amazon Kinesis Data Streams for real-time analytics.

---

## Real-Time Processing and Anomaly Detection

### PyFlink on Kinesis Data Analytics (KDA)

A PyFlink application processes the streaming telemetry from Kinesis Data Streams and performs:

- Real-time streaming ETL  
- Sliding-window aggregations  
- Outlier and anomaly detection  
- Threshold-based alerts  
- High-frequency metric computations  

The PyFlink application outputs anomaly events and processed metrics directly to Grafana for real-time visualization.

(No AWS Lambda is used. PyFlink handles the entire anomaly detection pipeline.)

---

## Data Lake Architecture (Bronze → Silver → Gold)

### Bronze — Raw Landing Zone

Kinesis Firehose delivers unprocessed engine telemetry into Amazon S3.  
This zone stores the raw JSON messages exactly as received from the aircraft.  
It ensures traceability and serves as the foundation for batch ETL and ML training.

---

### Silver — Clean and Structured Zone

AWS Glue processes the raw data into structured and cleaned Silver datasets:

- Schema normalization  
- Missing value handling  
- Standardized units  
- Data validation and filtering  
- Initial transformations  

Silver datasets are optimized for analytics and downstream feature engineering.

---

### Gold — Feature-Engineered Lakehouse

AWS Glue further processes Silver datasets into Gold, performing:

- Advanced feature engineering  
- Rolling statistics  
- Aggregated time-window metrics  
- Derived engine health indicators  
- Rate-of-change calculations  

Gold data is stored as Iceberg tables, enabling:

- ACID transactions  
- Time travel  
- Efficient ML training  
- High-performance analytics  

---

## Machine Learning Workflow (Amazon SageMaker)

### Training

SageMaker consumes the Gold Iceberg tables to train predictive models, including:

- Failure prediction  
- Remaining Useful Life (RUL) estimation  
- Engine health scoring  

The training pipeline includes:

- Feature selection  
- Hyperparameter tuning  
- Validation based on flight timelines  
- Model evaluation and metrics  

### Inference

The trained model generates predictions such as:

- Failure risk  
- Estimated time before maintenance  
- Additional anomalies not detected by PyFlink  

Model outputs are streamed into Grafana for monitoring.

---

## Monitoring and Visualization (Grafana)

Grafana dashboards consolidate all operational and analytical insights, including:

### Real-Time Metrics from PyFlink
- Temperature spikes  
- Vibration anomalies  
- Outlier detection  
- Streaming window computations  

### ML Predictions from SageMaker
- Failure probabilities  
- RUL estimates  
- Model confidence  
- Historical trends  

### System Health and Pipeline Metrics
- Kinesis stream throughput  
- Data ingestion latency  
- Glue job performance  
- S3 data growth  

Grafana provides a unified monitoring experience across the streaming, batch, and ML layers.

---

##  Infrastructure Deployment (Terraform)

All AWS resources used in this project are deployed through Terraform for reproducibility, version control, and automated environment setup.

Deployment steps:
```
cd infra/envs/dev
terraform init
terraform plan
terraform apply
```
Terraform provisions:

- AWS IoT Core  
- Kinesis Data Streams  
- Kinesis Firehose  
- Kinesis Data Analytics (PyFlink)  
- S3 Data Lake (Bronze, Silver, Gold)  
- AWS Glue jobs and Data Catalog  
- Iceberg lakehouse configuration  
- SageMaker resources  
- Grafana workspace  

---

##  Sample Dataset (20,000 Records)

The dataset used to simulate aircraft engine telemetry includes:

- timestamp  
- aircraft_id  
- engine_id  
- egt  
- epr  
- vibration  
- altitude  
- airspeed  
- fuel_flow  
- outside_air_temp  
- maintenance_flag  

This dataset is used for batch ETL, historical storage, ML feature engineering, and model training.

---

## ETL (AWS Glue — PySpark)

AWS Glue performs the batch ETL pipeline across the data lake:

### Bronze to Silver
- Data cleaning  
- Standardization  
- Schema alignment  
- Removal of corrupted records  

### Silver to Gold
- Feature engineering  
- Rolling windows  
- Aggregated flight-level metrics  
- Iceberg table creation  

Glue ensures that all downstream ML and analytics pipelines receive high-quality, structured datasets.

---

## Machine Learning (Amazon SageMaker)

The ML pipeline consists of:

- Data ingestion from Gold Iceberg tables  
- Feature scaling and encoding  
- Model training (RUL and anomaly prediction)  
- Hyperparameter optimization  
- Evaluation and performance scoring  
- Real-time inference endpoint  
- Drift monitoring  

Outputs are integrated into Grafana dashboards for operational visibility.

---

## End-to-End Workflow Summary

1. Aircraft sensors publish telemetry to AWS IoT Core  
2. IoT Core routes data to Kinesis Data Streams  
3. PyFlink on Kinesis Data Analytics performs real-time ETL and anomaly detection  
4. Kinesis Firehose delivers raw data to S3 Bronze  
5. AWS Glue transforms Bronze → Silver → Gold  
6. Iceberg tables in the Gold zone support ML training  
7. SageMaker trains RUL and failure prediction models  
8. Real-time anomalies and ML predictions flow into Grafana dashboards  

---

## Skills Demonstrated

- AWS IoT Core  
- Amazon Kinesis Streams, Firehose, and KDA (PyFlink)  
- S3 Data Lake Architecture (Bronze, Silver, Gold)  
- AWS Glue ETL (PySpark)  
- Apache Iceberg  
- Amazon SageMaker (Training and Inference)  
- Grafana Monitoring and Visualization  
- Terraform Infrastructure as Code  
- Streaming and Batch Data Engineering  
- Predictive Maintenance and Anomaly Detection  

