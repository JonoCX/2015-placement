__author__ = 'Jonathan'

from core.models import UserProfile, Communication
import json, datetime
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

@login_required
@csrf_exempt
def user_profile_update(request):
    if request.method == 'POST':
        pk = request.POST['pk']
        obj = request.POST['name']
        val = request.POST['value']
        d = {obj: val}
        valid_fields = [
            'username', 'title', 'first_name', 'last_name', 'user_type',
            'email', 'smart_card', 'unit', 'known_as', 'role'
        ]
        if obj in valid_fields:
            try:
                UserProfile.objects.filter(pk=pk).update(**d)
                data = {'status': 'success', 'msg': 'updated'}
            except Exception as e:
                data = {'status': 'error', 'msg': 'Value not accepted'}
        else:
            data = {'status': 'error', 'msg': 'field not valid'}
    else:
        data = {'status': 'error', 'msg': 'post not received'}
    return_json = json.dumps(data, default=string_date_json_serializer)
    return HttpResponse(return_json, content_type="application/json")

@login_required
@csrf_exempt
def communication_update(request):
    if request.method == 'POST':
        pk = request.POST['pk']
        obj = request.POST['name']
        val = request.POST['value']
        d = {obj: val}
        valid_fields = [
            'short_desc', 'full_desc', 'bh_number', 'value_of_award', 'value_awarded_to_ncl',
            'project_start_date', 'duration', 'external', 'level', 'admin_checked'
        ]
        if obj in valid_fields:
            try:
                Communication.objects.filter(pk=pk).update(**d)
                data = {'status': 'success', 'msg': 'updated'}
            except Exception as e:
                data = {'status': 'error', 'msg': 'not updated'}
        else:
            data = {'status': 'error', 'msg': 'field not valid'}
    else:
        data = {'status': 'error', 'msg': 'post not received'}
    return_json = json.dumps(data, default=string_date_json_serializer)
    return HttpResponse(return_json, content_type="application/json")

## Date serializer catch for the json converter ##
def string_date_json_serializer(obj):
    temp = None
    if isinstance(obj, datetime.date):
        temp = obj.strftime('%Y/%m%/d')
    return temp
