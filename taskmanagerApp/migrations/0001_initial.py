# Generated by Django 4.2.3 on 2023-11-27 19:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=60, verbose_name='メッセージ')),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=60, verbose_name='ユーザー名')),
                ('email', models.EmailField(max_length=120, verbose_name='メール')),
                ('password', models.CharField(max_length=18, verbose_name='パスワード')),
                ('password_update', models.DateTimeField(verbose_name='パスワード変更日')),
            ],
        ),
        migrations.CreateModel(
            name='Tasks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_name', models.CharField(max_length=60, verbose_name='タスク名')),
                ('task_plan_time', models.DecimalField(decimal_places=2, max_digits=4, verbose_name='タスク予定時間')),
                ('task_end_time', models.DecimalField(decimal_places=2, max_digits=4, verbose_name='タスク終了時間')),
                ('task_date', models.DateField(verbose_name='タスク日時')),
                ('delete_flag', models.BooleanField(default=0, verbose_name='削除フラグ')),
                ('f_user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='taskmanagerApp.users')),
            ],
        ),
    ]
