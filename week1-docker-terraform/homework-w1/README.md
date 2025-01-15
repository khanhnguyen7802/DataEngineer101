\_to initialize Postgres and create a new database
docker run -it -e POSTGRES_USER="root" -e POSTGRES_PASSWORD="root" -e POSTGRES_DB="green_trip" -v E:\CS.nl\data-engineer\zoom-camp\week1-docker-terraform\homework-w1\green_trip_data:/var/lib/postgresql/data -p 5434:5432 postgres:13

\_ingest data into Postgres using `upload-data.ipynb` (2 tables)

\_check with pgcli: pgcli -h localhost -p 5434 -u root -d green_trip

\_writing docker compose to start both pgadmin and postgres

\_compose and access pgadmin, then register server (in order to add the current pgdatabase to pgadmin)

-----Q3
SELECT COUNT(1)
FROM green_trip_data
WHERE trip_distance <= 1

104,838; 199,013; 109,645; 27,688; 35,202

-----Q4
SELECT lpep_pickup_datetime
FROM green_trip_data
ORDER BY trip_distance DESC
LIMIT 1

-----Q5
SELECT "Zone", SUM(total_amount) as sum_total_amount
FROM green_trip_data, zone_data
WHERE
green_trip_data."PULocationID" = zone_data."LocationID"
AND date(lpep_pickup_datetime) = '2019-10-18'
GROUP BY "Zone", zone_data."LocationID"
HAVING SUM(total_amount) > 13000

-----Q6
SELECT \*
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
-- LIMIT 10
) AS drop_off_ids, zone_data
WHERE drop_off_ids."DOLocationID" = zone_data."LocationID"
ORDER BY total_tip_amount DESC
LIMIT 1

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
