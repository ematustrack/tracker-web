from server.models import Pro
from django.http import HttpResponse
from functools import wraps
import json

class FilterPhone(object):

    def __init__(self, view_func):
        self.view_func = view_func
        wraps(view_func)(self)

    def __call__(self, request, *args, **kwargs):
        number = request.META.get('HTTP_TOKEN_NUMBER')
        print number
        allowed_numbers = Pro.objects.all().only('phone')
        for value in allowed_numbers:
            if value.phone == number:
                print "value -> ",value.phone
                response = self.view_func(request, *args, **kwargs)
                return response
        response = {
            "message":"error with your phone",
        }
        return HttpResponse(json.dumps(response),status=404)
