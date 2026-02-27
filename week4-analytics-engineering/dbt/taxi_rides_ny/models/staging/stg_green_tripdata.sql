{{ config(materialized='view') }}

SELECT
  -- identifiers (standardized naming for consistency accross yellow/green)
  CAST(vendorid AS INTEGER) AS vendor_id,
  CAST(ratecodeid AS INTEGER) AS rate_code_id,
  CAST(pulocationid AS INTEGER) AS pickup_location_id,
  CAST(dolocationid AS INTEGER) AS dropoff_location_id,

  -- timestamps
  CAST(lpep_pickup_datetime AS TIMESTAMP) AS pickup_datetime,
  CAST(lpep_dropoff_datetime AS TIMESTAMP) AS dropoff_datetime,

  -- trip info
  store_and_fwd_flag,
  CAST(passenger_count AS INTEGER) AS passenger_count,
  CAST(trip_distance AS NUMERIC) AS trip_distance,
  CAST(trip_type AS INTEGER) AS trip_type,

  -- payment info 
  CAST(fare_amount AS NUMERIC) AS fare_amount,
  CAST(extra AS NUMERIC) AS extra,
  CAST(mta_tax AS NUMERIC) AS mta_tax,
  CAST(tip_amount AS NUMERIC) AS tip_amount,
  CAST(tolls_amount AS NUMERIC) AS tolls_amount,
  CAST(ehail_fee AS NUMERIC) AS ehail_fee,
  CAST(improvement_surcharge AS NUMERIC) AS improvement_surcharge,
  CAST(total_amount AS NUMERIC) AS total_amount,
  CAST(payment_type AS INTEGER) AS payment_type

FROM {{ source('raw_data', 'green_tripdata') }}
WHERE vendorid IS NOT NULL 
