import time
from celery import shared_task


@shared_task
def test_beat_task():
    print("Test task is running!")
    time.sleep(2)
    return "Beat task finished"