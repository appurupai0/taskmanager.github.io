from django.db import models


class Users(models.Model):
    user_name = models.CharField(
        verbose_name="ユーザー名",
        max_length=60
    )
    email = models.EmailField(
        verbose_name="メール",
        max_length=120
    )
    password = models.CharField(
        verbose_name="パスワード",
        max_length=100
    )
    password_update = models.DateTimeField(
        verbose_name="パスワード変更日"
    )

    # class Meta:
    #     db_table = 'users'


class Tasks(models.Model):
    task_name = models.CharField(
        verbose_name="タスク名",
        max_length=60
    )
    task_plan_time = models.DecimalField(
        verbose_name="タスク予定時間",
        max_digits=4,
        decimal_places=2
    )
    task_end_time = models.DecimalField(
        verbose_name="タスク終了時間",
        max_digits=4,
        decimal_places=2
    )
    task_date = models.DateField(
        verbose_name="タスク日時"
    )
    f_user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    delete_flag = models.BooleanField(
        verbose_name="削除フラグ",
        default=0
    )


class Messages(models.Model):
    message = models.CharField(
        verbose_name="メッセージ",
        max_length=60
    )

