# Generated by Django 4.1 on 2023-04-21 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0003_alter_task_contribute_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='deadline',
            field=models.DateTimeField(),
        ),
    ]
