from django.shortcuts import render
from django.http import HttpResponse
from app1 import models
from django.core.files.base import ContentFile
from django.contrib.auth import authenticate, login


# Create your views here.

# 主页，处理教师和管理员登录，学生签到
def index(request):
    return render(request, "test-studentdis.html")


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


def teacher_register(request):
    return render(request, "teacher_register.html")


def teacher_register(request):
    if request.method == "POST":
        new_teacher = models.Teacher(
            user=request.POST.get('user'),
            name=request.POST.get('name'),
            teacherNo=request.POST.get('teacherNo'),
            password=request.POST.get('password')
        )
        new_teacher.save()


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


# 教师功能组


def teacher(request):
    return render(request, "app1/templates/teacher/teacher.html")


def teacherlogin(request):
    # request.session["is_login"]=True
    if request.method == 'GET':
        return render(request, "TeacherLogin.html")
    if request.session.get("is_login", None):
        return HttpResponse("您已登录！")
    teacherNo = request.POST.get('teacherNo')
    password = request.POST.get('password')
    # print(teacherNo, password)
    detailist = models.Teacher.objects.filter(teacherNo=teacherNo)
    if not detailist.exists():
        return HttpResponse("该用户不存在！")
    # print(detailist)
    for i in detailist:
        if password == i.password:
            request.session["teacherNo"] = teacherNo
            request.session["is_login"] = True
            return render(request, "ManageIndex.html")
        else:
            return HttpResponse('职工号或密码错误')
            # return render(request, "ManageIndex.html")


def classInfo(request):
    data_list = models.Class.objects.all()
    print(data_list)
    return render(request, "Classinfo.html", {"n1": data_list})

def publishSign(request):
    return render(request, "app1/templates/teacher/SignPublish.html")


def signResult(request):
    return render(request, "app1/templates/teacher/SignResult.html")


# 管理员功能组
def manageIndex(request):
    return render(request, "ManageIndex.html")


def manageCourse(request):
    return render(request, "ManageCourse.html")


def manageTeacher(request):
    return render(request, "ManageTeacher.html")


def manageStudent(request):
    return render(request, "ManageTeacher.html")


def adminlogin(request):
    # request.session["is_login"]=True
    if request.method == 'GET':
        return render(request, "TeacherLogin.html")
    if request.session.get("is_login", None):
        return HttpResponse("您已登录！")
    username = request.POST.get('teacherNo')
    password = request.POST.get('password')
    # print(teacherNo, password)
    detailist = models.Admin.objects.filter(username=username)
    if not detailist.exists():
        return HttpResponse("该用户不存在！")
    # print(detailist)
    for i in detailist:
        if password == i.password:
            request.session["username"] = username
            request.session["is_login"] = True
            return render(request, "ManageIndex.html")
        else:
            return HttpResponse('职工号或密码错误')
            # return render(request, "ManageIndex.html")

# 学生签到页面
# def studentQiandao(request):
