"""FBM URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    path('ping/',views.Ping.as_view()),
    path('login/',views.LoginView.as_view()),
    path('pass-login/',views.PassLoginView.as_view()),
    path('pages/',views.FBPages.as_view()),
    path('pages/<int:id>/',views.FBPages.as_view()),
    path('validate/',views.Validate.as_view()),
    
]
