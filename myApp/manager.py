import struct

from django.http import JsonResponse, HttpResponse
from django.core import serializers

from myApp.models import *
from djangoProject.settings import DBG, USER_REPOS_DIR
import json
import os
import shutil
import sys
from myApp.userdevelop import genResponseStateInfo, genUnexpectedlyErrorInfo
import random


# TODO : add check manager function
def isAdmin(userId):
  try:
    status = User.objects.get(id=userId).status
    if status != User.ADMIN:
      return False
    return True
  except Exception as e:
    return False

def genRandStr(randLength=6):
  randStr = ''
  baseStr = 'ABCDEFGHIGKLMNOPORSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
  length = len(baseStr) - 1
  for i in range(randLength):
    randStr += baseStr[random.randint(0, length)]
  return randStr

def showUsers(request):
  DBG("---- in " + sys._getframe().f_code.co_name + " ----")
  response = {}
  genResponseStateInfo(response, 0, "get users ok")
  users = []
  managerId = request.POST.get('managerId')
  if not isAdmin(managerId):
    return JsonResponse(genResponseStateInfo(response, 1, "Insufficient authority"))
  allUsers = User.objects.all()
  for user in allUsers:
    users.append({"name" : user.name, "email" : user.email, 
                  "registerTime" : user.create_time, "status" : user.status})
    
  response["users"] = users
  return JsonResponse(response)

def changeUserStatus(request):
  DBG("---- in " + sys._getframe().f_code.co_name + " ----")
  response = {}
  genResponseStateInfo(response, 0, "change status ok")
  managerId = request.POST.get('managerId')
  if not isAdmin(managerId):
    return JsonResponse(genResponseStateInfo(response, 1, "Insufficient authority"))
  userId = request.POST.get('userId')
  changeToStatus = request.POST.get('changeToStatus')
  user = User.objects.get(id=userId)
  userName = user.name
  if user.status == changeToStatus:
    return JsonResponse(genResponseStateInfo(response, 2, "no need change"))
  user.status = changeToStatus
  user.save()
  response["name"] = userName
  return JsonResponse(response)

def resetUserPassword(request):
  DBG("---- in " + sys._getframe().f_code.co_name + " ----")
  response = {}
  genResponseStateInfo(response, 0, "reset password ok")
  managerId = request.POST.get('managerId')
  if not isAdmin(managerId):
    return JsonResponse(genResponseStateInfo(response, 1, "Insufficient authority"))
  userId = request.POST.get('userId')
  user = User.objects.get(id=userId)
  userName = user.name
  resetPassWord = genRandStr()
  user.password = resetPassWord
  user.save()
  response["name"] = userName
  response["resetPassword"] = resetPassWord
  return JsonResponse(response)

def showAllProjects(request):
  DBG("---- in " + sys._getframe().f_code.co_name + " ----")
  response = {}
  genResponseStateInfo(response, 0, "get projects ok")
  managerId = request.POST.get('managerId')
  if not isAdmin(managerId):
    return JsonResponse(genResponseStateInfo(response, 1, "Insufficient authority"))
  projects = []
  allProjects = Project.objects.all()
  for project in allProjects:
    leader = User.objects.get(id=project.manager_id.id)
    projects.append({"name" : project.name, "leader" : leader.name,
                     "email" : leader.email, "createTime" : project.create_time,
                     "progress" : project.progress, "status" : project.status})
  response["projects"] = projects
  return JsonResponse(response)

def changeProjectStatus(request):
  DBG("---- in " + sys._getframe().f_code.co_name + " ----")
  response = {}
  genResponseStateInfo(response, 0, "change status ok")
  managerId = request.POST.get('managerId')
  if not isAdmin(managerId):
    return JsonResponse(genResponseStateInfo(response, 1, "Insufficient authority"))
  projectId = request.POST.get('projectId')
  changeToStatus = request.POST.get('changeToStatus')
  project = Project.objects.get(id=projectId)
  projectName = project.name
  if project.status == changeToStatus:
    return JsonResponse(genResponseStateInfo(response, 2, "no need change"))
  project.status = changeToStatus
  project.save()
  response["name"] = projectName
  return JsonResponse(response)

def showUsersLogin(request):
  DBG("---- in " + sys._getframe().f_code.co_name + " ----")
  response = {}
  genResponseStateInfo(response, 0, "get login messages ok")
  managerId = request.POST.get('managerId')
  if not isAdmin(managerId):
    return JsonResponse(genResponseStateInfo(response, 1, "Insufficient authority"))
  loginMessages = []
  allUsers = User.objects.all()
  for user in allUsers:
    loginMessages.append({"name" : user.name, "email" : user.email, 
                          "loginTime" : user.last_login_time})
    
  response["loginMessages"] = loginMessages
  return JsonResponse(response)

def getUserNum(request):
  DBG("---- in " + sys._getframe().f_code.co_name + " ----")
  response = {}
  genResponseStateInfo(response, 0, "get users num ok")
  managerId = request.POST.get('managerId')
  if not isAdmin(managerId):
    return JsonResponse(genResponseStateInfo(response, 1, "Insufficient authority"))
  response["userSum"] = User.objects.count()
  return JsonResponse(response)

def getProjectNum(request):
  DBG("---- in " + sys._getframe().f_code.co_name + " ----")
  response = {}
  genResponseStateInfo(response, 0, "get projects num ok")
  managerId = request.POST.get('managerId')
  if not isAdmin(managerId):
    return JsonResponse(genResponseStateInfo(response, 1, "Insufficient authority"))
  response["projectSum"] = Project.objects.count()
  return JsonResponse(response)
  
def getProjectsScale(request):
  DBG("---- in " + sys._getframe().f_code.co_name + " ----")
  response = {}
  genResponseStateInfo(response, 0, "get numbers of different scale projects ok")
  managerId = request.POST.get('managerId')
  if not isAdmin(managerId):
    return JsonResponse(genResponseStateInfo(response, 1, "Insufficient authority"))
  tiny = 0
  small = 0
  medium = 0
  big = 0
  large = 0
  projects = Project.objects.all()
  for project in projects:
    usersNum = int(UserProject.objects.filter(project_id=project.id).count())
    if usersNum < 4:
      tiny = tiny + 1
    elif usersNum < 8:
      small = small + 1
    elif usersNum < 16:
      medium = medium + 1
    elif usersNum < 31:
      big = big + 1
    else:
      large = large + 1
  response["tiny"] = tiny
  response["small"] = small
  response["medium"] = medium
  response["big"] = big
  response["large"] = large
  return JsonResponse(response)