from django.shortcuts import render
from django.http import HttpResponse
from app1 import models
from django.core.files.base import ContentFile


# Create your views here.
def index(request):
    return render(request, "ManageIndex.html")


def user_list(request):
    return render(request, "user.html")


def user_list(request):
    return render(request, "user.html")


def tpl(request):
    return render(request, "tpl.html")


def register(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    return render(request, "register.html")


def login(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    print(username, password)
    return render(request, "ManagementLogin.html")


def login_post(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        # username = request.POST['username']
        # password = request.POST['password']
        print(username, password)
    return render(request, "ManageIndex.html")


def pic_upload(request):
    return render(request, "PicUploadTest.html")


def updateinfo(request):
    if request.method == 'POST':
        new_img = models.mypicture(
            photo=request.FILES.get('photo'),
            user=request.FILES.get('photo').name
        )
        new_img.save()
        return HttpResponse('上传成功！')
    return render(request, 'PicUploadTest.html')

