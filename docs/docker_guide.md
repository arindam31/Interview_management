# Docker usage with the project.

This document provides each step and additinal guidelines to use docker
with the project.


## 1. Creating a Docker Image
To build the Docker image, navigate to the project root directory (imt) and run the following command:

```bash
docker build -t imt-django-docker .
docker image list
```

Verifying the Image
```bash
docker image list
```
Look for imt-django-docker in the output list.

## 2. Using Docker Compose
Alternatively, you can use Docker Compose to build and run the project in a single step. Navigate to the project root directory (imt) and run:

```bash
docker compose up --build
```
**This command will:**

- Build the Docker images.
- Start the containers defined in the docker-compose.yml file.

## 2.1 Viewing Logs
To see the logs for the running containers, use the following command:
```bash
docker compose logs project_imt_container
```
Where project_imt_container is the service name (check running container list).

## 3. Accessing the Running Container
3.1. Starting a Shell in the Container
To access the shell of the running container, use the following command (replace project_imt_container with the actual container name, which you can find using docker ps):

To start a shell on the running container:
```bash
docker exec -it project_imt_container bash
```

To execute commands manually on container:
  ```bash
  docker exec -it project_imt_container python manage.py createsuperuser
  ```

## 4. Stopping and Removing Containers
If you want to stop the running containers and remove them, you can use:

```bash
docker compose down
```

## 5. If you are running out of space:
```bash
docker system prune
```