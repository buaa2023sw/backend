import struct

from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.views import View
from myApp.models import *
from djangoProject.settings import DBG, USER_REPOS_DIR, BASE_DIR
import json
import os
import shutil
import sys
import subprocess
import json5
from myApp.userdevelop import *


def userDocListTemplate(userId, projectId, table):
  DBG("---- in " + sys._getframe().f_code.co_name + " ----")
  response = {'message': "get userDocListTemplate ok", "errcode": 0}
  project = isProjectExists(projectId)
  if project == None:
    return genResponseStateInfo(response, 1, "project does not exists")
  userProject = isUserInProject(userId, projectId)
  if userProject == None:
    return genResponseStateInfo(response, 2, "user not in project")
  data = []
  userAccessEntries = table.objects.filter(user_id=userId)
  for userAccess in userAccessEntries:
    docEntry = Document.objects.get(id=userAccess.doc_id.id)
    ownerName = User.objects.get(id=docEntry.user_id.id).name
    data.append({"id" : docEntry.id, 
                 "name" : docEntry.name, 
                 "ownerName" : ownerName,
                 "updateTime" : docEntry.time,
                 "outline" : docEntry.outline,
                 "content" : docEntry.content})
  response["data"] = data
  return response
    
class UserDocList(View):
  def post(self, request):
    response = {'message': "404 not success", "errcode": -1}
    try:
      kwargs: dict = json.loads(request.body)
    except Exception:
      return JsonResponse(response)
    try:
      response = userDocListTemplate(kwargs.get('userId'), kwargs.get('projectId'), UserAccessDoc)
    except Exception as e:
      return JsonResponse({'message': str(e), "errcode": -1}) 
    return JsonResponse(response)

class UserCollectDocList(View):
  def post(self, request):
    response = {'message': "404 not success", "errcode": -1}
    try:
      kwargs: dict = json.loads(request.body)
    except Exception:
      return JsonResponse(response)
    try:
      response = userDocListTemplate(kwargs.get('userId'), kwargs.get('projectId'), UserCollectDoc)
    except Exception as e:
      return JsonResponse({'message': "error in logic func", "errcode": -1}) 
    return JsonResponse(response)

def addDocToCollect(userId, projectId, docId):
  DBG("---- in " + sys._getframe().f_code.co_name + " ----")
  response = {'message': "get addDocToCollect ok", "errcode": 0}
  project = isProjectExists(projectId)
  if project == None:
    return genResponseStateInfo(response, 1, "project does not exists")
  userProject = isUserInProject(userId, projectId)
  if userProject == None:
    return genResponseStateInfo(response, 2, "user not in project")
  docprev = UserCollectDoc.objects.filter(user_id=User.objects.get(id=userId), 
                 doc_id=Document.objects.get(id=docId))
  if len(docprev) > 0:
    return genResponseStateInfo(response, 3, "doc already in collect")
  UserCollectDoc(user_id=User.objects.get(id=userId), 
                 doc_id=Document.objects.get(id=docId)).save()
  return response

class AddDocToCollect(View):
  def post(self, request):
    response = {'message': "404 not success", "errcode": -1}
    try:
      kwargs: dict = json.loads(request.body)
    except Exception:
      return JsonResponse(response)
    try:
      response = addDocToCollect(kwargs.get('userId'), 
                                 kwargs.get('projectId'), kwargs.get('docId'))
    except Exception as e:
      return JsonResponse({'message': "error in logic func", "errcode": -1}) 
    return JsonResponse(response)
  
def delDocFromCollect(userId, projectId, docId):
  DBG("---- in " + sys._getframe().f_code.co_name + " ----")
  response = {'message': "get delDocFromCollect ok", "errcode": 0}
  project = isProjectExists(projectId)
  if project == None:
    return genResponseStateInfo(response, 1, "project does not exists")
  userProject = isUserInProject(userId, projectId)
  if userProject == None:
    return genResponseStateInfo(response, 2, "user not in project")
  UserCollectDoc.objects.filter(user_id=userId, doc_id=docId).delete()
  return response

class DelDocFromCollect(View):
  def post(self, request):
    response = {'message': "404 not success", "errcode": -1}
    try:
      kwargs: dict = json.loads(request.body)
    except Exception:
      return JsonResponse(response)
    try:
      response = delDocFromCollect(kwargs.get('userId'), 
                                 kwargs.get('projectId'), kwargs.get('docId'))
    except Exception as e:
      return JsonResponse({'message': "error in logic func", "errcode": -1}) 
    return JsonResponse(response)
  
