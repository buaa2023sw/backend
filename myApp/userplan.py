from django.http import JsonResponse
from django.core import serializers

from myApp.models import *
from django.views import View
import json
import datetime


class newProject(View):
    def post(self, request):
        response = {'success': False, 'message': "404 not success"}

        try:
            kwargs: dict = json.loads(request.body)
        except Exception:
            return JsonResponse(response)

        projectName = kwargs.get("projectName")
        projectIntro = kwargs.get("projectIntro")

        userId = request.POST.get('userId')
        if User.objects.filter(id=userId).count() == 0:
            response['errcode'] = 1
            response['message'] = "user not exist"
            response['data'] = None
            return JsonResponse(response)
        project = Project.objects.create(name=projectName, outline=projectIntro, manager_id=userId, status='C')
        project.save()
        # NORMAL = 'A'
        #  ADMIN = 'B'
        #  ROLE_LIST = (
        #    (NORMAL, 'NORMAL'),
        #    (ADMIN, 'ADMIN'),
        #  )
        #  role          = models.CharField(max_length=2, choices=ROLE_LIST)
        UserProject.objects.create(user_id=userId, project_id=project.id, role=UserProject.ADMIN)
        response['errcode'] = 0
        response['message'] = "success"
        response['data'] = None
        return JsonResponse(response)


class watchAllProject(View):
    def get(self, request):
        response = {'errcode': 0, 'success': False, 'message': "404 not success"}
        userProjectRepo = UserProject.objects.filter(user_id=request.user)
        projectList = []
        for i in userProjectRepo:
            projectList.append({
                "id": i.project_id.id,
                "name": i.project_id.name,
                "outline": i.project_id.outline,
                "status": i.project_id.status,
                "time": [i.project_id.create_time.year, i.project_id.create_time.month, i.project_id.create_time.day],
                "manageId": i.project_id.manager_id.id,
            })
        response['errcode'] = 0
        response['message'] = "success"
        response['data'] = projectList
        return JsonResponse(response)


class addTask(View):
    def post(self, request):
        response = {'errcode': 0, 'success': False, 'message': "404 not success"}
        try:
            kwargs: dict = json.loads(request.body)
        except Exception:
            return JsonResponse(response)
        #### 添加任务
        # * parameter format
        # *`time`：int数组[year, month, day]
        # *`contribute`：int
        # *`people`：int数组[id1, id2, ...]
        #

        time = kwargs.get("time", [1999, 1, 1])
        contribute = kwargs.get("contribute", 0)
        people = kwargs.get("people", [])
        name = kwargs.get("name", "")
        projectId = kwargs.get("projectId", 0)
        if Project.objects.filter(id=projectId).count() == 0:
            response['errcode'] = 1
            response['message'] = "project not exist"
            response['data'] = None
            return JsonResponse(response)
        for i in people:
            if User.objects.filter(id=i).count() == 0:
                response['errcode'] = 1
                response['message'] = "user not exist"
                response['data'] = None
                return JsonResponse(response)
        # use time[0] as year time[1] as month time[2] as day
        deadline = datetime.datetime(year=time[0], month=time[1], day=time[2])
        task = Task.objects.create(name=name, deadline=deadline, contribute=contribute, project_id=projectId)
        task.status = Task.NOTSTART
        task.save()
        for i in people:
            UserTask.objects.create(user_id=i, task_id=task.id)
        response['errcode'] = 0
        response['message'] = "success"
        response['data'] = None
        return JsonResponse(response)


