# Analytical Engineering

Literally analysts that can do a bit of engineering -> has the capacity of an analyst to explain to the stakeholder

## Roles in a data team

- Data engineer: prepares and maintain the infrastructure the data team needs
- Data analyst: uses data to answer questions and solve problems

➡️ Analytics engineer: introduces the good software engineering practices to the efforts of data analysts and data scientists.

### Tooling

An analytic engineer might touch:

1. Data loading - tools like Fivetran, Stitch (the EL layer)
2. Data storing: cloud data warehouses like Snowflake, BigQuery, RedShift
3. Data Modelling: Tools like dbt or Dataform
4. Data Presentation: BI tools like PowerBI, Google Data Studio, Looker, Tableau

## ETL vs ELT

- `Extract -> Transform -> Load`
  - Slightly more stable and compliant data analysis
  - Higher storage and compute costs

➡️ Takes longer to set up because the transformation logic has to be built first, but the data in the warehouse is clean and stable from day one.

- `Extract -> Load -> Transform`
  - Faster and more flexible data analysis
  - Lower cost and lower maintenance

➡️ This is the approach that cloud warehouses made possible — storage is cheap, so just load everything and figure out the transformations later.

![alt text](image-11.png)

> ELT is the dominant approach now, and it's the one we'll be working with. dbt fits squarely into the "T" of ELT — it runs transformations inside the warehouse using SQL.

# (Kimball's) Dimensional Modelling

## Objective

To deliver data **understandable to the business users** and deliver **fast query performance**.

The priority is **user understandability** and **query performance** over non-redundant data (3NF).

## Elements of Dimensional Modelling (Star Schema)

![alt text](image.png)

### Facts tables

- Measurements, metrics or facts
- Correspond to business process
- _verbs_ (e.g., sales, orders, ...)

### Dimensions tables

- Provide context to a business process
- Correspond to a business entity
- _nouns_ (e.g., customers, products, ...)

- Dimensions come into 2 flavors:
  - Slowly changing
  - Fixed

### Architecture of Dimensional Modelling

A good way to understand the architecture of Dimensional Modeling is by drawing an analogy between dimensional modeling and a restaurant:

- **Stage Area**:
  - Contains the raw data.
  - Not meant to be exposed to everyone.
  - Similar to the food storage area in a restaurant.
- **Processing area**:
  - From raw data to data models.
  - Focuses in efficiency and ensuring standards.
  - Similar to the kitchen in a restaurant.
- **Presentation area**:
  - Final presentation of the data.
  - Exposure to business stakeholder.
  - Similar to the dining room in a restaurant.

Problem: there is data redundancy -> normalization to **snowflake schema**

## Snowflake Schema

- A star schema is basically a snowflake schema having 1-level hierarchy
- Snowflake schema is more NORMALIZED.

|     |                     Advantages                      |             Disadvantages             |
| :-- | :-------------------------------------------------: | :-----------------------------------: |
|     | Less space (storage cost) thanks to less redundancy |             More complex              |
|     |   Less redundant data (easier to maintain/update)   | More joins (more complex SQL queries) |
|     |               Solves write slow downs               |  Less performance Data Marts / Cubes  |
|     |

<br>

## OLTP-to-OLAP continuum (4-layer modeling)

![alt text](image-10.png)

1. **Production Database Snapshots** <br>
   The starting point is usually OLTP systems. They handle real-time transactions: customer placing an order, transferring money, or updating account details. <br>
   However, they are not designed for complex data analysis => This is where **production database snapshots** come into play. These snapshots provide a periodic snapshot of operational data, preserving the state of the system at a given moment. <br>
   **Next step:** aggregate those data into a big whole **master data.**

2. **Master Data** <br>
   In the \*absence of a **master data layer\***, analysts have to work with raw, inconsistent data. Master data provides a single source of truth and organizing data sources. <br>
   Imagine, without a unified view of the customer, you end up with fragmented and sometimes contradictory data, which makes it difficult to draw meaningful insights.<br>
   In other words, you put everything together in the master data.

3. **OLAP Cubes** <br>
   Once we have the master data, we process it through **OLAP cubes**. For example, an OLAP cube might allow a company to analyze sales data by region or product category. <br>
   Imagine, from the master data, you split into related chunks by using OLAP cubes

4. **Metrics** <br>
   At the end of the continuum, we reach **metrics** — the ultimate output of the entire data pipeline. Whether it’s tracking sales performance, customer behavior, or operational efficiency, these metrics provide the actionable insights that drive business decisions. <br>
   In other words, from chunks in the OLAP cubes, you smash into 1 value and that's the metrics.

# DBT (Data Build Tool)

Refer to [dbt_installation.md](./dbt_installation.md) and [main_dbt.md](./main_dbt.md).
