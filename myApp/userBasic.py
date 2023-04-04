from enum import Enum

from djangoProject.settings import response_json
from myApp.models import User

class UserBasicErrCode(Enum):
    Success = 0
    Email_Duplicated = 2
    Username_Duplicated = 3
    None_Existed_User = 1
    Password_Wrong = 2
    Invalid_Status = 3
    Modification_Failed = 1

class UserBasicMessage(Enum):
    Register_Success = '注册成功！'
    Login_Success = '登录成功！'
    Email_Duplicated = ''
    Username_Duplicated = ''
    None_Existed_User = ''
    Password_Wrong = ''
    Invalid_Status = ''
    Modification_Failed = ''
    Modification_Success = '更改密码成功！'


def register(request):
    """
        register api,
        1. check whether have duplicated username.
        2. check whether have duplicated email.
    """
    username, email = request.POST.get('username'), request.POST.get('email')

    # Step 1. Check
    users = User.objects.filter(email=email)
    if len(users) == 0:
        return response_json(
            errcode = UserBasicErrCode.Email_Duplicated,
            message = UserBasicMessage.Email_Duplicated
        )

    # Step 2. Check
    users = User.objects.filter(name=username)
    if len(users) == 0:
        return response_json(
            errcode = UserBasicErrCode.Username_Duplicated,
            message = UserBasicMessage.Username_Duplicated
        )

    # Step 3. Create
    u = User(name=username, password=request.POST.get('password'),
             email=email, status=User.NORMAL)
    u.save()
    return response_json(
        errcode = UserBasicErrCode.Success,
        message = UserBasicMessage.Register_Success
    )


def login(request):
    """
        login api:
        1. Get specific user according to `username`.
        2. Check whether the user has limit.
        2. Check password correct.
    """
    # Step 1. Check
    user = User.objects.filter(name=request.POST.get('username'))
    if len(user) == 0:
        return response_json(
            errcode = UserBasicErrCode.None_Existed_User,
            message = UserBasicMessage.None_Existed_User
        )

    # Step 2. Check
    user = user.first()
    if user.status == User.ILLEGAL:
        return response_json(
            errcode = UserBasicErrCode.Invalid_Status,
            message = UserBasicMessage.Invalid_Status
        )

    # Step 3. Check
    if not user.password == request.POST.get('request'):
        return response_json(
            errcode = UserBasicErrCode.Password_Wrong,
            message = UserBasicMessage.Password_Wrong
        )

    # Step 4. Login & Session
    request.session['userId'] = user.id
    return response_json(
        errcode = UserBasicErrCode.Success,
        message = UserBasicMessage.Login_Success
    )


def modify_password(request):
    """
        modify password api
        0. Check Authentication.
        1. Check whether there exists target user, according to `id`.
        2. Check user password correct, according to `oldPassword`.
        3. Modification.
    """
    # Step 0. Check, todo
    # Step 1. Check
    user = User.objects.get(id=int(request.POST.get('userId')))
    if user is None:
        return response_json(
            errcode = UserBasicErrCode.Modification_Failed,
            message = UserBasicMessage.Modification_Failed
        )

    if not user.password == request.POST.get('oldPassword'):
        return response_json(
            errcode = UserBasicErrCode.Modification_Failed,
            message = UserBasicMessage.Modification_Failed
        )

    try:
        user.password = request.POST.get('newPassword')
        user.save()
        return response_json(
            errcode = UserBasicErrCode.Success,
            message = UserBasicMessage.Modification_Success
        )
    except Exception as exp:
        return response_json(
            errcode = UserBasicErrCode.Modification_Failed,
            message = UserBasicMessage.Modification_Failed
        )
