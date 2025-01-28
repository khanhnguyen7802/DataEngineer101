# Introduction

## What is Databricks?

- Is an **open analytic platform** for building, deploying, sharing and maintaining enterprise-grade data, analytics and AI solution at scale | built on Apache Spark
- Can: build an enterprise data lakehouse | ETL and data engineering | ML, AI … | data warehousing, analytics and BI | DevOps

# Create Azure Databricks Service

- Step 1: Acces [portal.azure.com](portal.azure.com) and choose _Create a resource_. Search for `Azure Databricks`.
- Step 2: Fill in the form.

  - Basics
    - Subscription: either Pay-As-You-Go or Student Account.
    - Resource group: where we keep all resources needed. Suggested name: `databrickscourse-rg`
    - Workspace name: suggested `databrickscourse-ws`
    - Region: choose the one that is (near) you for low latency. Regarding optimization for Student Account -> choose `UK South`
    - Pricing Tier: choose `Premium`
  - Networking: set all by default (unless you want your own configuration)

- Step 3: hit `Create` button. It will take quite a while (~5mins) to complete validation and creation.

- Step 4: Launch the workspace to actually use Databricks

# Overview of Databricks UI

![alt text](image.png)

- `New`: let you create some of Databricks objects, such as Notebooks, clusters, ... etc
- `Workspace`: a container for holding a set of folders, libraries and files. By default, each user has their **own workspace** and also **the shared one**. There is also Git in this section that allows you to migrate your work in GitHub.
- `Catalog`: let us interact with any tables that you created
- `Workflow`: contain jobs, job runs, and Delta Live Tables
- `Compute`: let us create clusters, cluster pools and SQL data warehouses.

## Architecture Overview

![alt text](image-1.png)

- Is split into 2 parts:
  - `Control Plane`: located in Databricks own subscription, containing:
    - Databricks UX
    - Cluster Manager: when a cluster is requested by the user, the Cluster Manager will create the required VM in our subscription via Azure Resource Manager
    - Databricks File System (DBFS)
    - Metadata about Clusters, Files Mounted, etc ...
  - `Data Plane`: located in the customer subscription. When creating Databricks services in Azure, there are 4 resources created in your own subscription:
    - A virtual Network and Network Security Group for the VNet
    - Azure Blob Storage for the default storage (_not recommend for the permanent data storage_)
    - A Databricks Workspace

# Databricks Cluster

## Cluster types

- A cluster is basically a collection of VMs, where each consists of a **Driver node** and (one or more) **Worker nodes**. <br>
  Clusters allow us to treat this group of computers as a **single compute engine** via the Driver node.
  ![alt text](image-2.png)

- There are 2 types of clusters:

|     |            All purpose             |             Job cluster             |
| :-- | :--------------------------------: | :---------------------------------: |
|     |          Created manually          |           Created by jobs           |
|     |             Persistent             |  Terminated at the end of the job   |
|     | Suitable for interactive workloads |  Suitable for automated workloads   |
|     |      Shared among many users       | Isolated just for the job workloads |
|     |          Expensive to run          |           Cheaper to run            |
|     |    -> Interactive analysis work    |     -> Repeated production work     |

<br>

- `Cluster Policy`: help us with pre-configuration, so that creating a Cluster will become easier. Also, it helps restrict the maximum size of the Clusters being created to keep the cost under control.

## Cluster Configuration

![alt text](image-3.png)

- `Single node` or `multi node`: Multi node will have one Driver node and (one or more) Workers node. Single node does not have Worker nodes, so only light-weight workload.
- `Access mode`: there are 4 types

  - **Single user**: only allows **a single user** to access the cluster. Supports Python, SQL, Scala, R.
  - **Shared**: multiple user access; provides process isolation -> each process gets its environment, so one cannot see the data nor credentials from the other.
  - **No isolation shared**: also allows the Cluster to be shared amongst more than one user. Different from the `shared` mode is that this does not provide any process isolation, thus failure in one user's process may affect the others. <br>
    Also, it does not offer any task preemption -> one running process may use up all the resources and the other may fail.

