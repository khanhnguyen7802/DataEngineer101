# About

## Some general knowledge

### What is virtualization?

- In the virtual machine, we are able to run the whole OS. This technique is usually used in the Cloud when deploying, such as AWS. Typically, what you are doing is putting up a new virtual machine and you can then deploy your code onto.
- A virtual machine has a type of program that can run and manage the life cycle of these machines, which is called **Hypervisor**. E.g., VMWare.

### What is containerization?

- Docker manages the life cycle of containers and it then runs them and interacts with them.
- To sum up, containerization is the ability to create a light-weight environment where processes can run on a host operating system. They share all things in that operating system but they cannot touch anything outside that bounded box.

## What is Docker?

- A software development platform makes it easy to develop and deploy apps
  inside of neatly packed **virtually containerized environment**. <br>

![VM vs Docker](image.png)

|              |                              VM                               |                            Docker                            |
| :----------- | :-----------------------------------------------------------: | :----------------------------------------------------------: |
| OS support   |                  Occupies a lot of mem space                  |                      Occupy less space                       |
| Boot-up time |                       Long boot-up time                       |                      Short boot-up time                      |
| Performance  |      Running multiple VMs leads to unstable performance       | Better performance as it is hosted in a single Docker engine |
| Scaling      |                     Difficult to scale up                     |                       Easy to scale up                       |
| Efficiency   |                        Low efficiency                         |                       High efficiency                        |
| Portability  | Compatibility issues while porting across different platforms |          Easily portable across different platforms          |

## Components

1. Dockerfile: is just code telling Docker how to build an image.
2. Image: is a snapshot of all softwares and their dependencies down to the OS level \
   -> is used for running Docker Containers.
   Images can be stored in either public or private repos, but usually public repos are used to host Docker Images which can be used by everyone. - Immutable, i.e., cannot be modified after being created. - Composed of layers; each layers represents a set of file system that changes, add, remove or modify files.
3. Container: is a standalone, executable software package which includes applications and their dependencies.
4. Registry: contains repos where Images are stored, which allows you to share images across teams. \
   Docker also has its own default registry called Docker Hub.

![alt text](image-1.png)

## Basic commands

- To build a container -> `pull` is used to get a Docker image from the Docker repo.
- With `push` -> store the Docker Image in Docker Registry.

## Summary

- Dockerfile creates a Docker Image -> contains all project's code -> any user can run the code in order to create Docker Containers -> once the Image is built, it's uploaded in a Registry or a Docker Hub -> From Docker Hub, users can get the Docker Image and build new containers.

  ![alt text](image-2.png)

# Installation

## First step

Download Docker Desktop from their [official page.](https://docs.docker.com/get-started/introduction/get-docker-desktop/) \
After downloading, run the `.exe` file to set up Docker. \
After having finished setting up, open terminal, run `docker -v` to make sure Docker is indeed installed.
![alt text](image-3.png)

## Run the first container

Open your CLI terminal and start a container by running the `docker run` command:

```<bash>
docker run -d -p 8080:80 docker/welcome-to-docker
```

![alt text](image-4.png)

For this container, the frontend can be accessed on port 8080. Open via your [localhost](http://localhost:8080).

## Stop the container

The container continues until you stop it. You can stop a cointainer using `docker stop`

- Run `docker ps` to get the ID of the container.
- Provide the container ID or name to the `docker stop`:

```<bash>
docker stop <the-container-id>
```

# More about

## Running containers

A `docker run` command takes the following form:

```
docker run [OPTIONS] IMAGE[:TAG|@DIGEST] [COMMAND] [ARG...]
```

- An image tag is the image version, which defaults to latest.
  Use the tag to run a container from specific version of an image. \
  For example, to run version **24.04** of the ubuntu image: `docker run ubuntu:24.04`.
- [OPTIONS] let you configure options for the container. \
  For example, you can give the container a name `(--name)`,
  or run it as a background process `(-d)`.
- [COMMAND] and [ARG...] are positional arguments
  to specify commands and arguments for the container
  to run when it starts up. \
  For example, you can specify `sh` as the [COMMAND],
  combined with the `-i` and `-t` flags, to start an interactive shell in the container (if the image you select has an sh executable on PATH).
  ```<bash>
  docker run -it IMAGE sh
  ```

## Dealing with Images

### Search and download an image

Open the terminal and search for images :

```
docker search docker/welcome-to-docker
```

If an error is encountered for WSL2/Ubuntu (something like
`Error response from daemon: open \\.\pipe\docker_engine_windows: The system cannot find the file specified docker error`),
then you may need to adjust in Docker Destop. \
Go to Docker Desktop -> **Settings** -> tab **Resources** -> **WSL integration** -> turn on the `Ubuntu` option.
![alt text](image-6.png)
Upon running, the terminal shows:
![alt text](image-7.png)

Download the image using command `pull`:

```
docker pull docker/welcome-to-docker
```

![alt text](image-5.png)

### Learn about the image

1. List the download images using:
   ```
   docker image ls
   ```
   Or
   ```
   docker images
   ```
2. List the image's layers using:
   ```
   docker image history docker/welcome-to-docker
   ```
   This output shows you all of the layers, their sizes,
   and the command used to create the layer.

## Dealing with Registries

### Registry vs Repository

A registry is a centralized location that stores and manages
container images, whereas a repository is a collection
of related container images within a registry.

![alt text](image-8.png)

### Example

1. Clone this github repo (a sample Node.js project with pre-built Dockerfile):
   ```
   git clone https://github.com/dockersamples/helloworld-demo-node
   ```
2. Navigate to the cloned folder.
3. Run the following command to build the Image:
   ```
   docker build -t <YOUR_DOCKER_USERNAME>/docker-quickstart .
   ```
   ![alt text](image-9.png)
4. Use `docker images` to view the newly created Docker Image.
5. Use the `docker tag` to label the version of Image:
   ```
   docker tag <YOUR_DOCKER_USERNAME>/docker-quickstart <YOUR_DOCKER_USERNAME>/docker-quickstart:1.0
   ```
6. Push to Docker Hub

   ```
   docker push <YOUR_DOCKER_USERNAME>/docker-quickstart:1.0
   ```

   ![alt text](image-10.png)

7. Go to [Docker Hub](https://hub.docker.com/) to view your Image.
   ![alt text](image-11.png)
