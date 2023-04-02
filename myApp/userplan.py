from django.http import JsonResponse
from django.core import serializers

from myApp.models import *
from django.views import View
import json


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
        project = Project.objects.create(name=projectName, outline=projectIntro, manager_id=userId, status='C')
        project.save()

        response['success'] = True
        response['message'] = "success"
        return JsonResponse(response)


class watchAllProject(View):
    def get(self, request):
        response = {'success': False, 'message': "404 not success"}
        userId = request.GET.get('userId')
        user = User.objects.get(id=userId)
        userProjectRepo = Project.objects.filter(user_id=user)
        projectList = []
        for i in userProjectRepo:
            projectList.append([i.name, i.status, i.create_time, i.manager_id, i.outline])
        response['success'] = True
        response['message'] = "success"
        response['projectList'] = serializers.serialize('json', projectList)
        return JsonResponse(response)
