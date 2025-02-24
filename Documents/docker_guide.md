# Docker usage with the project.

## Creating an image (be at dir: imt)
- > ´docker build -t imt-django-docker .´
- check if image was created
    > `docker image list`

Or 
- docker compose up --build

### Other commands

- To start a shell on the running container:
  > `docker exec -it project_imt_container bash`

- To execute commands manually on container:
  > `docker exec -it project_imt_container python manage.py createsuperuser`

