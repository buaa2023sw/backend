from myApp.models import *
from djangoProject.settings import response_json
import datetime
import json

SUCCESS = 0

def get_room_content(request):
    kwargs: dict = json.loads(request.body)

    roomId = int(kwargs.get('roomId'))
    group = Group.objects.get(id = roomId)

    messages = [
        {
            'content': message.content,
            'senderName': message.send_user.name,
            'senderId': message.send_user.id,
            'time': message.time
        } for message in group.message_set
    ]

    return response_json(
        errcode = SUCCESS,
        data = messages
    )


def get_user_public_groups(request):
    kwargs: dict = json.loads(request.body)

    projectId = int(kwargs.get('projectId'))
    userId = int(request.session['userId'])

    discussions = []
    for association in UserGroup.objects.filter(user = userId):
        group = Group.objects.get(id = association.group)
        if group.type == 'PUB' and group.project_id == projectId:
            discussions.append({
                'roomId': group.id,
                'roomName': group.name,
                'outline': group.outline
            })

    return response_json(
        errcode = SUCCESS,
        data = {
            'discussions': discussions
        }
    )


def get_user_private_groups(request):
    kwargs: dict = json.loads(request.body)

    projectId = int(kwargs.get('projectId'))
    userId = int(request.session['userId'])

    privates = []
    for association in UserGroup.objects.filter(user = userId):
        group = Group.objects.get(id = association.group)
        if group.type == 'PRI' and group.project_id == projectId:
            privates.append({
                'roomId': group.id,
                'roomName': group.name,
                'outline': group.outline
            })

    return response_json(
        errcode = SUCCESS,
        data = {
            'privates': privates
        }
    )


def create_public_group(request):
    kwargs: dict = json.loads(request.body)
    project = Project.objects.get(id=kwargs.get('projectId'))
    group = Group(
        name = kwargs.get('roomName'),
        outline = kwargs.get('outline'),
        project_id = project,
        type = 'PUB'
    )
    group.save()

    association = UserGroup(
        user = int(kwargs.get('currentUserId')),
        group = group.id,
        role = 'A'
    )
    association.save()

    for user_info in kwargs.get('users'):
        association = UserGroup(
            user = int(user_info['userId']),
            group = group.id,
            role = 'A'
        )
        association.save()

    return response_json(
        errcode = SUCCESS,
        data = {
            'roomId': group.id,
        }
    )


def create_private_group(request):
    kwargs: dict = json.loads(request.body)

    group = Group(
        name = kwargs.get('roomName'),
        outline = kwargs.get('outline'),
        project_id = int(kwargs.get('projectId')),
        type = 'PRI'
    )
    group.save()

    association = UserGroup(
        user = int(kwargs.get('currentUserId')),
        group = group.id,
        role = 'A'
    )
    association.save()

    association = UserGroup(
        user = int(kwargs.get('UserId')),
        group = group.id,
        role = 'A'
    )
    association.save()

    return response_json(
        errcode=SUCCESS,
        data={
            'roomId': group.id,
        }
    )


def add_user_to_group(request):
    kwargs: dict = json.loads(request.body)

