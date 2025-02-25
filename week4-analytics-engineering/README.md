# (Kimball's) Dimensional Modelling

## Objective

- Deliver data understandable to the business users
- Deliver fast query performance

## Approach

Prioritize user understandability and query performance over non-redundant data (3NF).

## Elements of Dimensional Modelling

![alt text](image.png)

### Facts tables

- Measurements, metrics or facts
- Correspond to business process
- _verbs_ (e.g., sales, orders, ...)

### Dimensions tables

- Provide context to a business process
- Correspond to a business entity
- _nouns_ (e.g., customers, products, ...)

### Discussion

Dimensional Modeling is built on a **star schema** with fact tables surrounded by dimension tables.

A good way to understand the architecture of Dimensional Modeling is by drawing an analogy between dimensional modeling and a restaurant:

- Stage Area:
  - Contains the raw data.
  - Not meant to be exposed to everyone.
  - Similar to the food storage area in a restaurant.
- Processing area:
  - From raw data to data models.
  - Focuses in efficiency and ensuring standards.
  - Similar to the kitchen in a restaurant.
- Presentation area:
  - Final presentation of the data.
  - Exposure to business stakeholder.
  - Similar to the dining room in a restaurant.

# Intro to `dbt`

## About

- **(data build tool)**
- is a transformation workflow that allows us to _transform_ process raw data in our Data Warehouse to _transformed_ data which can be later used by Business Intelligence tools and any other data consumers.
- Follows SE best practices (e.g., modularity, CI/CD, and documentation) by defining _deployment workflow_:
  - Develop models
  - Test and document models
  - Deploy models with version control and CI/CD.

![alt text](image-1.png)

## How does dbt work?

![alt text](image-2.png)
dbt works by defining a **modeling layer** that sits on top of our Data Warehouse. The modeling layer will turn tables into **models** which we will then transform into _derived models_, which can be then stored into the Data Warehouse for persistence.

A **model** is a .sql file with a `SELECT` statement; no DDL or DML is used. dbt will compile the file and run it in our Data Warehouse.

## Start dbt project

dbt has 2 main components: **dbt Core** and **dbt Cloud**:

- `dbt Core`: open-source project that allows the data transformation.
  - Builds and runs a dbt project (.sql and .yaml files).
  - Includes SQL compilation logic, macros and database adapters.
  - Includes a CLI interface to run dbt commands locally.
  - Open-source and free to use.
- `dbt Cloud`: SaaS application to develop and manage dbt projects.
  - Web-based IDE to develop, run and test a dbt project.
  - Jobs orchestration.
  - Logging and alerting.
  - Intregrated documentation.
  - Free for individuals (one developer seat).

For integration with **BigQuery** we will use the **dbt Cloud IDE** -> local installation of dbt core isn't required.
<br>
Using dbt with a **local Postgres** database can be done with **dbt Core**, which can be installed locally and connected to Postgres and run models through the CLI.
![alt text](image-3.png)

### Setting up Cloud environment

#### Google Cloud Storage setup

- Step 1: Access Google Cloud account (create one if you don't have yet)
- Step 2: Create a **new project**. As you have created a new project, you will also have the **project ID** (which will be used later on).
- Step 3: Navigate to **IAM and admin** -> **Service accounts** -> create a **Service Account** with role **BigQuery Admin** (since we will be working with BigQuery).
<br> Additionally, if you want to edit the roles (add, remove, update), go to **IAM and admin** -> **IAM** -> adjust roles.
- Step 4: Add key -> Create a new key -> choose the **JSON** option -> Download that file (that is your credentials). <br>
In case you need to create the key again, just `IAM and admin` -> `Service accounts` -> click on the service account that you want to generate the key -> `Keys` tab -> `Add key`.
  ![alt text](image-4.png) 

- Step 5: in your workspace, put the Google Credentials in such structure: `.google\credentials\google_credentials.json`.

#### dbt Cloud project 
- Step 1: Go to [dbt](https://www.getdbt.com/pricing) and sign up for the Free developer seat. 

- Step 2: Create a project, then set up a database connection -> choose **BigQuery**
![alt text](image-5.png)

- Step 3: Upload the `JSON` key file to use the service account. 
![alt text](image-6.png)

Save the configuration, test the connection and then `Save`.

- Step 4: The last step is to configure **Git repository**. Simply connect to Github and that's done.

  ****NOTE:** to edit your project configuration, you can do the following steps: go to the **menu bar** on the left, click on the icon of your **organization** -> choose `Account settings` -> choose `Projects` tab.

  ![alt text](image-7.png)

- Step 5: access the Cloud IDE to use **dbt**.
![alt text](image-8.png)