import re

from django.shortcuts import render
from django.shortcuts import redirect


def top(request):
    # print("aq")
    if request.POST:
        input_task = request.POST.get('input_task').split('\n')
        regex_pattern = r"^\d+\.\s*(\[.+?\]\s*.+?)\s*->\s+予定[:：]\s*(.+?)$"
        task_list = []
        for task in input_task:
            if task.strip():
                print('入力されました')
                # matches = re.match(regex_pattern, task)
                # task_data = {
                #     'task_name': matches[0],
                #     'task_hour': matches[1],
                # }
                # task_list.append(task_data)
            else:
                print('マッチしてません')
        # for task in task_list:
    return render(request, "taskmanagerApp/index.html")

