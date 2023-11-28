import re
import json
import math
from datetime import datetime
import hashlib

from django.shortcuts import render
from django.shortcuts import redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Tasks, Users
from .form import LoginForm, UserResisterForm
from .decorator import login_check


def login(request):
    # form.pyで作ったフォームをインスタンス化
    form = LoginForm(request.POST or None)
    # POST送信
    if request.method == 'POST':
        # validation
        if form.is_valid():
            # ログインされたuser情報を取得
            user = Users.objects.get(email=form.cleaned_data.get('email'))
            # sessionにuser情報を保存
            request.session['user_id'] = user.id
            request.session['name'] = user.user_name
            # urls.pyのname='index'を参照しredirect
            return redirect('top')
    context = {
        "form": form
    }
    return render(request, 'taskmanagerApp/login.html', context)


# logout
def logout(request):
    # sessionのuser_idとuser_emailの保存値を削除
    del request.session['user_id']
    del request.session['name']
    # urls.pyのname = 'login'を参照しredirect
    return redirect('login')


def register(request):
    # form.pyで作ったフォームをインスタンス化

    # 確認画面から戻った際に入力値を初期値として入れる
    session_values = {
        'user_name': request.session.get('name'),
        'email': request.session.get('email'),
        'password': request.session.get('password'),
    }
    form = UserResisterForm(initial_values=session_values)

    if request.method == 'POST':
        form = UserResisterForm(request.POST or None)
        # validation
        if form.is_valid():
            # 入力値を取得
            request.session['name'] = form.cleaned_data['name']
            request.session['email'] = form.cleaned_data['email']
            request.session['password'] = form.cleaned_data['password']
            request.session['conf_password'] = form.cleaned_data['conf_password']
            # register_confへ
            return redirect('register_conf')
    context = {"form": form}
    return render(request, 'taskmanagerApp/register.html', context)


# register_conf
def register_conf(request):
    # sessionへ保存されたデータ取得
    name = request.session.get('name')
    email = request.session.get('email')
    password = request.session.get('password')
    conf_password = request.session.get('conf_password')
    # ただURLが叩かれただけ（sessionに保存無し
    if not email or not password or not conf_password:
        return redirect('register')
    # POST送信
    if request.method == 'POST':
        if 'register' in request.POST:
            now = datetime.now()
            # 登録処理
            # passwordをハッシュ値に変換 hexdigest()は16進法に変換 encode()は文字列を文字コードに変換
            hs_password = hashlib.md5(password.encode()).hexdigest()
            # Userクラスをインスタンス化
            user = Users()
            # 各データをカラムへレコードとしてinsert
            user.name = name
            user.email = email
            user.password = hs_password
            user.password_update = now
            # save() でDBへ保存
            user.save()
            # comp画面へ遷移
            return render(request, 'taskmanagerApp/comp.html')
    # templateへ値を渡す
    context = {
        'name': name,
        'email': email,
        'password': password,
        'conf_password': conf_password
    }
    return render(request, 'taskmanagerApp/register-conf.html', context)


@login_check
def top(request):
    name = request.session.get('name')

    return render(request, "taskmanagerApp/index.html", {'name': name})


