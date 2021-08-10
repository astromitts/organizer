# Generated by Django 3.2.6 on 2021-08-10 00:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appcalendar', '0002_goal_rolled_over'),
    ]

    operations = [
        migrations.AddField(
            model_name='goal',
            name='status',
            field=models.CharField(choices=[('todo', 'To Do'), ('inprogress', 'In Progress'), ('doing', 'Doing'), ('done', 'Done'), ('archived', 'Archived')], default='todo', max_length=20),
        ),
        migrations.AddField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('todo', 'To Do'), ('inprogress', 'In Progress'), ('doing', 'Doing'), ('done', 'Done'), ('archived', 'Archived')], default='todo', max_length=20),
        ),
    ]
