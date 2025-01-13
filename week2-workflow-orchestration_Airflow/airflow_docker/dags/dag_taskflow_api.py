from airflow.decorators import dag, task 
from datetime import datetime, timedelta

default_args = {
  'owner': 'Khanh', 
  'retries': 5, 
  'retry_delay': timedelta(minutes=2),

}


@dag(dag_id='dag_taskflow_api',
     default_args = default_args,
     start_date = datetime(2025, 1, 13),
     schedule_interval='@daily')

def hello_world_etl():

  @task(multiple_outputs=True)
  def get_name():
    return {
      'first_name': 'Khanh',
      'last_name': 'Nguyen'
    }
  
  @task()
  def get_age():
    return 20

  @task()
  def greet(first_name, last_name, age):
    print(f"Hello World! My name is {first_name} {last_name}"
          f" and I am {age} years old.")
    
  
  name_dict = get_name()
  age = get_age()
  greet(name_dict['first_name'], 
        name_dict['last_name'],
        age)
  


greet_dag = hello_world_etl()