@login_check
def confirm_today_task(request):
    today_tasks = ""
    if request.method == 'POST':
        if 'confirm' in request.POST:
            input_tasks = request.POST.get("input_task")
            all_task_data_json = request.POST.get("all_task_data")

            # all_task_dataがNoneでないことを確認してからJSONとして読み込む
            all_task_data = json.loads(all_task_data_json) if all_task_data_json else {}

            # 実績の追加表示
            today_tasks = ""
            for task in input_tasks.split('\n'):
                if task.strip():
                    # 入力値の整形
                    task_format = task.replace('\n', "").replace('\r', "")
                    _, _, task_achievement_hour = task_formatting(task, all_task_data)

                    # localStorage ではタスク名で保存してあるからここでタスク名で各実績値をだして表示
                    task_achievement = f"{task_format}　実績：{task_achievement_hour}h"
                    today_tasks += task_achievement + '\n'
            # 余分な改行を除去
            today_tasks = today_tasks.rstrip('\n')

        # 登録処理
        if 'register' in request.POST:
            input_tasks = request.POST.get("input_task")
            all_task_data_json = request.POST.get("all_task_data")

            # all_task_dataがNoneでないことを確認してからJSONとして読み込む
            all_task_data = json.loads(all_task_data_json) if all_task_data_json else {}

            # 今日の日付取得
            now = datetime.now()
            today = now.strftime('%Y-%m-%d')

            # 登録するデータリスト
            insert_data_list = []

            try:
                # タスクデータの整形
                for task in input_tasks.split('\n'):
                    if task.strip():
                        task_name, task_plan_hour, task_achievement_hour = task_formatting(task, all_task_data, True)
                        # 各タスクと実績をデータリストへ追加
                        insert_data_list.append(
                            Tasks(
                                task_name=task_name,
                                task_plan_time=task_plan_hour,
                                task_end_time=task_achievement_hour,
                                task_date=today,
                                f_user_id_id=request.session.get('user_id')
                            )
                        )
                # リストをDBへ一括登録
                Tasks.objects.bulk_create(insert_data_list)
                print("データが登録されました。")
            except Exception:
                raise

            return redirect("my-page")
    ctx = {
        "today_tasks": today_tasks,
    }
    return render(request, "taskmanagerApp/confirm.html", ctx)


def my_page(request):
    # ユーザ情報取得
    user_id = request.session.get('user_id')
    user = Users.objects.filter(id=user_id).first()

    result = None
    message = None
    search_date = None
    if 'search' in request.GET:
        search_date = request.GET.get('datapicker')
        result = []

        if search_date:
            result = Tasks.objects.filter(task_date=search_date)
        else:
            message = "その日の業務データは登録されていません"

    ctx = {
        'user': user,
        'results': result,
        'message': message,
        'search_date': search_date,
    }
    return render(request, "taskmanagerApp/my-page.html", ctx)


# タスクを整形する関数
def task_formatting(task, all_task_data, confirm_flag=False):
    task = task.replace('\r', "").replace('\n', "")
    if confirm_flag:
        regex_task = r"^\d+\.\s*(.+?)\s*->\s*予定\s*[:：]\s*(.+?)[hｈ](.+?)$"
    else:
        regex_task = r"^\d+\.\s*(.+?)\s*->\s*予定\s*[:：]\s*(.+?)[hｈ]$"
    matches = re.match(regex_task, task)

    # タスクの名前を取得
    task_name = matches[1]
    task_plan_hour = matches[2]
    if task_name:
        task_name_hour_float = float(all_task_data[f"{task_name}"])
    else:
        task_name_hour_float = 0

    # 実績時間を整形
    task_achievement_hour = convert_to_hours(int(task_name_hour_float))
    task_plan_hour = float(task_plan_hour)

    return task_name, task_plan_hour, task_achievement_hour


# 秒を時間表記に変換する処理（近い値に合わせる）
def convert_to_hours(seconds):
    # 秒を時間に変換して小数点第2位まで表示
    hours = round(seconds / 3600, 2)

    # 最も近い方の表示に合わせる（0.25, 0.5, 0.75, 1.0の4分母に分数にする）
    rounded_hours_up = math.ceil(hours * 4) / 4
    rounded_hours_down = math.ceil(hours * 4) / 4

    # 小数点以下2桁まで表示
    rounded_hours_up = round(rounded_hours_up, 2)
    rounded_hours_down = round(rounded_hours_down, 2)

    # 最も近い方の表記を選択
    if abs(rounded_hours_up - hours) < abs(rounded_hours_down - hours):
        return rounded_hours_up
    else:
        return rounded_hours_down