- Runtime: the set of core libraries that run on Databricks Clusters. There are 4 types:
  - Databricks runtime: includes an optimized version of Apache Spark library | Scala, Java, Python, R | Ubuntu libraries | GPU libraries | Delta Lake | other Databricks services
  - Databricks runtime ML: Databricks runtime + ML libraries (PyTorch, Keras, TensorFlow, XGBoost, ...)
  - Photon runtime: Databricks runtime + Photon Engine (i.e., Databricks native vectorized query engine that runs SQL workloads faster and reduces your cost per workload).
  - Databricks runtime light: for jobs that are not requiring advanced features such as auto scaling, reliability, and improved performance. <br>
    It is only suitable for Automated Workloads, cannot use it for Interactive Workloads nor Notebook jobs.
- Auto termination: avoid unnecessary costs on ilde clusters (terminate cluster after _n minutes_ of inactivity)
- Auto scaling: automatically add/remove nodes from the Cluster depending on your workload.
- Cluster VM Type/Size:

  - Memory Optimized: recommend for memory intensive applications. E.g., a ML workload that caches a lot of data in memory.
  - Compute Optimized: useful for structured streaming applications, where you need to make sure that the processing rate is above the input rate at peak times of the day.
  - Storage Optimized: recommended for use cases requiring high disk throughput and I/O.
  - General Purpose: recommended for Enterprise applications and analytics with in-memory caching.
  - GPU Accelerated: recommended for Deep Learning models which are data and compute intensive.

- Cluster Policy (_only available in Premium Tier_): Administrators can create policies with restrictions, and assign them to users/groups -> achieve cost control by limiting the maximum size of clusters.

## Azure Databricks Pricing

- Depends on a number of factors:

  - Type of workload (All purpose, Jobs compute, Databricks SQL, Photon Engine...)
  - Tier of Databricks workspace (Standard/Premium)
  - VM type (General Purpose/GPU/Optimized)
  - Purchase plan (Pay-as-you-go/Pre-purchases)
  - We also have to pay for the VM themselves too.

  ### Databricks Unit

  - Is a normalized unit of processing power on the Databricks Lakehouse Platform used for measurement and pricing purposes.

## Azure Databricks Cluster Pool

- Clusters usually take time to start up an Auto Scale. In order to minimize that time, we can use **Pools**. <br>
  -> Cluster Pool is basically a set of idle, ready to use VMs that allow us to reduce the Cluster start and Auto Scaling time. E.g.,

## Cluster Policy

- Is basically a set of rules which allows us to hide or take out the configuration options. They allow us to fix the values of some of the configuration params and restrict access for the users -> easier UI.
- An admin can create a policy and assign that to a set of users.
- Cluster policies take away **the need for an administrator** to be involved in every cluster creation decision.

  ### Define the policy

  - JSON format

  ```
    {
      "spark_conf.spark.databricks.cluster.profile": {
        "type": "fixed",
        "value": "singleNode",
        "hidden": true
      },
      "node_type_id": {
        "type": "allowlist",
        "values": [
          "Standard_DS3_v2",
          "Standard_D3_v2",
          "Standard_DS12_v2",
          "Standard_D12_v2"
        ],
        "defaultValue": "Standard_DS3_v2"
      },
      "autotermination_minutes": {
        "type": "fixed",
        "value": 20
      },
      "spark_version": {
        "type": "fixed",
        "value": "auto:latest-lts",
        "hidden": true
      },
      "cluster_type": {
        "type": "fixed",
        "value": "all-purpose"
      }
    }
  ```

  ![alt text](image-4.png)

  - You can also override (inherit) the policy.

# Databricks Notebooks

## Magic command

- In case you want to write SQL commands in a Python environment -> follow this command:

  ```
  %sql
  SELECT ...
  ```

- To list all the files in system -> use this command:
  ```
  %fs
  ls
  ```

# Databricks Utilities

## File system utilities

- To see what contents we have in a Folder, use the command:

  ```
  dbutils.fs.ls('<folder_path>')
  ```

  This will output as a **Python list**.

- To get help with any method in this package:
  ```
  dbutils.fs.help('<name_of_method>')
  ```

# Azure Data Lake

## Accessing Azure Data Lake from Databricks

