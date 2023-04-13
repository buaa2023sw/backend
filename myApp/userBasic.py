from myApp.models import User
from djangoProject.settings import response_json


# 返回给前端的 ErrorCode
Success = 0
Email_Duplicated = 2
Username_Duplicated = 3
None_Existed_User = 1
Password_Wrong = 2
Invalid_Status = 3
Modification_Failed = 1


# 返回给前端的信息
Register_Success_Message = '注册成功！'
Login_Success_Message = '登录成功！'
Email_Duplicated_Message = ''
Username_Duplicated_Message = 'nin'
None_Existed_User_Message = ''
Password_Wrong_Message = ''
Invalid_Status_Message = ''
Modification_Failed_Message = ''
Modification_Success_Message = '更改密码成功！'


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
    username, email = request.POST.get('username'), request.POST.get('email')
    print('yesyesyes')
    print(username, email)

    # Step 1. Check
    users = User.objects.filter(email=email)
    if not len(users) == 0:
        return response_json(
            errcode = Email_Duplicated,
            message = Email_Duplicated_Message
        )

    # Step 2. Check
    users = User.objects.filter(name=username)
    if len(users) == 0:
        return response_json(
            errcode = Username_Duplicated,
            message = Username_Duplicated_Message
        )

    # Step 3. Create
    u = User(name=username, password=request.POST.get('password'),
             email=email, status=User.NORMAL)
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
    # Step 1. Check
    user = User.objects.filter(name=request.POST.get('username'))
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
    if not user.password == request.POST.get('request'):
        return response_json(
            errcode = Password_Wrong,
            message = Password_Wrong_Message
        )

    # Step 4. Login & Session
    request.session['userId'] = user.id
    return response_json(
        errcode = Success,
        message = Login_Success_Message
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
            errcode = Modification_Failed,
            message = Modification_Failed_Message
        )

    if not user.password == request.POST.get('oldPassword'):
        return response_json(
            errcode = Modification_Failed,
            message = Modification_Failed_Message
        )

    try:
        user.password = request.POST.get('newPassword')
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
