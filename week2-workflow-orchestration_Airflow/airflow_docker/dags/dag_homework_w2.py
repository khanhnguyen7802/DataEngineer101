import os
from datetime import timedelta, datetime

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from google.cloud import storage
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateExternalTableOperator, BigQueryCreateEmptyDatasetOperator

PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
BUCKET_NAME = os.environ.get("GCP_GCS_BUCKET")


# DATASET_URL = https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/
# DATASET_FILE = "green_tripdata_2021-01.csv.gz"
# MONTH = [01, 02, 03, 04, 05, 06, 07]
# the downloaded file will be in this format: green_tripdata_2021-{MONTH}.csv.gz

GCS_PATH = f"homework" # data will be stored in this destination on GCP
LOCAL_PATH = "/opt/airflow" # local path of airflow
BIGQUERY_DATASET = 'green_trips_data'


# NOTE: takes 20 mins, at an upload speed of 800kbps. Faster if your internet has a better upload speed
def upload_to_gcs(bucket_name, object_path, local_path):
    """
    Ref: https://cloud.google.com/storage/docs/uploading-objects#storage-upload-object-python
    :param bucket: GCS bucket name (where the file will be uploaded)
    :param object_path: target path (in the GCP bucket)
    :param local_path: source path
    :return:
    """
    # WORKAROUND to prevent timeout for files > 6 MB on 800 kbps upload speed.
    # (Ref: https://github.com/googleapis/python-storage/issues/74)
    storage.blob._MAX_MULTIPART_SIZE = 5 * 1024 * 1024  # 5 MB
    storage.blob._DEFAULT_CHUNKSIZE = 5 * 1024 * 1024  # 5 MB
    # End of Workaround

    filenames = [f for f in os.listdir(f"{LOCAL_PATH}/dataset") if f.endswith(".csv")]


    # upload to Google Cloud Storage
    client = storage.Client()
    bucket = client.bucket(bucket_name)

    for filename in filenames:
        blob = bucket.blob(f"{object_path}/{filename}")
        blob.upload_from_filename(f"{local_path}/{filename}")
        print(f"Data uploaded to gs://{bucket_name}/{GCS_PATH}/{filename}")

default_args = {
  'owner': 'Khanh', 
  'retries': 2, 
  'retry_delay': timedelta(minutes=1),

}

# NOTE: DAG declaration - using a Context Manager (an implicit way)
with DAG(
    dag_id="homework-w2",
    schedule_interval="@daily",
    default_args=default_args,
    start_date=datetime(2025, 2, 5, 5, 45),
    catchup=False,
    max_active_runs=1
) as dag:


    download_and_unzip_dataset_task = BashOperator(
        task_id="download_dataset_task",
        bash_command="/opt/airflow/dags/download_unzip.sh $airflow_path",
        env={"airflow_path": LOCAL_PATH}
    )


    # TODO: Homework - research and try XCOM to communicate output values between 2 tasks/operators
    local_to_gcs_task = PythonOperator(
        task_id="local_to_gcs_task",
        python_callable=upload_to_gcs,
        op_kwargs={
            "bucket_name": BUCKET_NAME,
            "object_path": f"{GCS_PATH}",
            "local_path": f"{LOCAL_PATH}/dataset", # place where dataset is stored locally
        },
    )

    # create_empty_dataset_task = BigQueryCreateEmptyDatasetOperator( # to create a (placeholder) dataset 
    #     task_id="create_bigquery_dataset",
    #     dataset_id= BIGQUERY_DATASET,
    #     project_id= PROJECT_ID,
    #     location="EU",  # Specify the dataset location
    # )

    # # Load data from GCS to BigQuery
    # bigquery_external_table_task = BigQueryCreateExternalTableOperator(
    #     task_id="bigquery_external_tables_task",
    #     table_resource={
    #         "tableReference": {
    #             "projectId": PROJECT_ID, # The ID of the project containing this table.
    #             "datasetId": BIGQUERY_DATASET,
    #             "tableId": "external_table", # name of the table
    #         },

    #         "externalDataConfiguration": {
    #             "sourceFormat": "PARQUET",
    #             "sourceUris": [f"gs://{BUCKET_NAME}/{GCS_PATH}"],
    #         },
    #     },
    # )

    # Task dependencies
    (
        download_and_unzip_dataset_task 
        >> local_to_gcs_task 
        # >> create_empty_dataset_task
        # >> bigquery_external_table_task
    )