- In Databricks, we generally use Azure Data Lake Storage Gen 2 as the Data Lake Storage solution.

  ### Create Storage Account

  - Step 1: go to Azure Portal -> Create new resource -> Search for _Storage Account_ -> Create
  - Step 2: fill in the form for creation. The setting should be similar to the below images. Everything else can be set _by default_.
    ![alt text](image-5.png)
    ![alt text](image-6.png)
  - Step 3: Deploy the resource
  - Step 4: after deployment, click `Go to resource` to go to the `Storage Account`. Then, on the left menu, cick on tab `Data Storage` -> `Containers`. In this project, we are having 3 containers called: **raw, processed and presentation** (~ equivalent to bronze, silver and gold).
  - Step 5: create the 3 containers.
    ![alt text](image-7.png)

## Azure Storage Explorer

- By using ONLY the web browser, you dont have many choices in performing operations.
  Therefore, a desktop tool has come to help with interacting with DataLake, called `Azure Storage Explorer`.

  ### How to download?

  - Step 1: Navigate to `Storage Accounts` tab in Portal Home.
  - Step 2: choose the newly created storage account, then choose `Storage browser` -> `Download Azure Storage Explorer`

  ![alt text](image-8.png)

  - Step 3: it will now redirect to an Azure page. Click on tab **Download** and choose the corresponding OS. After that, run the `.exe` file to finish with the setup
  - Step 4: Open the application and sign in with your Azure account. You will be able to see the folder contents after having successfully signed in.

## Access Azure Data Lake Gen2 using Access Keys

- In Auzre notebooks, if you want to get data from your storage -> use `access key` to access your storage

  ### What is Access Key?

  - Each storage comes with 2 keys (512 bit)
  - Give full access to the storage account

  ### Access Key - Spark configuration

  - To access the data from Databricks, we need to **provide one of the access keys to Azure Databricks**, so that it can authenticate to the ADLs Gen2 service.
  - By assigning the access key, to a Spark configuration called `fs.azure.account.key`.
    ```
    spark.conf.set(
      "fs.azure.account.key.formula1in2025.dfs.core.windows.net",
      "<key>"
    )
    ```
    ![alt text](image-9.png)

  ### Access Key - abfs driver

  - A new driver, which is part of the Apache Hadoop suite of products
  - Starts with `abfs[s]://`; the optional `s` ensures TLS (Transport Level Security). The data will be encrypted while at transit.
  - The syntax: `abfs[s]://<container>@<storage_account_name>.dfs.core.windows.net/<folder_path/file_name>`
    <br> E.g., `abfss://demo@formula1dl.dfs.core.windows.net/test` URI points to a folder **test** within the **demo** container.

  ### Practical

  - Step 1: open Databricks workspace.
  - Step 2: create a new folder (straight under `Workspace`), not under any specific user.
  - Step 3: get the access key: go to Portal -> navigate to the storage account -> get Keys.
    ![alt text](image-10.png)
  - Step 4: use Spark config to set the access key.
    ![alt text](image-11.png)

    (_Optional_) You can wrap the command in `display()` for better formatted output.

## Access Azure Data Lake using SAS token

- Can be used to control access at a more granular level
- Can restrict access to specific resource types or services. For example, we can allow access to only Blob containers
- Allow specific permissions. For example, allow Read-only access to a container
- Restrict access to a specific time period
- Limit access to specific IP addresses

  ### Shared Access Signature using Spark config

  For instance:

  ```
  spark.conf.set("fs.azure.account.auth.type.formula1in2025.dfs.core.windows.net", "SAS")
  spark.conf.set("fs.azure.sas.token.provider.type.formula1in2025.dfs.core.windows.net", "org.apache.hadoop.fs.azurebfs.sas.FixedSASTokenProvider")
  spark.conf.set("fs.azure.sas.fixed.token.formula1in2025.dfs.core.windows.net", "<token>")

  ```

  ![alt text](image-12.png)

  ### Practical

  ![alt text](image-13.png)
  When generating the SAS token, it will ask to choose which `access key` will be used to sign the SAS token. IF THE ACCESS KEY IS RE-GENERATED, YOU WILL NOT BE ABLE TO USE SAS TOKEN EITHER.

  After having generated the token, just simply copy paste into the missing place. The remaining procedure should be the same as working with `Access Key`.

## Access Azure Data Lake using Service Principal

### What is Service Principal?

- Similar to user account
- Can be registered in Azure Active Directory and assigned permissions required to access resources
- Is recommended method to use in automated tools like **Databricks jobs**, **CI/CD pipeline**
  ![alt text](image-14.png)

