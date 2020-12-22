from rest_framework import serializers
from rest_framework import exceptions, response
from django.contrib.auth import authenticate
from rest_framework.validators import UniqueValidator
from . import models
from rest_framework.response import Response
from datetime import datetime, date
import requests



class PageSerializer(serializers.ModelSerializer):
    details = serializers.SerializerMethodField('getdetails')

    def getdetails(self,datas):
        url = "https://graph.facebook.com/{}?fields=about,attire,bio,location,parking,hours,emails,phone,website&access_token={}".format(datas.page_id,datas.access_token)
        r = requests.get(url)
        access_token_info = r.json()
        print(access_token_info)
        details = {}
        if "about" in access_token_info:
            details["about"] = access_token_info["about"]
        else:
            details["about"] = ""

        if "emails" in access_token_info:
            details["email"] = access_token_info["emails"]
        else:
            details["email"] = ""
        if "website" in access_token_info:
            details["website"] = access_token_info["website"]
        else:
            details["website"] = ""
        if "phone" in access_token_info:
            details["phone"] = access_token_info["phone"]
        else:
            details["phone"] = ""
        return details
    class Meta:
        model = models.Page
        fields = ('id','title','page_id','page_icon','created_at','details')


