# Generated by Django 4.2.3 on 2023-11-28 01:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskmanagerApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='password',
            field=models.CharField(max_length=100, verbose_name='パスワード'),
        ),
    ]