### Practical

![alt text](image-15.png)

After this, you need to assign the role to the Data Lake:

- Go to the dedicated storage account
- Choose `Access Control (IAM)` on the tab menu -> `Add` -> `Add role assignment`
- Search for `Storage Blob Data Contributor` -> Next
- Assign access to `User, group or service principal` -> Select member (i.e., the storage account you created)
- Finally, `review and assign`.

## Cluster Scoped Authentication

### About

- What we have been doing so far is validating the authentication within the session established by the execution of the Notebook (**Session Scoped Authentication**). The authentication is only valid **WITHIN THE SESSION**. <br>
  -> Once the Notebook is detached -> re-authenticate again. <br>

- Therefore, instead of authenticating from notebook, do it **WITHIN** the cluster at the startup <br>
  -> Every notebook connecting to the cluster has acccess to the storage (C**luster Scoped Authentication**).
- We can achieve that by: specifying **Spark config params** and corresponding **secret values** within the Cluster config <br>
  -> As the Cluster is created, it already had the Spark config set with the right Secret value.
- **Advantages**: effectively making the cluster **specific** for one permission group, in which all users require the same level of access.
- **Drawbacks**: **EVERY** notebook runs _on this cluster_ will have the access to the Data Lake.

<br> THIS APPROACH IS NOT WIDELY USED IN THE INDUSTRY DUE TO **MANY DIFFERENT** CLUSTERS BEING CREATED FOR DIFFERENT ROLES -> waste of resources

### Practical

- Step 1: Go to Compute tab -> `Edit` button on the right corner
- Step 2: expand the `Advanced options` -> scroll down to the bottom
- Step 3: as the Spark config is in the format `key value` separated by blank space, edit it as follow:
  ```
  "fs.azure.account.key.formula1in2025.dfs.core.windows.net" <your key>
  ```
- Step 4: confirm and restart the cluster

  **Note:** You can also do that with SAS token and Principal Services.

## Securing access to Azure Data Lake

### Overview

- `Secret Scope` (in Databricks): a collection of secrets identified by a name. There are 2 types:
  - **Databricks backed Secret scope**: a secret scope is backed by an encrypted databricks database owned and managed by Databricks. <br>
    We can create and alter the encrypted database using the _Databricks CLI_ or the _API_; cannot use Graphical UI.
  - **Azure Key Vault backed Secrete scope**: the secrets are created and managed in Azure Key Vault. By keeping the secrets in Azure, they can be shared among other Azure services such as Azure Data Factory, Azure Synapse Analytics, ...

![alt text](image-16.png)

### Creating Azure Key Vault

- Step 1: click `Create a resource` -> Search for _Key Vault_
- Step 2: in **Access Configuration** tab, in **Permission model**, choose `Vault access policy`.
- Step 3: Create the resource
- Step 4: After having created -> go to the `Key Vault` -> `Objects` -> `Secrets` -> `Generate/Import`

  ![alt text](image-17.png)

- Step 5: Create a secret. In this example, I'm gonna set the `Access Key` as the secret.

  ![alt text](image-18.png)

### Creating Secret Scope

- Step 1: Navigate to the homepage of Databricks (by clicking the icon). Then add **#secrets/createScope** at the end of the URL. This URL is case sensitive. For example, scope in createScope must use an uppercase S).
  ![alt text](image-19.png)

- Step 2: fill in the form

  - Manage Principal: choose `All workspace user`
  - DNS name: go to the created `Key Vault` -> `Settings` tab -> `Properties` -> `Vault URI`.
  - Resource ID: also the `Resource ID` in the same session as above.

- Step 3: click `Create`


### Databricks Secrets Utility 
- Purpose: to get secret values from Databricks Secret Scope and Azure Key Vault. 

- Different methods in dbutils.secrets:
  - `dbutils.secrets.list(scope="<scope_name>")`
  - To achieve the secret value: `dbutils.secrets.get(scope="<scope_name>", key="<key_value>")` -> however, it will only be showed as **REDACTED**

  #### Using Secrets utility in Cluster 
    - Go to `Edit` in a Cluster in Databricks. 
    - Edit several things in Spark config: `fs.azure.account.key.<storage_account>.dfs.core.windows.net {{secrets/<secret_scope_name>/<secret_name>}}`