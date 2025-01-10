import argparse
import pyarrow.parquet as pq
import pandas as pd
from sqlalchemy import create_engine
from time import time 
import os 

def main(params):
  user = params.user
  password = params.password
  host = params.host 
  port = params.port 
  db = params.db 
  url = params.url
  table_name = params.table_name 

  parquet_name = 'output.parquet'

  os.system(f"wget {url} -O {parquet_name}")

  engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
  engine.connect()

  parquet_file = pq.ParquetFile(f'{parquet_name}')
  for batch in parquet_file.iter_batches():
      t_start = time()
      batch_df = batch.to_pandas()
      batch_df.to_sql(name=f'{table_name}', 
                      con=engine, if_exists='append')
      t_end=time()
      print(f"inserted another batch..., took {t_end - t_start:.2f} seconds")

      break # just take a small chunk of the database due to storage size 


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description="Ingest CSV data to Postgres")

  # user, password, host, port, database name, table name, url of the csv
  parser.add_argument('--user', help='username for Postgres')
  parser.add_argument('--password', help='password for Postgres')
  parser.add_argument('--host', help='host for Postgres')
  parser.add_argument('--port', help='port for Postgres')
  parser.add_argument('--db', help='database name for Postgres')
  parser.add_argument('--table_name', help='name of the table where we will write the results to')
  parser.add_argument('--url', help='url of the csv file')

  args = parser.parse_args()

  main(args)




