#!/bin/sh
celery -A imt_mng.celery beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler