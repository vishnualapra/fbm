from django.shortcuts import render
from django.http import HttpResponseRedirect
import requests
import json

# Create your views here.


def login_required(function):
    def wrap(request, *args, **kwargs):
        if 'token' in request.COOKIES:
            url = "http://localhost:8000/api/validate/"

            payload={}
            headers = {
            'Authorization': 'token ' + request.COOKIES.get("token"),
            }

            response = requests.request("POST", url, headers=headers, data=payload)
            data = json.loads(response.text)
            if data["status"] == True:
                return function(request, *args, **kwargs)
            else:
                response = HttpResponseRedirect('/web/login/')
                response.delete_cookie('token')
                return response
        else:
            return HttpResponseRedirect('/web/login/')
    return wrap

def login_view(request):
    return render(request,'web/auth-login.html',{})

def index(request):
    return HttpResponseRedirect("/web/dashboard/")


@login_required
def dashboard(request):
    return render(request,'web/dashboard.html',{})