from django.shortcuts import render


def index(request):
    return render(request, "taskmanagerApp/index.html")