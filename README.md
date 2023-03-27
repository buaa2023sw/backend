# 后端开发

## 添加数据库 SSL 证书

将证书放在 djangoProject 文件夹下

## 更新数据库表
如果更改了数据库表，需要在项目根目录下执行：
- python manage.py makemigrations
- python manage.py migrate

如果数据库提示表已存在或字段已存在错误，请删库并重新建库。(数据库名为 develop1 )

## api 开发
- 在 myApp/views.py 中添加视图函数
- 在 djangoProject/urls.py 中添加视图函数 url
- 在 myApp/tests.py 中写单元测试

## 运行后端项目：
项目根目录下执行：
- python manage.py runserver