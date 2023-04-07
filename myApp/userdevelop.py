import struct

from django.http import JsonResponse, HttpResponse
from django.core import serializers

from myApp.models import *
from djangoProject.settings import DBG, USER_REPOS_DIR, BASE_DIR
import json
import os
import shutil
import sys
import subprocess
import json5

def isProjectExists(projectId):
  try:
    project = Project.objects.get(id=projectId)
    return project
  except Exception as e:
    return None

def isUserInProject(userId, projectId):
  try:
    userProject = UserProject.objects.get(user_id=userId,project_id=projectId)
    return userProject
  except Exception as e:
    return None
  
def genUnexpectedlyErrorInfo(response, e):
  response["errcode"] = -1
  response['message'] = "unexpectedly error : " + str(e)
  return response

def genResponseStateInfo(response, errcode, message):
  response["errcode"] = errcode
  response['message'] = message
  return response

def getProjectName(request):
  DBG("---- in " + sys._getframe().f_code.co_name + " ----")
  response = {}
  genResponseStateInfo(response, 0, "get project name ok")
  response["data"] = {}
  response["data"]["name"] = ""
  userId = request.POST.get('userId')
  projectId = request.POST.get('projectId')
  project = isProjectExists(projectId)
  if project == None:
    return JsonResponse(genResponseStateInfo(response, 1, "project does not exists"))
  userProject = isUserInProject(userId, projectId)
  if userProject == None:
    return JsonResponse(genResponseStateInfo(response, 2, "user not in project"))
  
  response["data"]["name"] = project.name
  return JsonResponse(response)

def getBindRepos(request):
  DBG("---- in " + sys._getframe().f_code.co_name + " ----")
  response = {}
  genResponseStateInfo(response, 0, "get bind repos ok")
  response["data"] = []
  userId = request.POST.get('userId')
  projectId = request.POST.get('projectId')
  project = isProjectExists(projectId)
  if project == None:
    return JsonResponse(genResponseStateInfo(response, 1, "project does not exists"))
  userProject = isUserInProject(userId, projectId)
  if userProject == None:
    return JsonResponse(genResponseStateInfo(response, 2, "user not in project"))
  
  try:
    userProjectRepos = UserProjectRepo.objects.filter(user_id=userId,project_id=projectId)
    for userProjectRepo in userProjectRepos:
      repoId = userProjectRepo.repo_id.id
      repo = Repo.objects.get(id=repoId)
      response["data"].append({"repoId" : repoId, 
                              "repoRemotePath" : repo.remote_path,
                              "repoIntroduction" : repo.name})
  except Exception as e:
    return JsonResponse(genUnexpectedlyErrorInfo(response, e))
  
  return JsonResponse(response)

def userBindRepo(request):
    DBG("---- in " + sys._getframe().f_code.co_name + " ----")
    response = {}
    genResponseStateInfo(response, 0, "bind ok")
    userId = request.POST.get('userId')
    projectId = request.POST.get('projectId')
    repoRemotePath = request.POST.get('repoRemotePath')
    DBG("userId=" + userId + " projectId=" + projectId + " repoRemotePath=" + repoRemotePath)
    project = isProjectExists(projectId)
    if project == None:
      return JsonResponse(genResponseStateInfo(response, 1, "project does not exists"))
    userProject = isUserInProject(userId, projectId)
    if userProject == None:
      return JsonResponse(genResponseStateInfo(response, 2, "user not in project"))
    # check if repo exists
    try:
      localHasRepo = False
      s = Repo.objects.filter(remote_path=repoRemotePath)
      if len(s) != 0:
        localHasRepo = True
        repoId = s[0].id
        userProjectRepo = UserProjectRepo.objects.filter(user_id=userId, project_id=projectId, repo_id=repoId)
        if len(userProjectRepo) != 0:
          return JsonResponse(genResponseStateInfo(response, 4, "duplicate repo"))
      # clone & repo
      repoName = repoRemotePath.split("/")[-1]
      localPath = os.path.join(USER_REPOS_DIR, repoName)
      DBG("repoName=" + repoName, " localPath=" + localPath)
      if localHasRepo == False:
        # if dir exists, just remove it
        if os.path.exists(localPath):
          shutil.rmtree(localPath)
        # clone the repo
        r = os.system("gh repo clone " + repoRemotePath + " " + localPath)
        if r != 0:
          return JsonResponse(genResponseStateInfo(response, 5, "clone repo fail"))
      # insert Repo
      repo = None
      s = Repo.objects.filter(remote_path=repoRemotePath)
      if len(s) != 0:
        repo = s[0]
      else:
        repoEntry = Repo(name=repoName, local_path=localPath, remote_path=repoRemotePath)
        repoEntry.save()
        # insert UserProjectRepo
        repo = Repo.objects.get(name=repoName, local_path=localPath, remote_path=repoRemotePath)
      user = User.objects.get(id=userId)
      project = Project.objects.get(id=projectId)
      userProjectRepoEntry = UserProjectRepo(user_id=user, project_id=project, repo_id=repo)
      userProjectRepoEntry.save()
    except Exception as e:
      return JsonResponse(genUnexpectedlyErrorInfo(response, e))
    
    return JsonResponse(response)
  
  
