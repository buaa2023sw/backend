"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
import os

from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from myApp import views as UserView

from django.urls import re_path
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('add_userInfo/', UserView.add_userInfo),
    path('search_userInfo/', UserView.search_userInfo),
    path('fetch_userInfo/', UserView.fetch_userInfo),
    path('edit_userInfo/', UserView.edit_userInfo),
    path('userId2userName/', UserView.userId2userName),
    path('search_usertype/', UserView.search_usertype),
    path('edit_password/', UserView.edit_password),


    re_path(r'^media/avatar/(?P<path>.*)$', serve, {'document_root': os.path.join(settings.MEDIA_ROOT,'avatar/')}),
    re_path(r'^media/user_avatar/(?P<path>.*)$', serve, {'document_root': os.path.join(settings.MEDIA_ROOT,'user_avatar/')}),
    re_path(r'^media/comments/(?P<path>.*)$', serve, {'document_root': os.path.join(settings.MEDIA_ROOT,'user_avatar/')}),

    #re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    path("",TemplateView.as_view(template_name="index.html"))
]
