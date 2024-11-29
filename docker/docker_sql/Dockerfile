# base image
FROM python:3.9.1 

# execute commands
RUN apt-get install wget
RUN pip install pyarrow pandas sqlalchemy psycopg2

# working directory
WORKDIR /app

# copy file from src to dst
COPY ingest_data.py ingest_data.py

# 
ENTRYPOINT ["python", "ingest_data.py"]

