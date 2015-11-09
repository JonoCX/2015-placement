__author__ = 'student'
from django.contrib.syndication.views import Feed
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Communication
from django.core.urlresolvers import reverse

class CommunicationFeed(Feed):
    title = "Latest Communications"
    link = "/"

    def items(self):
        return Communication.objects.all().order_by('-created_on')[:5]

    def item_title(self, item):
        return item.short_desc

    def item_description(self, item):
        return item.full_desc

    def item_link(self, item):
        return '/comms-feed/'