def userUnbindRepo(request):
  DBG("---- in " + sys._getframe().f_code.co_name + " ----")
  response = {}
  genResponseStateInfo(response, 0, "unbind ok")
  userId = request.POST.get('userId')
  projectId = request.POST.get('projectId')
  repoId = request.POST.get('repoId')
  project = isProjectExists(projectId)
  if project == None:
    return JsonResponse(genResponseStateInfo(response, 1, "project does not exists"))
  userProject = isUserInProject(userId, projectId)
  if userProject == None:
    return JsonResponse(genResponseStateInfo(response, 2, "user not in project"))
  
  if not UserProjectRepo.objects.filter(user_id=userId, project_id=projectId, repo_id=repoId).exists():
    return JsonResponse(genResponseStateInfo(response, 3, "no such repo in project that bind by this user"))
  
  try:
    userProjectRepo = UserProjectRepo.objects.get(user_id=userId, project_id=projectId, repo_id=repoId)
    userProjectRepo.delete()
  except Exception as e:
    return JsonResponse(genUnexpectedlyErrorInfo(response, e))
  
  return JsonResponse(response)
  
def getRepoBranches(request):
  DBG("---- in " + sys._getframe().f_code.co_name + " ----")
  response = {}
  genResponseStateInfo(response, 0, "get branches ok")
  userId = request.POST.get('userId')
  projectId = request.POST.get('projectId')
  repoId = request.POST.get('repoId')
  project = isProjectExists(projectId)
  if project == None:
    return JsonResponse(genResponseStateInfo(response, 1, "project does not exists"))
  userProject = isUserInProject(userId, projectId)
  if userProject == None:
    return JsonResponse(genResponseStateInfo(response, 2, "user not in project"))
  
  if not UserProjectRepo.objects.filter(user_id=userId, project_id=projectId, repo_id=repoId).exists():
    return JsonResponse(genResponseStateInfo(response, 3, "no such repo in project that bind by this user"))
  
  data = []
  try:
    log = "getRepoBranches.log"
    remotePath = Repo.objects.get(id=repoId).remote_path
    os.system("gh api -H \"Accept: application/vnd.github+json\" -H \
              \"X-GitHub-Api-Version: 2022-11-28\" /repos/" + remotePath + "/branches > " + os.path.join(USER_REPOS_DIR, log))
    ghInfo = json.load(open(os.path.join(USER_REPOS_DIR, log), encoding="utf-8"))
    for it in ghInfo:
      data.append({"branchName" : it["name"]})
    response["data"] = data
  except Exception as e:
    return genUnexpectedlyErrorInfo(response, e)
  return JsonResponse(response)

def getCommitHistory(request):
  DBG("---- in " + sys._getframe().f_code.co_name + " ----")
  response = {}
  genResponseStateInfo(response, 0, "get commit history ok")
  userId = request.POST.get('userId')
  projectId = request.POST.get('projectId')
  repoId = request.POST.get('repoId')
  branchName = request.POST.get('branchName')
  project = isProjectExists(projectId)
  if project == None:
    return JsonResponse(genResponseStateInfo(response, 1, "project does not exists"))
  userProject = isUserInProject(userId, projectId)
  if userProject == None:
    return JsonResponse(genResponseStateInfo(response, 2, "user not in project"))
  
  if not UserProjectRepo.objects.filter(user_id=userId, project_id=projectId, repo_id=repoId).exists():
    return JsonResponse(genResponseStateInfo(response, 3, "no such repo in project that bind by this user"))
  
  data = []
  try:
    log = "getCommitHistory.log"
    localPath = Repo.objects.get(id=repoId).local_path
    os.system("cd " + localPath + " git checkout " + branchName + " && git pull")
    cmd = "cd " + localPath + " && bash " + os.path.join(BASE_DIR, "myApp/get_commits.sh") + " > " + os.path.join(USER_REPOS_DIR, log)
    os.system(cmd)
    ghInfo = json5.load(open(os.path.join(USER_REPOS_DIR, log), encoding="utf-8"))
    response["data"] = ghInfo
  except Exception as e:
    return genUnexpectedlyErrorInfo(response, e)
  return JsonResponse(response)

def getIssueList(request):
  DBG("---- in " + sys._getframe().f_code.co_name + " ----")
  response = {}
  genResponseStateInfo(response, 0, "get issue list ok")
  userId = request.POST.get('userId')
  projectId = request.POST.get('projectId')
  repoId = request.POST.get('repoId')
  project = isProjectExists(projectId)
  if project == None:
    return JsonResponse(genResponseStateInfo(response, 1, "project does not exists"))
  userProject = isUserInProject(userId, projectId)
  if userProject == None:
    return JsonResponse(genResponseStateInfo(response, 2, "user not in project"))
  
  if not UserProjectRepo.objects.filter(user_id=userId, project_id=projectId, repo_id=repoId).exists():
    return JsonResponse(genResponseStateInfo(response, 3, "no such repo in project that bind by this user"))
  
  data = []
  try:
    log = "getIssueList.log"
    remotePath = Repo.objects.get(id=repoId).remote_path
    os.system("gh api -H \"Accept: application/vnd.github+json\" -H \
              \"X-GitHub-Api-Version: 2022-11-28\" /repos/" + remotePath + "/issues > " + os.path.join(USER_REPOS_DIR, log))
    ghInfo = json.load(open(os.path.join(USER_REPOS_DIR, log), encoding="utf-8"))
    for it in ghInfo:
      data.append({"issuer" : it["user"]["login"],
                   "issueTitle" : it["title"],
                   "issueTime" : it["updated_at"],
                   "isOpen" : it["state"] == "open",
                   "ghLink" : it["html_url"]})
    response["data"] = data
  except Exception as e:
    return genUnexpectedlyErrorInfo(response, e)
  return JsonResponse(response)