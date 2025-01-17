# Instructions for homework - Week 1
## Question 1
Run docker with the `python:3.12.8` image in an interactive mode, use the entrypoint `bash`.

What's the version of `pip` in the image? 

-> **Solution:** 24.3.1
```
docker run -it python:3.12.8  bash
```
```
pip --version
```

## Question 2

Given the following `docker-compose.yaml`, what is the `hostname` and `port` that **pgadmin** should use to connect to the postgres database?

```yaml
services:
  db:                           ---> hostname
    container_name: postgres
    image: postgres:17-alpine
    environment:
      POSTGRES_USER: 'postgres'
      POSTGRES_PASSWORD: 'postgres'
      POSTGRES_DB: 'ny_taxi'
    ports:
      - '5433:5432'     ---> map to port 5432 in the container
    volumes:
      - vol-pgdata:/var/lib/postgresql/data

  pgadmin:
    container_name: pgadmin
    image: dpage/pgadmin4:latest
    environment:
      PGADMIN_DEFAULT_EMAIL: "pgadmin@pgadmin.com"
      PGADMIN_DEFAULT_PASSWORD: "pgadmin"
    ports:
      - "8080:80"
    volumes:
      - vol-pgadmin_data:/var/lib/pgadmin  
```
**Solution:** `db:5432`

## Question 3
### Set up the environment
- Step 1: Download these 2 datasets and put into this folder 
  ```
  wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-10.csv.gz
  ```

  ```bash
  wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv
  ```
- Step 2: create an empty folder to contain the data (namely `green_trip_data`). Initialize Postgres and create a new database (namely `green_trip`), run:
  ```
  docker run -it -e POSTGRES_USER="root" -e POSTGRES_PASSWORD="root" -e POSTGRES_DB="green_trip" -v \absolute\path\to\green_trip_data\folder:/var/lib/postgresql/data -p 5434:5432 postgres:13
  ```
- Step 3: ingest data from the `.csv` files (refer to [ingest_data.manually.ipynb](./ingest_data_manually.ipynb))

- Step 4 (*optionally*): use `pcli` to check whether the data is ingested properly. (*I used `conda` in CMD to run the command*).
  ```
  pgcli -h localhost -p 5434 -u root -d green_trip
  ```

- Step 5: at this step, I already knew that the data is correctly ingested, therefore, instead of using `pgcli`, I will use `pgAdmin` for more convenient viewing. \
Like usual, you need to run containers for `pgAdmin` and `postgres` separately, but I will put them all into 1 container and using `docker compose`. 

- Step 6: in [compose.yaml](./compose.yaml), there a **networks** section, which you have to create in prior to link between `pgAdmin` and `postgres` database. (refer to [\week1-docker-terraform\docker\docker_sql\week1-tutorial.md](../docker/docker_sql/week1-tutorial.md) for more information).

- Step 7: in VSCode terminal, navigate to the folder that contains `compose.yaml` and run 
  ```
  docker compose up -d
  ```

- Step 8: after having composed, access [localhost:8080](http://localhost:8080) to pgAdmin and register the server. \
**Note:** In pgAdmin, in the *connection* tab, make sure the *Host name/address* must match the name of the database (which is **pgdatabase** (in `compose.yaml`))

- Step 9: DONE !!! You can now go to the server, select the corresponding table and do queries.

### Queries 
During the period of October 1st 2019 (inclusive) and November 1st 2019 (exclusive), how many trips, **respectively**, happened: 

1. Up to 1 mile
    ```
    SELECT COUNT(1)
    FROM green_trip_data
    WHERE trip_distance <= 1
    ```
-> 104,838

2.  In between 1 (exclusive) and 3 miles (inclusive)
    ```
    SELECT COUNT(1)
    FROM green_trip_data
    WHERE trip_distance > 1 AND trip_distance <= 3
    ```
-> 199,013 

3. In between 3 (exclusive) and 7 miles (inclusive)
    ```
    SELECT COUNT(1)
    FROM green_trip_data
    WHERE trip_distance > 3 AND trip_distance <= 7
    ```

-> 109,645

4. In between 7 (exclusive) and 10 miles (inclusive)
    ```
    SELECT COUNT(1)
    FROM green_trip_data
    WHERE trip_distance > 7 AND trip_distance <= 10
    ```

-> 27,688

5. Over 10 miles
    ```
    SELECT COUNT(1)
    FROM green_trip_data
    WHERE trip_distance > 10
    ```

-> 35,202


## Question 4
Which was the pick up day with the longest trip distance?
Use the pick up time for your calculations.

Tip: For every day, we only care about one single trip with the longest distance. 
  ```
  SELECT lpep_pickup_datetime
  FROM green_trip_data
  ORDER BY trip_distance DESC
  LIMIT 1
  ```

### Question 5
Which were the top 3 pickup locations with over 13,000 in
`total_amount` (across all trips) for 2019-10-18?

Consider only `lpep_pickup_datetime` when filtering by date.
  ```
  SELECT "Zone", SUM(total_amount) as sum_total_amount
  FROM green_trip_data, zone_data
  WHERE
    green_trip_data."PULocationID" = zone_data."LocationID"
    AND date(lpep_pickup_datetime) = '2019-10-18'
  GROUP BY "Zone", zone_data."LocationID"
  HAVING SUM(total_amount) > 13000
  ```

## Question 6
For the passengers picked up in October 2019 in the zonename "East Harlem North" which was the drop off zone that had the largest tip?

Note: it's `tip` , not `trip`
- Solution 1
```
SELECT *
FROM
  (
  SELECT "DOLocationID", SUM(tip_amount) AS total_tip_amount
  FROM green_trip_data, zone_data
  WHERE
  green_trip_data."PULocationID" = zone_data."LocationID" -- pickup zone
  AND zone_data."Zone" = 'East Harlem North' -- zone name
  AND EXTRACT(MONTH from lpep_pickup_datetime) = 10
  AND EXTRACT(YEAR from lpep_pickup_datetime) = 2019
  GROUP BY "DOLocationID"
  ORDER BY SUM(tip_amount) DESC
  ) AS drop_off_ids, zone_data
WHERE drop_off_ids."DOLocationID" = zone_data."LocationID"
ORDER BY total_tip_amount DESC
LIMIT 1
```
- Solution 2
```
SELECT z_drop."Zone", MAX(tip_amount)
FROM green_trip_data, zone_data z_pick, zone_data z_drop
WHERE
  green_trip_data."PULocationID" = z_pick."LocationID" -- pickup zone
  AND z_pick."Zone" = 'East Harlem North' -- zone name
  AND green_trip_data."DOLocationID" = z_drop."LocationID"
  AND EXTRACT(MONTH from lpep_pickup_datetime) = 10
  AND EXTRACT(YEAR from lpep_pickup_datetime) = 2019
GROUP BY z_drop."Zone"
ORDER BY MAX(tip_amount) DESC
LIMIT 1
```

-> JFK Airport

## Question 7. Terraform Workflow
Which of the following sequences, **respectively**, describes the workflow for: 
1. Downloading the provider plugins and setting up backend,
2. Generating proposed changes and auto-executing the plan
3. Remove all resources managed by terraform`

-> terraform init, terraform apply -auto-approve, terraform destroy
