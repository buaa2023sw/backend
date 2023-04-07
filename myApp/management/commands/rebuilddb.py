from django.core.management.base import CommandError, BaseCommand
from django.db import models
from django.db import connection
from myApp.models import *
from djangoProject.settings import DBG, USER_REPOS_DIR
import sys
import inspect
import datetime

class Command(BaseCommand):
  help = "delete all data in db and insert some data"
  
  def clearDataBase(self):
    "delete all data in database"
    print("begin build data base")
    tables = inspect.getmembers(sys.modules[__name__], inspect.isclass)
    cursor = connection.cursor() 
    cursor.execute('SET foreign_key_checks = 0')
    # for t in tables:
    #   try:
    #     eval(str(t[0]) + ".objects.all().delete()")
    #     # cursor.execute('update sqlite_sequence set seq=0 where name=' + eval(str(t[0]) + "._meta.db_table"))
    #   except Exception as e:
    #     print(e)
    for t in tables:
      try:
        cursor.execute('TRUNCATE TABLE {0}'.format(eval(str(t[0])+"._meta.db_table")))
      except Exception as e:
        print(e)
    cursor.execute('SET foreign_key_checks = 1')
    
        
  def buildDataBase(self):
    "insert some data in data base"
    print("begin build data base")
    userListToInsert = list()
    User(name="admin1",email="admin@buaa.edu.cn",password="111111",
         last_login_time=datetime.datetime.today(),status=User.ADMIN).save()
    for i in range(2, 11):
      name = "user" + str(i)
      email = "2037364" + str(i) + "@buaa.edu.cn"
      password = "2037364" + str(i)
      userListToInsert.append(User(name=name, email=email,
                                   password=password,status=User.NORMAL
                                   ,last_login_time=datetime.datetime.today()))
    User.objects.bulk_create(userListToInsert)
    
    
    projectListToInsert = list()
    for i in range(2, 11):
      name = "project" + str(i)
      outline = "this is project" + str(i)
      userInstance = User.objects.get(name="user" + str(i))
      projectListToInsert.append(Project(status=Project.INPROGRESS,name=name,
                                 outline=outline,manager_id=userInstance,progress=str(i)))
    Project.objects.bulk_create(projectListToInsert)
    
    userProjectlist = list()
    for i in range(2, 11):
      user = User.objects.get(id=str(i))
      project = Project.objects.get(id=str(i - 1))
      userProjectlist.append(UserProject(user_id=user, project_id=project))
    UserProject.objects.bulk_create(userProjectlist)
    
    Repo(name="repo1",local_path="repo1_local_path",remote_path="repo1_remote_path").save()
    UserProjectRepo(user_id=User.objects.get(id=2),project_id=Project.objects.get(id=1),repo_id=Repo.objects.get(id=1)).save()
  
  def handle(self, *args, **options):
    # self.clearDataBase()
    self.buildDataBase()
    
  