from django.db import models


class UserInfo(models.Model):
    user_name = models.CharField(max_length=64,unique=True)
    user_password = models.CharField(max_length=64)

    user_type = models.CharField(max_length=10,null=True)

    user_address = models.CharField(max_length=64,null=True)
    user_mobile = models.CharField(max_length=64, null=True)
    user_avatar = models.ImageField(upload_to="user_avatar/",null=True,default="user_avatar/default_avatar.jpg")
    user_createtime = models.DateField(auto_now_add=True,null=True)

    user_province = models.CharField(max_length=16,null=True)
    user_city = models.CharField(max_length=16, null=True)
    user_area = models.CharField(max_length=16, null=True)


class UserLog(models.Model):
    log_id = models.ForeignKey("UserInfo", on_delete=models.CASCADE)
    log_time = models.DateTimeField(auto_now_add=True)
    log_name=models.CharField(max_length=16)
    log_type=models.CharField(max_length=10,null=True)

    log_province = models.CharField(max_length=16, null=True)
    log_city = models.CharField(max_length=16, null=True)
    log_area = models.CharField(max_length=16, null=True)
