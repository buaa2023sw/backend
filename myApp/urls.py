from django.urls import path, include
from myApp import userBasic

urlpatterns = [
    path('test', userBasic.testtesttest),
    path('register', userBasic.register),
    path('login', userBasic.login),
    path('user/information/password', userBasic.modify_password),
]
