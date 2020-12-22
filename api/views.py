from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
# from . import serializers
from rest_framework.permissions import BasePermission
from rest_framework import viewsets
from FBM.settings import SOCIAL_AUTH_FACEBOOK_KEY
from FBM.settings import SOCIAL_AUTH_FACEBOOK_SECRET
import requests
from . import models
from django.contrib.auth.models import User
from django.contrib.auth import login
from rest_framework.authtoken.views import Token
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from . import serializers
from django.contrib.auth import login, logout, authenticate, get_user_model

# Create your views here.


class Ping(APIView):
    def get(self,request):
        return Response({"status":True})

class LoginView(APIView):
    def post(self, request):
        try:
            access_token = request.POST.get('token')
            parameters = {'access_token': access_token}
            access_token_url = "https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id={}&client_secret={}&fb_exchange_token={}".format(SOCIAL_AUTH_FACEBOOK_KEY, SOCIAL_AUTH_FACEBOOK_SECRET, access_token)
            r = requests.get(access_token_url)
            access_token_info = r.json()
            user_long_token = access_token_info['access_token']
            url = 'https://graph.facebook.com/me/'
            r = requests.get(url, params=parameters)
            results = r.json()
            name = results['name']
            userid = results['id']
            new_url = "https://graph.facebook.com/{0}?fields=name,email,picture&access_token={1}".format(userid,access_token)
            result_new = requests.get(new_url)
            results = result_new.json()
            profile_pic = results['picture']['data']['url']
            try:
                user_profile = models.Profile.objects.get(fb_id=userid)
                user = user_profile.user
            except:
                user = User.objects.create(username=userid)
                if 'email' in results:
                    user.email = results["email"]
                user.save()
                user_profile = models.Profile()
            user_profile.user = user
            user_profile.fb_id = userid
            user_profile.fb_token = user_long_token
            user_profile.profile_image = profile_pic
            user_profile.full_name = name
            user_profile.save()
            login(request, user)
            page_url = "https://graph.facebook.com/{}/accounts?fields=name,picture,access_token&access_token={}".format(user_profile.fb_id,user_long_token)
            r = requests.get(page_url)
            access_token_info = r.json()
            user_profile.pages.clear()
            for i in access_token_info["data"]:
                try:
                    page = models.Page.objects.get(page_id=i["id"])
                except:
                    page = models.Page()
                page.title = i["name"]
                page.page_id = i["id"]         
                page.access_token = i["access_token"]
                page.page_icon = i["picture"]["data"]["url"]
                page.save()
                user_profile.pages.add(page)
            try:
                Token.objects.get(user=user).delete()
            except:
                pass
            token, created = Token.objects.get_or_create(user=user)
            dat = {'token': token.key, 'user_id':user.id,"name":user_profile.full_name,"profile_pic":user_profile.profile_image}
            stat = status.HTTP_200_OK
        except Exception as e:
            dat = {'error': "error occured","error_details":str(e)}
            stat = status.HTTP_400_BAD_REQUEST
        return Response({"data":dat},status=stat)



class PassLoginView(APIView):
    def post(self, request):
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is None:
                dat = {'error': 'invalid login details'}
                stat = status.HTTP_400_BAD_REQUEST
            else:
                login(request, user)
                user_profile = models.Profile.objects.get(user=user)
                page_url = "https://graph.facebook.com/{}/accounts?fields=name,picture,access_token&access_token={}".format(user_profile.fb_id,user_profile.fb_token)
                r = requests.get(page_url)
                access_token_info = r.json()
                user_profile.pages.clear()
                for i in access_token_info["data"]:
                    try:
                        page = models.Page.objects.get(page_id=i["id"])
                    except:
                        page = models.Page()
                    page.title = i["name"]
                    page.page_id = i["id"]         
                    page.access_token = i["access_token"]
                    page.page_icon = i["picture"]["data"]["url"]
                    page.save()
                    user_profile.pages.add(page)
                try:
                    Token.objects.get(user=user).delete()
                except:
                    pass
                token, created = Token.objects.get_or_create(user=user)
                dat = {'token': token.key, 'user_id':user.id,"name":user_profile.full_name,"profile_pic":user_profile.profile_image}
                stat = status.HTTP_200_OK
        except Exception as e:
            dat = {'error': "error occured","error_details":str(e)}
            stat = status.HTTP_400_BAD_REQUEST
        return Response({"data":dat},status=stat)




class FBPages(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    def get(self, request, **kwargs):
        try:
            user_profile = models.Profile.objects.get(user=request.user)
            if "id" in kwargs:
                pages  = user_profile.pages.get(id=kwargs.get("id"))
                ser = serializers.PageSerializer(pages,many=False)
            else:
                pages  = user_profile.pages.all()
                ser = serializers.PageSerializer(pages,many=True)
            print(ser,'****')
            dat = ser.data
            stat = status.HTTP_200_OK
        except Exception as e:
            dat = {}
            dat["error"] = str(e)
            stat = status.HTTP_401_UNAUTHORIZED
        return Response({"data":dat},status=stat)

    def post(self, request, **kwargs):
        try:
            dat = {}
            user_profile = models.Profile.objects.get(user=request.user)
            if "id" in kwargs:
                page  = user_profile.pages.get(id=kwargs.get("id"))
                about = request.POST.get("about")
                email = request.POST.get("email")
                website = request.POST.get("website")
                phone = request.POST.get("phone")
                page_url = "https://graph.facebook.com/{}?about={}&access_token={}&website={}&phone={}".format(page.page_id,about,page.access_token,website,phone)
                r = requests.post(page_url)
                access_token_info = r.json()
                if "error" in access_token_info:
                    dat["error"] = access_token_info["error"]["message"]
                    stat = status.HTTP_400_BAD_REQUEST
                else:
                    dat["success"] = True
                    dat["data"] = access_token_info
                    stat = status.HTTP_200_OK
            else:
                dat["error"] = "Invalid action"
                stat = status.HTTP_401_UNAUTHORIZED
            
        except Exception as e:
            dat = {}
            dat["error"] = str(e)
            stat = status.HTTP_401_UNAUTHORIZED
        return Response({"data":dat},status=stat)
    


class Validate(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        return Response({"status":True})

