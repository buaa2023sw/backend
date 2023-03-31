import struct

from django.http import JsonResponse, HttpResponse
from django.core import serializers

from myApp.models import *
from djangoProject.settings import DBG, USER_REPOS_DIR
import json
import os
import shutil
import sys


def userBindRepo(request):
    DBG("---- in " + sys._getframe().f_code.co_name + " ----")
    response = {}
    response['success'] = False
    response['message'] = "success"
    userId = request.POST.get('userId')
    projectId = request.POST.get('projectId')
    repoRemotePath = request.POST.get('repoRemotePath')
    DBG("userId=" + userId + " projectId=" + projectId + " repoRemotePath=" + repoRemotePath)
    # check if repo exists
    s = Repo.objects.filter(remote_path=repoRemotePath)
    if len(s) != 0:
      response['message'] = "repo already exists"
      return JsonResponse(response)
    
    # clone & repo
    repoName = repoRemotePath.split("/")[-1]
    localPath = os.path.join(USER_REPOS_DIR, repoName)
    DBG("repoName=" + repoName, " localPath=" + localPath)
    # if dir exists, just remove it
    if os.path.exists(localPath):
      shutil.rmtree(localPath)
    # clone the repo
    r = os.system("gh repo clone " + repoRemotePath + " " + localPath)
    if r != 0:
      response['message'] = "clone repo fail"
      return JsonResponse(response)
  
    try:
      # insert Repo
      repoEntry = Repo(name=repoName, local_path=localPath, remote_path=repoRemotePath)
      repoEntry.save()
    # insert UserProjectRepo
      repo = Repo.objects.get(name=repoName, local_path=localPath, remote_path=repoRemotePath)
      user = User.objects.get(id=userId)
      project = Project.objects.get(id=projectId)
      userProjectRepoEntry = UserProjectRepo(user_id=user, project_id=project, repo_id=repo)
      userProjectRepoEntry.save()
    except Exception as e:
      response['message'] = str(e)
      return JsonResponse(response)
    
    response['success'] = True
    return JsonResponse(response)