# Generated by Django 3.2.6 on 2021-08-10 17:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appuser', '0003_load_defauly_policies'),
        ('appcalendar', '0004_auto_20210810_0059'),
    ]

    operations = [
        migrations.AddField(
            model_name='goal',
            name='appuser',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='appuser.appuser'),
            preserve_default=False,
        ),
    ]
