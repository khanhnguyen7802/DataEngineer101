# Instructions for homework - Week 1 - Cohort 2026
For the setup (pgAdmin + postgres) in Question 3, I also have a [tutorial video](https://www.youtube.com/watch?v=_iqCWi_UoOc).

## Question 1

Run docker with the `python:3.13` image in an interactive mode, use the entrypoint `bash`.

What's the version of `pip` in the image?

-> **Solution:** 25.3

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
  db:
    container_name: postgres
    image: postgres:17-alpine
    environment:
      POSTGRES_USER: "postgres"
      POSTGRES_PASSWORD: "postgres"
      POSTGRES_DB: "ny_taxi"
    ports:
      - "5433:5432"
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

volumes:
  vol-pgdata:
    name: vol-pgdata
  vol-pgadmin_data:
    name: vol-pgadmin_data
```

**Solution:** To connect to the **postgres database**, we need to access its service, which is `postgres`. The service that contains _postgres_ is defined as `db`, and looking at the port, we see _5433:5432_, which means _map the port from host machine **(5433)** to the port inside postgres container **(5432)**._

-> Answer: `db:5432`

## Set up the environment with pgAdmin + postgres (prepare the data)

- Step 1: In VSCode terminal, navigate to the folder that contains `docker-compose.yaml` and run

  ```
  docker compose up -d
  ```

  As I have defined all the needed services _(pgAdmin + postgres)_ in `docker-compose.yaml` file, services will work when you run the above command.

- Step 2: When all the services are up, it's time to ingest the data. In the [Jupyter notebook](./ingest_data_manually.ipynb), we create an empty folder (namely `green_trip_data`) to ingest the data into.

  The download links for the dataset are as follows:

  ```
  wget https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-11.parquet
  ```

  ```bash
  wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv
  ```

  Run every cell in the notebook to download + ingest data.

- Step 3 (_optionally | I would skip this_): use `pcli` to check whether the data is ingested properly. (_I used `conda` in CMD to run the command_).

  ```
  pgcli -h localhost -p 5434 -u root -d green_trip
  ```

  > The command connects to localhost using port 5434, under user **root** and access database **green_trip** (as defined in `docker-compose.yaml`).

  Personally, I'd skip this step and go straight for `pgAdmin`.

- Step 4: After having ingested all the data from the notebook, I will use `pgAdmin` for convenient viewing. Access [localhost:5050](http://localhost:5050) to pgAdmin. Normally, you need to register the server, however, I have already included in `docker-compose.yaml
`, so you just have to enter the password for the database, and that's all.

- Step 5: DONE !!! You can now go to the server, select the corresponding table and do queries.

## Queries

### Question 3

For the trips in November 2025 (`lpep_pickup_datetime` between '2025-11-01' and '2025-12-01', exclusive of the upper bound), how many trips had a `trip_distance` of less than or equal to 1 mile?

```sql
SELECT COUNT(*)
FROM "green_trip_2025-11"
WHERE lpep_pickup_datetime >= '2025-11-01'
      AND lpep_pickup_datetime < '2025-12-01'
	  AND trip_distance <= 1
```

-> 8007

### Question 4

Which was the pick up day with the longest trip distance? Only consider trips with `trip_distance` less than 100 miles (to exclude data errors).

Use the pick up time for your calculations.

```sql
SELECT lpep_pickup_datetime
FROM "green_trip_2025-11"
WHERE trip_distance < 100
ORDER BY trip_distance DESC
LIMIT 1
```

-> 2025-11-14 15:36:27

### Question 5

Which was the pickup zone with the largest `total_amount` (sum of all trips) on November 18th, 2025?

- East Harlem North
- East Harlem South
- Morningside Heights
- Forest Hills

```sql
SELECT zone_data."LocationID", "Zone", SUM(total_amount) AS sum_of_all_trips
FROM "green_trip_2025-11", zone_data
WHERE
  "green_trip_2025-11"."PULocationID" = zone_data."LocationID"
  AND DATE(lpep_pickup_datetime) = '2025-11-18'
GROUP BY zone_data."LocationID", "Zone"
ORDER BY sum_of_all_trips DESC
LIMIT 1
```

-> East Harlem North

## Question 6

For the passengers picked up in the zone named "East Harlem North" in November 2025, which was the drop off zone that had the largest tip?
**Note:** it's **tip**, not trip. We need the name of the zone, not the ID.

- JFK Airport
- Yorkville West
- East Harlem North
- LaGuardia Airport

```sql
SELECT z_drop."Zone", MAX(tip_amount)
FROM "green_trip_2025-11", zone_data z_pick, zone_data z_drop
WHERE
  "green_trip_2025-11"."PULocationID" = z_pick."LocationID" -- pickup zone
  AND z_pick."Zone" = 'East Harlem North' -- zone name
  AND "green_trip_2025-11"."DOLocationID" = z_drop."LocationID"
  AND EXTRACT(MONTH FROM lpep_pickup_datetime) = 11
  AND EXTRACT(YEAR FROM lpep_pickup_datetime) = 2025
GROUP BY z_drop."Zone"
ORDER BY MAX(tip_amount) DESC
LIMIT 1
```

-> Yorkville West

## Question 7. Terraform Workflow

Which of the following sequences, **respectively**, describes the workflow for:

1. Downloading the provider plugins and setting up backend,
2. Generating proposed changes and auto-executing the plan
3. Remove all resources managed by terraform

-> terraform init, terraform apply -auto-approve, terraform destroy
