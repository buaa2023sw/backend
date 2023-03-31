from django.core.management.base import CommandError, BaseCommand
from django.db import models
from django.db import connection
from myApp.models import *
from djangoProject.settings import DBG, USER_REPOS_DIR
import sys
import inspect

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
    for i in range(1, 11):
      name = "user" + str(i)
      email = "2037364" + str(i) + "@buaa.edu.cn"
      password = "2037364" + str(i)
      userListToInsert.append(User(name=name, email=email,
                                   password=password,status=User.NORMAL))
    User.objects.bulk_create(userListToInsert)
    
    
    projectListToInsert = list()
    for i in range(1, 11):
      name = "project" + str(i)
      outline = "this is project" + str(i)
      userInstance = User.objects.get(name="user" + str(i))
      projectListToInsert.append(Project(status=Project.INPROGRESS,name=name,
                                 outline=outline,manager_id=userInstance))
    Project.objects.bulk_create(projectListToInsert)
  
  def handle(self, *args, **options):
    self.clearDataBase()
    self.buildDataBase()
    
  