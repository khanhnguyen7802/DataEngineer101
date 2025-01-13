from airflow import DAG 
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator

default_args = {
  'owner': 'Khanh', 
  'retries': 5, 
  'retry_delay': timedelta(minutes=2),

}

def greet(name, age):
  print(f"Hello World! My name is {name}"
        f" and I am {age} years old.")

# ============

def greet_v2(age, ti): # task instance
  name = ti.xcom_pull(task_ids='get_name')
  print(f"Hello World! My name is {name}"
        f" and I am {age} years old.")


def get_name():   
  return 'Khanh'

# ================

def greet_v3(age, ti): # task instance
  first_name = ti.xcom_pull(task_ids='get_name_xcom', key='first_name')
  last_name = ti.xcom_pull(task_ids='get_name_xcom', key='last_name')
  print(f"Hello World! My name is {first_name} {last_name}"
        f" and I am {age} years old.")

def get_name_v2(ti): # task instance
  ti.xcom_push(key='first_name', value='Khanh')
  ti.xcom_push(key='last_name', value='Nguyen')

# ===================

def greet_v4(ti): # task instance
  first_name = ti.xcom_pull(task_ids='get_name_xcom', key='first_name')
  last_name = ti.xcom_pull(task_ids='get_name_xcom', key='last_name')
  age = ti.xcom_pull(task_ids='get_age', key='age')
  
  print(f"Hello World! My name is {first_name} {last_name}"
        f" and I am {age} years old.")

def get_age(ti):
  ti.xcom_push(key='age', value=20)

# =================

with DAG(
  dag_id='dag_with_py_v5',
  default_args=default_args,
  description='Another DAG with Python operator',
  start_date=datetime(2025, 1, 10, 14, 12),
  schedule_interval='@daily', 
) as dag: # an instance of DAG
  task1=PythonOperator(
    task_id='greet',
    python_callable=greet, 
    op_kwargs={'name':'Khanh', 'age':20}
  )
  
  task2_1=PythonOperator(
    task_id='greet_v2',
    python_callable=greet_v2, 
    op_kwargs={'age':20}
  )

  task2_2=PythonOperator(
    task_id='get_name',
    python_callable=get_name, 

  )

  task3_1=PythonOperator(
    task_id='greet_v3',
    python_callable=greet_v3, 
    op_kwargs={'age':20}
  )

  task3_2=PythonOperator(
    task_id='get_name_xcom',
    python_callable=get_name_v2, 
  )

  task4_1=PythonOperator(
    task_id='greet_v4',
    python_callable=greet_v4
  )

  task4_2=PythonOperator(
    task_id='get_age',
    python_callable=get_age
  )

  
  task1 
  task2_2 >> task2_1
  task3_2 >> task3_1
  [task3_2, task4_2] >> task4_1
