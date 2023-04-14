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

from myApp import userdevelop, manager, userBasic, userplan

from django.urls import re_path
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/userBindRepo', userdevelop.userBindRepo),
    path('api/management/showUsers', manager.showUsers),
    path('api/management/changeUserStatus', manager.changeUserStatus),
    path('api/management/resetUserPassword', manager.resetUserPassword),
    path('api/management/showAllProjects', manager.showAllProjects),
    path('api/management/changeProjectStatus', manager.changeProjectStatus),
    path('api/management/showUsersLogin', manager.showUsersLogin),
    path('api/management/getUserNum', manager.getUserNum),
    path('api/management/getProjectNum', manager.getProjectNum),
    path('api/management/getProjectsScale', manager.getProjectsScale),
    path('api/develop/getProjectName', userdevelop.getProjectName),
    path('api/develop/getBindRepos', userdevelop.getBindRepos),
    path('api/develop/userBindRepo', userdevelop.userBindRepo),
    path('api/develop/userUnbindRepo', userdevelop.userUnbindRepo),
    path('api/develop/getRepoBranches', userdevelop.getRepoBranches),
    path('api/develop/getCommitHistory', userdevelop.getCommitHistory),
    path('api/develop/getIssueList', userdevelop.getIssueList),
    path('api/develop/getPrList', userdevelop.getPrList),
    path('api/register', userBasic.register),
    path('api/login', userBasic.login),
    path('api/user/information/password', userBasic.modify_password),
    path('api/plan/newProject', userplan.newProject.as_view()),
    path('api/plan/watchAllProject', userplan.watchAllProject.as_view()),
    path('api/plan/addTask', userplan.addTask.as_view()),
    path('api/plan/addSubTask', userplan.addSubTask.as_view()),
    path('api/plan/showTaskList', userplan.showTaskList.as_view()),
    path('api/plan/modifyTaskContent', userplan.modifyTaskContent.as_view()),
    path('api/plan/showPersonList', userplan.showPersonList.as_view()),
    path('api/plan/modifyRole', userplan.modifyRole.as_view()),
    path('api/plan/addMember', userplan.addMember.as_view()),
    path('api/plan/removeMember', userplan.removeMember.as_view()),
    path('api/plan/deleteProject', userplan.deleteProject.as_view()),
    path('api/plan/modifyProject', userplan.modifyProject.as_view()),
]
