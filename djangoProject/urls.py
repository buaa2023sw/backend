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

from myApp import userdevelop, manager, userBasic, userPlan, debug
from myApp import notice
from django.urls import re_path
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/userBindRepo', userdevelop.UserBindRepo.as_view()),
    path('api/management/showUsers', manager.ShowUsers.as_view()),
    path('api/management/showAdmins', manager.ShowAdmins.as_view()),
    path('api/management/changeUserStatus', manager.ChangeUserStatus.as_view()),
    path('api/management/resetUserPassword', manager.ResetUserPassword.as_view()),
    path('api/management/showAllProjects', manager.ShowAllProjects.as_view()),
    path('api/management/changeProjectStatus', manager.ChangeProjectStatus.as_view()),
    path('api/management/changeProjectAccess', manager.ChangeProjectAccess.as_view()),
    path('api/management/showUsersLogin', manager.ShowUsersLogin.as_view()),
    path('api/management/getUserNum', manager.GetUserNum.as_view()),
    path('api/management/getProjectNum', manager.GetProjectNum.as_view()),
    path('api/management/getProjectsScale', manager.GetProjectScale.as_view()),
    path('api/develop/getProjectName', userdevelop.GetProjectName.as_view()),
    path('api/develop/getBindRepos', userdevelop.GetBindRepos.as_view()),
    path('api/develop/userBindRepo', userdevelop.UserBindRepo.as_view()),
    path('api/develop/userUnbindRepo', userdevelop.UserUnbindRepo.as_view()),
    path('api/develop/getRepoBranches', userdevelop.GetRepoBranches.as_view()),
    path('api/develop/getCommitHistory', userdevelop.GetCommitHistory.as_view()),
    path('api/develop/getIssueList', userdevelop.GetIssueList.as_view()),
    path('api/develop/getPrList', userdevelop.GetPrList.as_view()),
    path('api/register', userBasic.register),
    path('api/login', userBasic.login),
    path('api/user/information/password', userBasic.modify_password),
    path('api/showProfile', userBasic.show),
    path('api/editProfile', userBasic.modify_information),
    path('api/plan/newProject', userPlan.newProject.as_view()),
    path('api/plan/watchAllProject', userPlan.watchAllProject.as_view()),
    path('api/plan/addTask', userPlan.addTask.as_view()),
    path('api/plan/addSubTask', userPlan.addSubTask.as_view()),
    path('api/plan/showTaskList', userPlan.showTaskList.as_view()),
    path('api/plan/modifyTaskContent', userPlan.modifyTaskContent.as_view()),
    path('api/plan/showPersonList', userPlan.showPersonList.as_view()),
    path('api/plan/modifyRole', userPlan.modifyRole.as_view()),
    path('api/plan/addMember', userPlan.addMember.as_view()),
    path('api/plan/removeMember', userPlan.removeMember.as_view()),
    path('api/plan/deleteProject', userPlan.deleteProject.as_view()),
    path('api/plan/modifyProject', userPlan.modifyProject.as_view()),
    path('api/plan/completeTask', userPlan.completeTask.as_view()),
    path('api/plan/notice', userPlan.notice.as_view()),
    path('api/plan/watchMyTask', userPlan.watchMyTask.as_view()),
    path('api/plan/test', userPlan.test.as_view()),
    path('api/plan/removeTask', userPlan.removeTask.as_view()),
    path('api/plan/modifyProjectStatus', userPlan.modifyProjectStatus.as_view()),
    path('api/plan/showNoticeList', userPlan.showNoticeList.as_view()),
    path('api/plan/modifyNotice', userPlan.modifyNotice.as_view()),
    path('api/plan/removeNotice', userPlan.removeNotice.as_view()),
    path('api/echo', debug.echo),
    path('api/notice/userPostNoticeToAll', notice.UserPostNoticeToAll.as_view()),
    path('api/notice/userPostNoticeToOne', notice.UserPostNoticeToOne.as_view()),
    path('api/notice/sysPostNoticeInProject', notice.SysPostNoticeInProject.as_view()),
    path('api/notice/sysPostNoticeToAll', notice.SysPostNoticeToAll.as_view()),
    path('api/notice/userGetNotice', notice.UserGetNotice.as_view()),
    path('api/notice/userConfirmNotice', notice.UserConfirmNotice.as_view()),
    path('api/plan/getEmail', userPlan.getEmail.as_view())
]