def userCreateDoc(userId, projectId, name, outline, content, accessUserId):
  DBG("---- in " + sys._getframe().f_code.co_name + " ----")
  DBG("#"+str(userId)+"#"+str(projectId)+"#"+str(name)+"#"+str(accessUserId))
  response = {'message': "get userCreateDoc ok", "errcode": 0}
  project = isProjectExists(projectId)
  if project == None:
    return genResponseStateInfo(response, 1, "project does not exists")
  userProject = isUserInProject(userId, projectId)
  if userProject == None:
    return genResponseStateInfo(response, 2, "user not in project")
  prevDoc = Document.objects.filter(name=name, project_id=projectId)
  if len(prevDoc) > 0:
    return genResponseStateInfo(response, 3, "duplicate doc")
  user = User.objects.get(id=userId)
  Document(name=name, outline=outline, content=content, project_id=project, 
           user_id=user).save()
  doc = Document.objects.get(name=name,project_id=projectId, user_id=userId)
  for item in accessUserId:
    accessUser = User.objects.get(id=item)
    UserAccessDoc(user_id=accessUser, doc_id=doc).save()
  return response

class UserCreateDoc(View):
  def post(self, request):
    response = {'message': "404 not success", "errcode": -1}
    try:
      kwargs: dict = json.loads(request.body)
    except Exception:
      return JsonResponse(response)
    try:
      response = userCreateDoc(kwargs.get('userId'), 
                                 kwargs.get('projectId'), kwargs.get('name'),
                                 kwargs.get('outline'), kwargs.get('content'),
                                 kwargs.get('accessUserId'))
    except Exception as e:
      return JsonResponse({'message': str(e), "errcode": -1}) 
    return JsonResponse(response)

def userEditDoc(userId, projectId, name, outline, content, accessUserId):
  DBG("---- in " + sys._getframe().f_code.co_name + " ----")
  response = {'message': "get userEditDoc ok", "errcode": 0}
  project = isProjectExists(projectId)
  if project == None:
    return genResponseStateInfo(response, 1, "project does not exists")
  userProject = isUserInProject(userId, projectId)
  if userProject == None:
    return genResponseStateInfo(response, 2, "user not in project")
  Document.objects.filter(name=name, project_id=projectId).update(
    outline=outline, content=content, time=datetime.datetime.now()
  )
  doc = Document.objects.get(name=name, project_id=projectId)
  for item in accessUserId:
    accessUser = User.objects.get(id=item)
    UserAccessDoc.objects.get_or_create(user_id=accessUser, doc_id=doc)
  return response

class UserEditDoc(View):
  def post(self, request):
    response = {'message': "404 not success", "errcode": -1}
    try:
      kwargs: dict = json.loads(request.body)
    except Exception:
      return JsonResponse(response)
    try:
      response = userEditDoc(kwargs.get('userId'), 
                                 kwargs.get('projectId'), kwargs.get('name'),
                                 kwargs.get('outline'), kwargs.get('content'),
                                 kwargs.get('accessUserId'))
    except Exception as e:
      return JsonResponse({'message': str(e), "errcode": -1}) 
    return JsonResponse(response)

def userDelDoc(userId, projectId, docId):
  DBG("---- in " + sys._getframe().f_code.co_name + " ----")
  response = {'message': "get userDelDoc ok", "errcode": 0}
  project = isProjectExists(projectId)
  if project == None:
    return genResponseStateInfo(response, 1, "project does not exists")
  userProject = isUserInProject(userId, projectId)
  if userProject == None:
    return genResponseStateInfo(response, 2, "user not in project")
  Document.objects.filter(id=docId).delete()
  return response

class UserDelDoc(View):
  def post(self, request):
    response = {'message': "404 not success", "errcode": -1}
    try:
      kwargs: dict = json.loads(request.body)
    except Exception:
      return JsonResponse(response)
    try:
      response = userDelDoc(kwargs.get('userId'), 
                                 kwargs.get('projectId'), kwargs.get('docId'))
    except Exception as e:
      return JsonResponse({'message': "error in logic func", "errcode": -1}) 
    return JsonResponse(response)

def docTimeUpdate(userId, projectId, docId, updateTime):
  DBG("---- in " + sys._getframe().f_code.co_name + " ----")
  response = {'message': "get docTimeUpdate ok", "errcode": 0}
  project = isProjectExists(projectId)
  if project == None:
    return genResponseStateInfo(response, 1, "project does not exists")
  userProject = isUserInProject(userId, projectId)
  if userProject == None:
    return genResponseStateInfo(response, 2, "user not in project")
  Document.objects.filter(id=docId).update(time=updateTime)
  return response

class DocTimeUpdate(View):
  def post(self, request):
    response = {'message': "404 not success", "errcode": -1}
    try:
      kwargs: dict = json.loads(request.body)
    except Exception:
      return JsonResponse(response)
    try:
      response = userDelDoc(kwargs.get('userId'), 
                                 kwargs.get('projectId'), kwargs.get('docId'),
                                 kwargs.get('updateTime'))
    except Exception as e:
      return JsonResponse({'message': "error in logic func", "errcode": -1}) 
    return JsonResponse(response)
  