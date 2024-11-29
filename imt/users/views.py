from django.shortcuts import render
from django.http import HttpResponse
import logging
from .models import Staff

logger = logging.getLogger("users")


# Create your views here.
def hello(request):
    logger.info("Hello my world")
    return HttpResponse("Hello, world.")


class StaffView:
    def get(self, request, id: int):
        return HttpResponse(Staff.objects.get(id=id))