class addSubTask(View):
    def post(self, request):
        response = {'errcode': 0, 'success': False, 'message': "404 not success"}
        try:
            kwargs: dict = json.loads(request.body)
        except Exception:
            return JsonResponse(response)
        time = kwargs.get("time", [1999, 1, 1])
        contribute = kwargs.get("contribute", 0)
        people = kwargs.get("people", [])
        name = kwargs.get("name", "")
        projectId = kwargs.get("projectId", -1)
        belongTask = kwargs.get("belongTask", -1)
        if Project.objects.filter(id=projectId).count() == 0:
            response['errcode'] = 1
            response['message'] = "project not exist"
            response['data'] = None
            return JsonResponse(response)
        for i in people:
            if User.objects.filter(id=i).count() == 0:
                response['errcode'] = 1
                response['message'] = "user not exist"
                response['data'] = None
                return JsonResponse(response)
        # use time[0] as year time[1] as month time[2] as day
        deadline = datetime.datetime(year=time[0], month=time[1], day=time[2])
        task = Task.objects.create(name=name, deadline=deadline, contribute=contribute, project_id=projectId,
                                   parent_id=belongTask)

        task.status = Task.NOTSTART
        task.save()
        for i in people:
            UserTask.objects.create(user_id=i, task_id=task.id)
        response['errcode'] = 0
        response['message'] = "success"
        response['data'] = None
        return JsonResponse(response)


def showTaskList(View):
    def post(self, request):
        response = {'errcode': 0, 'success': False, 'message': "404 not success"}
        try:
            kwargs: dict = json.loads(request.body)
        except Exception:
            return JsonResponse(response)
        projectId = kwargs.get("projectId", -1)
        if Project.objects.filter(id=projectId).count() == 0:
            response['errcode'] = 1
            response['message'] = "project not exist"
            response['data'] = None
            return JsonResponse(response)
        taskList = Task.objects.filter(project_id=projectId)
        taskList = serializers.serialize("json", taskList)
        print(taskList)
        # TODO: testsub Task
        response['errcode'] = 0
        response['message'] = "success"
        response['data'] = taskList
        return JsonResponse(response)


def modifyTaskContent(View):
    def post(self, request):
        response = {'errcode': 0, 'success': False, 'message': "404 not success"}
        try:
            kwargs: dict = json.loads(request.body)
        except Exception:
            return JsonResponse(response)
        taskId = kwargs.get("taskId", -1)
        if Task.objects.filter(id=taskId).count() == 0:
            response['errcode'] = 1
            response['message'] = "task not exist"
            response['data'] = None
            return JsonResponse(response)
        task = Task.objects.get(id=taskId)
        key = kwargs.get("key", "")
        if "value" not in kwargs:
            response['errcode'] = 1
            response['message'] = "value not exist"
            response['data'] = None
            return JsonResponse(response)
        value = kwargs.get("value", "")
        if key == "name":
            task.name = value
        elif key == "contribute":
            task.contribute = value
        elif key == "deadline":
            task.deadline = datetime.datetime(year=value[0], month=value[1], day=value[2])
        elif key == "status":
            task.status = value
        else:
            response['errcode'] = 1
            response['message'] = "key not exist"
            response['data'] = None
            return JsonResponse(response)
        task.save()
        return JsonResponse(response)


def showPersonList(View):
    def post(self, request):
        response = {'errcode': 0, 'success': False, 'message': "404 not success"}
        try:
            kwargs: dict = json.loads(request.body)
        except Exception:
            return JsonResponse(response)
        projectId = kwargs.get("projectId", -1)
        if Project.objects.filter(id=projectId).count() == 0:
            response['errcode'] = 1
            response['message'] = "project not exist"
            response['data'] = None
            return JsonResponse(response)
        personList = UserProject.objects.filter(project_id=projectId)
        res = []
        for person in personList:
            res.append({
                "peopleID": person.user_id,
                "peopleName": person.user_id.username,
                "peopleJob": person.role

            })
        response['errcode'] = 0
        response['message'] = "success"
        response['data'] = res
        return JsonResponse(response)


def modifyRole(View):
    def post(self, request):
        response = {'errcode': 0, 'success': False, 'message': "404 not success"}
        try:
            kwargs: dict = json.loads(request.body)
        except Exception:
            return JsonResponse(response)
        projectId = kwargs.get("projectId", -1)
        if Project.objects.filter(id=projectId).count() == 0:
            response['errcode'] = 1
            response['message'] = "project not exist"
            response['data'] = None
            return JsonResponse(response)
        peopleId = kwargs.get("peopleId", -1)
        if User.objects.filter(id=peopleId).count() == 0:
            response['errcode'] = 1
            response['message'] = "user not exist"
            response['data'] = None
            return JsonResponse(response)
        role = kwargs.get("role", "")
        if role not in [UserProject.ADMIN, UserProject.NORMAL]:
            response['errcode'] = 1
            response['message'] = "role not exist"
            response['data'] = None
            return JsonResponse(response)
        userProject = UserProject.objects.get(user_id=peopleId, project_id=projectId)
        userProject.role = role
        userProject.save()
        response['errcode'] = 0
        response['message'] = "success"
        response['data'] = None
        return JsonResponse(response)


