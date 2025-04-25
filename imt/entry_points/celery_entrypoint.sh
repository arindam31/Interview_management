#!/bin/sh
celery -A imt_mng.celery worker --loglevel=info