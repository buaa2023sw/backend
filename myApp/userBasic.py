from myApp.models import User
from djangoProject.settings import response_json
import datetime
import json


# 返回给前端的 ErrorCode
Success = 0
Email_Duplicated = 2
Username_Duplicated = 3
None_Existed_User = 1
Password_Wrong = 2
Invalid_Status = 3
Modification_Failed = 1


# 返回给前端的信息
Register_Success_Message = 'register ok'
Login_Success_Message = 'login ok'
Email_Duplicated_Message = 'email duplicated'
Username_Duplicated_Message = 'username duplicated'
None_Existed_User_Message = 'no user or email'
Password_Wrong_Message = 'error password'
Invalid_Status_Message = 'error status'
Modification_Failed_Message = 'fail to change'
Modification_Success_Message = 'change password ok'


def testtesttest(request):
    return response_json(
        errcode = 0,
        message = 'this is test')


def register(request):
    """
        register api,
        1. check whether have duplicated username.
        2. check whether have duplicated email.
    """
    kwargs: dict = json.loads(request.body)
    username, email = kwargs.get('username'), kwargs.get('email')

    # Step 1. Check
    users = User.objects.filter(email=email)
    if not len(users) == 0:
        return response_json(
            errcode = Email_Duplicated,
            message = Email_Duplicated_Message
        )

    # Step 2. Check
    users = User.objects.filter(name=username)
    if not len(users) == 0:
        return response_json(
            errcode = Username_Duplicated,
            message = Username_Duplicated_Message
        )

    # Step 3. Create
    u = User(name=username, password=kwargs.get('password'),
             email=email, status=User.NORMAL,
             create_time=datetime.datetime.now(),
             last_login_time=datetime.datetime.now())
    u.save()
    return response_json(
        errcode = Success,
        message = Register_Success_Message
    )


def login(request):
    """
        login api:
        1. Get specific user according to `username`.
        2. Check whether the user has limit.
        2. Check password correct.
    """
    kwargs: dict = json.loads(request.body)
    # Step 1. Check
    user = User.objects.filter(name=kwargs.get('userNameOrEmail'))
    if len(user) == 0:
        user = User.objects.filter(email=kwargs.get('userNameOrEmail'))
        if len(user) == 0:
            return response_json(
                errcode = None_Existed_User,
                message = None_Existed_User_Message
            )

    # Step 2. Check
    user = user.first()
    if user.status == User.ILLEGAL:
        return response_json(
            errcode = Invalid_Status,
            message = Invalid_Status_Message
        )

    # Step 3. Check
    if not user.password == kwargs.get('password'):
        return response_json(
            errcode = Password_Wrong,
            message = Password_Wrong_Message
        )

    # Step 4. Login & Session
    request.session['userId'] = user.id
    projects = [{ 'id': p.id, 'name': p.name } for p in user.project_set.all()]
    return response_json(
        errcode = Success,
        message = Login_Success_Message,
        data = {
            'status': user.status,
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'projects': projects
        }
    )


def modify_password(request):
    """
        modify password api
        0. Check Authentication.
        1. Check whether there exists target user, according to `id`.
        2. Check user password correct, according to `oldPassword`.
        3. Modification.
    """
    kwargs: dict = json.loads(request.body)
    # Step 0. Check, todo
    # Step 1. Check
    user = User.objects.get(id=int(kwargs.get('userId')))
    if user is None:
        return response_json(
            errcode = Modification_Failed,
            message = Modification_Failed_Message
        )

    if not user.password == kwargs.get('oldPassword'):
        return response_json(
            errcode = Modification_Failed,
            message = Modification_Failed_Message
        )

    try:
        user.password = kwargs.get('newPassword')
        user.save()
        return response_json(
            errcode = Success,
            message = Modification_Success_Message
        )
    except Exception as exp:
        return response_json(
            errcode = Modification_Failed,
            message = Modification_Failed_Message
        )