from myApp.models import Group
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

