import os
import logging
from datetime import timedelta, datetime

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from google.cloud import storage
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateExternalTableOperator, BigQueryCreateEmptyDatasetOperator
import pyarrow.parquet as pq

PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
BUCKET_NAME = os.environ.get("GCP_GCS_BUCKET")

DATASET_FILE = "yellow_tripdata_2024-01.parquet"
DATASET_URL = f"https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet" # link to download the dataset 

GCS_PATH = f"raw/{DATASET_FILE}" # data will be stored in this destination on GCP
LOCAL_PATH = "/opt/airflow/" # local path of 
BIGQUERY_DATASET = 'yellow_trips_data'



# NOTE: takes 20 mins, at an upload speed of 800kbps. Faster if your internet has a better upload speed
def upload_to_gcs(bucket_name, object_name, local_file):
    """
    Ref: https://cloud.google.com/storage/docs/uploading-objects#storage-upload-object-python
    :param bucket: GCS bucket name (where the file will be uploaded)
    :param object_name: target path & file-name (in the GCP bucket)
    :param local_file: source path & file-name
    :return:
    """
    # WORKAROUND to prevent timeout for files > 6 MB on 800 kbps upload speed.
    # (Ref: https://github.com/googleapis/python-storage/issues/74)
    storage.blob._MAX_MULTIPART_SIZE = 5 * 1024 * 1024  # 5 MB
    storage.blob._DEFAULT_CHUNKSIZE = 5 * 1024 * 1024  # 5 MB
    # End of Workaround

    # upload to Google Cloud Storage
    client = storage.Client()
    bucket = client.bucket(bucket_name)

    blob = bucket.blob(object_name)
    blob.upload_from_filename(local_file)
    print(f"Data uploaded to gs://{bucket_name}/{GCS_PATH}")

default_args = {
  'owner': 'Khanh', 
  'retries': 2, 
  'retry_delay': timedelta(minutes=1),

}

# NOTE: DAG declaration - using a Context Manager (an implicit way)
with DAG(
    dag_id="data_ingestion_gcs_dag",
    schedule_interval="@daily",
    default_args=default_args,
    start_date=datetime(2025, 1, 21, 2, 45),
    catchup=False,
    max_active_runs=1,
    tags=['dtc-de'],
) as dag:

    download_dataset_task = BashOperator(
        task_id="download_dataset_task",
        bash_command=f"curl {DATASET_URL} > {LOCAL_PATH}/{DATASET_FILE}"
    )


    # TODO: Homework - research and try XCOM to communicate output values between 2 tasks/operators
    local_to_gcs_task = PythonOperator(
        task_id="local_to_gcs_task",
        python_callable=upload_to_gcs,
        op_kwargs={
            "bucket_name": BUCKET_NAME,
            "object_name": f"{GCS_PATH}",
            "local_file": f"{LOCAL_PATH}/{DATASET_FILE}", # place where dataset is stored locally
        },
    )

    create_empty_dataset_task = BigQueryCreateEmptyDatasetOperator( # to create a (placeholder) dataset 
        task_id="create_bigquery_dataset",
        dataset_id= BIGQUERY_DATASET,
        project_id= PROJECT_ID,
        location="EU",  # Specify the dataset location
    )

    # Load data from GCS to BigQuery
    bigquery_external_table_task = BigQueryCreateExternalTableOperator(
        task_id="bigquery_external_table_task",
        table_resource={
            "tableReference": {
                "projectId": PROJECT_ID, # The ID of the project containing this table.
                "datasetId": BIGQUERY_DATASET,
                "tableId": "external_table", # name of the table
            },

            "externalDataConfiguration": {
                "sourceFormat": "PARQUET",
                "sourceUris": [f"gs://{BUCKET_NAME}/{GCS_PATH}"],
            },
        },
    )

    # Task dependencies
    (
        download_dataset_task 
        >> local_to_gcs_task 
        >> create_empty_dataset_task
        >> bigquery_external_table_task
    )