def addMember(View):
    def post(self, request):
        response = {'errcode': 0, 'success': False, 'message': "404 not success"}
        try:
            kwargs: dict = json.loads(request.body)
        except Exception:
            return JsonResponse(response)
        projectId = kwargs.get("projectId", -1)
        if Project.objects.filter(id=projectId).count() == 0:
            response['errcode'] = 1
            response['message'] = "project not exist"
            response['data'] = None
            return JsonResponse(response)
        peopleId = kwargs.get("peopleId", -1)
        if User.objects.filter(id=peopleId).count() == 0:
            response['errcode'] = 1
            response['message'] = "user not exist"
            response['data'] = None
            return JsonResponse(response)
        if UserProject.objects.filter(user_id=peopleId, project_id=projectId).count() != 0:
            response['errcode'] = 1
            response['message'] = "user already in project"
            response['data'] = None
            return JsonResponse(response)
        UserProject.objects.create(user_id=peopleId, project_id=projectId, role=UserProject.NORMAL)


def removeMember(View):
    def post(self, request):
        response = {'errcode': 0, 'success': False, 'message': "404 not success"}
        try:
            kwargs: dict = json.loads(request.body)
        except Exception:
            return JsonResponse(response)
        projectId = kwargs.get("projectId", -1)
        if Project.objects.filter(id=projectId).count() == 0:
            response['errcode'] = 1
            response['message'] = "project not exist"
            response['data'] = None
            return JsonResponse(response)
        peopleId = kwargs.get("peopleId", -1)
        if User.objects.filter(id=peopleId).count() == 0:
            response['errcode'] = 1
            response['message'] = "user not exist"
            response['data'] = None
            return JsonResponse(response)
        if UserProject.objects.filter(user_id=peopleId, project_id=projectId).count() == 0:
            response['errcode'] = 1
            response['message'] = "user not in project"
            response['data'] = None
            return JsonResponse(response)
        UserProject.objects.filter(user_id=peopleId, project_id=projectId).delete()
        response['errcode'] = 0
        response['message'] = "success"
        response['data'] = None
        return JsonResponse(response)


class deleteProject(View):
    def post(self, request):
        response = {'errcode': 0, 'success': False, 'message': "404 not success"}
        try:
            kwargs: dict = json.loads(request.body)
        except Exception:
            return JsonResponse(response)
        projectId = kwargs.get("projectId", -1)
        if Project.objects.filter(id=projectId).count() == 0:
            response['errcode'] = 1
            response['message'] = "project not exist"
            response['data'] = None
            return JsonResponse(response)
        Project.objects.filter(id=projectId).delete()
        response['errcode'] = 0
        response['message'] = "success"
        response['data'] = None
        return JsonResponse(response)


class modifyProject(View):
    def post(self, request):
        response = {'errcode': 0, 'success': False, 'message': "404 not success"}
        try:
            kwargs: dict = json.loads(request.body)
        except Exception:
            return JsonResponse(response)
        projectId = kwargs.get("projectId", -1)
        if Project.objects.filter(id=projectId).count() == 0:
            response['errcode'] = 1
            response['message'] = "project not exist"
            response['data'] = None
            return JsonResponse(response)
        projectName = kwargs.get("name", "")
        if projectName != "":
            project = Project.objects.get(id=projectId)
            project.name = projectName
            project.save()
        projectOutline = kwargs.get("outline", "")
        if projectOutline != "":
            project = Project.objects.get(id=projectId)
            project.outline = projectOutline
            project.save()
        response['errcode'] = 0
        response['message'] = "success"
        response['data'] = None
        return JsonResponse(response)
