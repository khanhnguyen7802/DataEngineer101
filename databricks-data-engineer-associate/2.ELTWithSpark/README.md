# 2. ETL with Apache Spark

## Set-up the environment

**Structure of the dataset:**

- _Operational data:_
  - addressess folder: contains `.tsv` file; format name: `addresses_<year>_<month>.tsv`
  - customers: contains `.json` file; format name: `customers_<year>_<month>.json`
  - memberships: contains images `.png`;
    format name: `<year>_<month>/{customer_id}.png`
  - orders
- _External data:_
  - payments
