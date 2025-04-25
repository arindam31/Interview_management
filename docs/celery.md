# Celery useful commands


### To find registered tasks :

- Start a bash on the celery docker service
- Execute the following:
    ```bash
    C:\Projects\Interview_management\imt> docker-compose exec celery bash
    appuser@c999ca879eb7:/code$ celery -A imt_mng.celery inspect registered
    
    ->  celery@c999ca879eb7: OK
    * imt_mng.celery.debug_task
    * jobs.tasks.test_beat_task

    1 node online.
    ```