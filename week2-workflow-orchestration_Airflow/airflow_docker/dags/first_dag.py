from airflow import DAG 
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator

default_args = {
  'owner': 'Khanh', 
  'retries': 5, 
  'retry_delay': timedelta(minutes=2),

}

with DAG(
  dag_id='first_dag_v2',
  default_args=default_args,
  description='This is our first DAG',
  start_date=datetime(2025, 1, 10, 10, 12),
  schedule_interval='@daily', 
) as dag: # an instance of DAG
  task1=BashOperator(
    task_id='first_task',
    bash_command="echo hello world!"
  )

  task2=BashOperator(
    task_id='second_task',
    bash_command="echo hey im running after task 1"
  )

  task1.set_downstream(task2)
  # task1 >> [task2, task3, ..., taskn] # bit shift 