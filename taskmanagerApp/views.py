import re

from django.shortcuts import render
from django.shortcuts import redirect

def top(request):
    if request.POST:
        input_task = request.POST.get('input_task').split('\n')
        regex_pattern = r"^\d+\.\s*(.+?)\s*->\s+予定[:：]\s*(.+?)$"
        task_list = []
        for task in input_task:
            if task.strip():
                matches = re.match(regex_pattern, task.replace('\r',''))
                task_data = {
                    'written_task_txt': matches[0],
                    'task_name': matches[1],
                    'task_hour': matches[2],
                }
                task_list.append(task_data)
            else:
                print('マッチしてません')
        print(task_list)
        
        ctx = {
            'task_list': task_list,
        }
        return render(request, "taskmanagerApp/index.html", ctx)

    return render(request, "taskmanagerApp/index.html")

