# About 
This folder demonstrates all components needed for Dockerization. 

Overview of the workflow: 
1. `compose.yaml` -> check `build: .`, which means that Docker will look for **Dockerfile** in that path and execute the **Dockerfile** line by line -> build the **image**.  

2. Afther that, Docker launches the services as `containers`. Each service will have its own container.  

# Set up environment
1. Prepare the `ingest_data file`. In this file, we download the dataset, perform modification on the schema, connect to the database (i.e., the **pgdatabase** service in container) and ingest the data into the database via the connection.

> Pay attention when creating the engine, as the hostname should be `<service_name>:<corresponding_port_in_docker>`.

2. Next, define `compose.yaml` that includes the services used. 
  - `ingest_data`: we build the image by ourselves, using the specific Dockerfile (see below in **3.**). In this service, the `volumes` is set as `./green_trip_data:/app/green_trip_data` which means any files in *./green_trip_data* on the host machine will appear in */app/green_trip_data* inside the container; and if the container writes to */app/green_trip_data*, those changes will be saved to *./green_trip_data* on your host.

    -> So, the data will persist across container restarts.

      
    Since **starting the services** does not follow an order, the field *depends_on* says that the database service must start first before ingesting the data. 
  
  - `pg_database`: the database service using the **Postgres image**. In this service, we configure the environment and map new ports (you might already have PostgreSQL running on your local machine on port 5432, so you avoid a conflict by mapping the container to a different host port like 5434) <br> 
  -> **Purpose**: to access the container from your machine on port **5434**, even though it runs on 5432 inside. 

    In case you want the data to be mapped accordingly with the ones in the container (data persists between container restarts), you can define `volumes` to map one another. Otherwise, without defining volumes, Postgres uses its container's ephemeral storage instead (data will be completely new for each restart).
    Additionally, we need to define `healthcheck` for the condition of *depends_on* field.

  - `pgadmin`: the pgAdmin service (for monitoring database) using the **pgadmin4 image**. The `volumes` here is to save the server connection, user and session data. By defining it, pgAdmin keeps its data across restarts.

  - `networks`: to define a network (namely **pg-network**) that connects **pgdatabase** to **pgadmin**.

3. Write commands for `Dockerfile` for a specific service (i.e., ingest data). 
The `CMD` states that the command will be executed when that container starts. 

# How to start?
- Step 1: Make sure you have docker
- Step 2: use `docker commpose up` to bring up all the containers. 
> In case you make changes in `Dockerfile`, run `docker compose build` or `docker compose up --build` to rebuild the images. 
- Step 3: as soon as everything is set, you can access to pgAdmin via localhost. When having logged in pgAdmin, in order to view its database, you need to **register the correct server**. 
- Step 4: now, you can do query as your preference. 
After having finished all, you can close the containers by `docker compose down`.
