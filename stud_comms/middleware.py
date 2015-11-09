__author__ = 'Jonathan Carlton'
from core.models import UserProfile
from django.http import HttpResponse
from django.core import serializers
import json

class CommsMiddleware(object):

    def process_request(self, request):
        pass

        # request.user = UserProfile.objects.get(username=request.user.username)
