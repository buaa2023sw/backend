from django.db import models

class User(models.Model):
  id            = models.AutoField(primary_key=True)
  name          = models.CharField(max_length=255)
  email         = models.EmailField(unique=True)
  password      = models.CharField(max_length=255)
  STATUS_LIST = (
    ('A', 'NORMAL'),
    ('B', 'ILLEGAL'),
    ('C', 'ADMIN'),
  )
  status        = models.CharField(max_length=2, choices=STATUS_LIST)
  
class Project(models.Model):
  id            = models.AutoField(primary_key=True)
  create_time   = models.DateTimeField(auto_now_add=True)
  STATUS_LIST = (
    ('A', 'COMPLETED'),
    ('B', 'INPROGRESS'),
    ('C', 'NOTSTART'),
  )
  status        = models.CharField(max_length=2, choices=STATUS_LIST)
  name          = models.CharField(max_length=255)
  outline       = models.TextField()
  manager_id    = models.ForeignKey(User, on_delete=models.CASCADE)
  
class Task(models.Model):
  id            = models.AutoField(primary_key=True)
  name          = models.CharField(max_length=255)
  create_time   = models.DateTimeField(auto_now_add=True)
  deadline      = models.DateTimeField()
  outline       = models.TextField()
  STATUS_LIST = (
    ('A', 'COMPLETED'),
    ('B', 'INPROGRESS'),
    ('C', 'NOTSTART'),
  )
  status        = models.CharField(max_length=2, choices=STATUS_LIST)
  contribute_level = models.IntegerField()
  parent_id     = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
  project_id    = models.ForeignKey(Project, on_delete=models.CASCADE)
  
class Group(models.Model):
  id            = models.AutoField(primary_key=True)
  name          = models.CharField(max_length=255)
  outline       = models.TextField()
  project_id    = models.ForeignKey(Project, on_delete=models.CASCADE)
  
class Message(models.Model):
  id            = models.AutoField(primary_key=True)
  TYPE_LIST = (
    ('A', 'TEXT'),
    ('B', 'PIC'),
    ('C', 'FILE'),
  )
  type          = models.CharField(max_length=2, choices=TYPE_LIST)
  content       = models.CharField(max_length=255) # TODO use FILE
  group_id      = models.ForeignKey(Group, on_delete=models.CASCADE)
  user_id       = models.ForeignKey(User, on_delete=models.CASCADE)
  time          = models.DateTimeField(auto_now_add=True)
  
class Document(models.Model):
  id            = models.AutoField(primary_key=True)
  name          = models.CharField(max_length=255)
  outline       = models.TextField()
  content       = models.TextField()
  project_id    = models.ForeignKey(Project, on_delete=models.CASCADE)
  user_id       = models.ForeignKey(User, on_delete=models.CASCADE)
  
class Post(models.Model):
  id            = models.AutoField(primary_key=True)
  name          = models.CharField(max_length=255)
  content       = models.TextField()
  user_id       = models.ForeignKey(User, on_delete=models.CASCADE)
  project_id    = models.ForeignKey(Project, on_delete=models.CASCADE)

class Repo(models.Model):
  id            = models.AutoField(primary_key=True)
  name          = models.CharField(max_length=255)
  local_path    = models.CharField(max_length=255) # TODO
  remote_path   = models.CharField(max_length=255)
  
class Progress(models.Model):
  id            = models.AutoField(primary_key=True)
  name          = models.CharField(max_length=255)
  TYPE_LIST = (
    ('A', 'COMMIT'),
    ('B', 'ISSUE'),
    ('C', 'PR'),
  )
  type          = models.CharField(max_length=2, choices=TYPE_LIST)
  remote_path   = models.CharField(max_length=255)
  repo_id       = models.ForeignKey(Repo, on_delete=models.CASCADE)
  
class UserProject(models.Model):
  user_id       = models.ForeignKey(User, on_delete=models.CASCADE)
  project_id    = models.ForeignKey(Project, on_delete=models.CASCADE)
  ROLE_LIST = (
    ('A', 'NORMAL'),
    ('B', 'ADMIN'),
  )
  role          = models.CharField(max_length=2, choices=ROLE_LIST)
  
class UserGroup(models.Model):
  user_id       = models.ForeignKey(User, on_delete=models.CASCADE)
  group_id      = models.ForeignKey(Group, on_delete=models.CASCADE)
  ROLE_LIST = (
    ('A', 'NORMAL'),
    ('B', 'ADMIN'),
  )
  role          = models.CharField(max_length=2, choices=ROLE_LIST)
  
class UserTask(models.Model):
  user_id       = models.ForeignKey(User, on_delete=models.CASCADE)
  task_id       = models.ForeignKey(Task, on_delete=models.CASCADE)

class UserDocument(models.Model):
  user_id       = models.ForeignKey(User, on_delete=models.CASCADE)
  document_id   = models.ForeignKey(Document, on_delete=models.CASCADE)
  
class UserProjectRepo(models.Model):
  user_id       = models.ForeignKey(User, on_delete=models.CASCADE)
  project_id    = models.ForeignKey(Project, on_delete=models.CASCADE)
  repo_id       = models.ForeignKey(Repo, on_delete=models.CASCADE)
  
class ProgressTask(models.Model):
  repo_id       = models.ForeignKey(Repo, on_delete=models.CASCADE)
  progress_id   = models.ForeignKey(Progress, on_delete=models.CASCADE)

  