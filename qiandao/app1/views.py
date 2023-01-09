from django.shortcuts import render,redirect
from django.http import HttpResponse
from app1 import models
from django.core.files.base import ContentFile
from django.contrib.auth import authenticate, login
from functools import wraps


# Create your views here.

# 检查登录状态
def check_login(func):
    @wraps(func)  #装饰器修复技术
    def inner(request,*args,**kwargs):
        #已经登录过的继续执行
        ret = request.get_signed_cookie("is_login", default="0", salt="dsb")
        if ret == "1":
            return func(request,*args,**kwargs)
        #没有登录过的跳转登录界面
        else:
            return redirect("/login")
            # #获取当前访问的URl
            # next_url = request.path_info
            # print(next_url)
            # return redirect("/login/?next={}".format(next_url))
    return inner

# 主页，处理教师和管理员登录，学生签到
@check_login
def index(request):
    return redirect("/login")


@check_login
def user_list(request):
    return render(request, "user.html")


@check_login
def user_list(request):
    return render(request, "user.html")


@check_login
def tpl(request):
    return render(request, "tpl.html")

def login(request):
    errmsg = ""
    if request.method == "POST":
        usertype = request.POST['seltype']
        username = request.POST['username']
        password = request.POST['password']
        next_url = request.GET.get("next")
        # 学生登录
        if usertype == "学生":
            stu_obj = models.Student.objects.filter(studentNo=username, password=password)
            if stu_obj:
                if next_url:
                    rep = redirect(next_url)
                else:
                    rep = redirect('/student')
                rep.set_signed_cookie("is_login", "1", salt="dsb", max_age=60 * 60 * 24 * 7)
                rep.set_signed_cookie("username", username, salt="dsb", max_age=60 * 60 * 24 * 7)
                return rep
            else:
                errmsg="用户名或密码输入错误"
        # 管理员登录
        elif usertype == "管理员":
            object = models.Admin.objects.filter(adminNo=username, password=password)
            if object:
                if next_url:
                    rep = redirect(next_url)
                else:
                    rep = redirect('/manage')
                rep.set_signed_cookie("is_login", "1", salt="dsb", max_age=60 * 60 * 24 * 7)
                rep.set_signed_cookie("username", username, salt="dsb", max_age=60 * 60 * 24 * 7)
                return rep
            else:
                errmsg="用户名或密码输入错误"
        # 教师登录
        else:
            object = models.Teacher.objects.filter(teacherNo=username, password=password)
            if object:
                if next_url:
                    rep = redirect(next_url)
                else:
                    rep = redirect('/teacher')
                rep.set_signed_cookie("is_login", "1", salt="dsb", max_age=60 * 60 * 24 * 7)
                rep.set_signed_cookie("username", username, salt="dsb", max_age=60 * 60 * 24 * 7)
                return rep
            else:
                errmsg = "用户名或密码输入错误"
    else:
        errmsg = "您还未登录！"
    return render(request, 'login.html', {"errmsg":errmsg})
@check_login
def logout(request):
    rep = redirect("/login/")
    rep.delete_cookie("is_login")
    rep.delete_cookie("username")
    return rep



def register(request):
    return render(request, "register.html")


@check_login
def pic_upload(request):
    return render(request, "PicUploadTest.html")

@check_login
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
@check_login
def teacher(request):
    teaName = request.get_signed_cookie("username", salt="dsb")
    return render(request, "Teacher/Tmain.html", {"teaName": teaName})

@check_login
def classInfo(request):
    data_list = models.Class.objects.all()
    print(data_list)
    return render(request, "Classinfo.html", {"n1": data_list})

@check_login
def signpublish(request):
    teaName = request.get_signed_cookie("username", salt="dsb")
    return render(request, "Teacher/SignPublish.html", {"teaName": teaName})

@check_login
def signresult(request):
    teaName = request.get_signed_cookie("username", salt="dsb")
    return render(request, "Teacher/SignResult.html", {"teaName": teaName})

@check_login
def tcourse(request):
    teaName = request.get_signed_cookie("username", salt="dsb")
    return render(request, "Teacher/Tcourse.html", {"teaName": teaName})


# 管理员功能组
@check_login
def manageIndex(request):
    admName = request.get_signed_cookie("username", salt="dsb")
    return render(request, "Manage/main.html", {"admName": admName})

@check_login
def manageStudent(request):
    admName = request.get_signed_cookie("username", salt="dsb")
    ask=request.GET.get("ask")
    if(ask!=None):
        studentNo=models.Student.objects.filter(name__contains=ask)
        return render(request, "Manage/ManageStudent.html", {"admName": admName,"n1": studentNo})
    if(ask==None):
        student_list = models.Student.objects.all()
        return render(request, "Manage/ManageStudent.html", {"admName": admName,"n1":student_list})
#管理员增加学生信息
@check_login
def addstudent(request):
    admName = request.get_signed_cookie("username", salt="dsb")
    if request.method=='GET':
            return render(request,"Manage/add-student.html")
    user=request.POST.get("name")
    pwd=request.POST.get("password")
    studentNo=request.POST.get("studentNo")
    img = request.FILES.get('img')
    img_name=img.name
    print('打印图片',img)
    models.Student.objects.create(studentNo=studentNo,name=user,password=pwd,photo=img,img_name=img_name)
    return redirect("/managestudent/")
#管理员删除学生信息
@check_login
def manageStudentDelete(request):
      nid=request.GET.get('nid')
      models.Student.objects.filter(studentNo=nid).delete()
      return redirect("/managestudent/")
#管理员修改学生信息
@check_login
def manageStudentModify(request,nid):
      admName = request.get_signed_cookie("username", salt="dsb")
      if request.method=='GET':
            studentNo=models.Student.objects.filter(studentNo=nid).first()
            return render(request,"Manage/modify-student.html",{"n1":studentNo,"nid":nid})
      user=request.POST.get("name")
      pwd=request.POST.get("password")
      studentNo=request.POST.get("studentNo")
      img = request.FILES.get('img')
      print('打印图片',img)
      if (img!=None):
           img_name=img.name 
           models.StudentPhoto.objects.create(photo=img)
           models.Student.objects.filter(studentNo=nid).update(studentNo=nid,name=user,password=pwd,photo=img,img_name=img_name)
      else:
            models.Student.objects.filter(studentNo=nid).update(studentNo=nid,name=user,password=pwd)
      return redirect("/managestudent/")
#管理员课程
@check_login
def manageCourse(request):
    admName = request.get_signed_cookie("username", salt="dsb")
    ask=request.GET.get("ask")
    if(ask!=None):
        courseNo=models.Course.objects.filter(courseName__contains=ask)
        return render(request, "Manage/ManageCourse.html", {"admName": admName,"n1": courseNo})
    if(ask==None):
        course_list = models.Course.objects.all()
        return render(request, "Manage/ManageCourse.html", {"admName": admName,"n1": course_list})
@check_login
def addcourse(request):
    admName = request.get_signed_cookie("username", salt="dsb")
    if request.method=='GET':
            return render(request,"Manage/add-course.html")
    print(request.POST)
    courseNo=request.POST.get("courseNo")
    courseName=request.POST.get("courseName")
    grade=request.POST.get("grade")
    models.Course.objects.create(courseNo=courseNo,courseName=courseName,grade=grade)
    return redirect("/managecourse/")
#管理员删除学生信息
@check_login
def manageCourseDelete(request):
      nid=request.GET.get('nid')
      models.Course.objects.filter(courseNo=nid).delete()
      return redirect("/managecourse/")
@check_login
def manageCourseModify(request,nid):
      admName = request.get_signed_cookie("username", salt="dsb")
      if request.method=='GET':
            studentNo=models.Course.objects.filter(courseNo=nid).first()
            return render(request,"Manage/modify-course.html",{"n1":studentNo,"nid":nid})
      nid=request.POST.get("nid")
      name=request.POST.get("courseName")
      pwd=request.POST.get("password")
      models.Course.objects.filter(courseNo=nid).update(courseNo=nid,courseName=name,grade=pwd)
      return redirect("/managestudent/")
#管理员教师
@check_login
def manageTeacher(request):
    admName = request.get_signed_cookie("username", salt="dsb")
    ask=request.GET.get("ask")
    if(ask!=None):
        teacherNo=models.Teacher.objects.filter(name__contains=ask)
        return render(request, "Manage/ManageTeacher.html", {"admName": admName,"n1": teacherNo})
    if(ask==None):
        teacher_list = models.Teacher.objects.all()
        return render(request, "Manage/ManageTeacher.html", {"admName": admName,"n1": teacher_list})

@check_login
def addteacher(request):
    admName = request.get_signed_cookie("username", salt="dsb")
    if request.method=='GET':
            return render(request,"Manage/add-teacher.html")
    print(request.POST)
    teacherNo=request.POST.get("teacherNo")
    name=request.POST.get("name")
    user=request.POST.get("user")
    password=request.POST.get("password")
    models.Teacher.objects.create(teacherNo=teacherNo,name=name,user=user,password=password)
    return redirect("/manageteacher/")
@check_login
def manageTeacherDelete(request):
      nid=request.GET.get('nid')
      models.Teacher.objects.filter(teacherNo=nid).delete()
      return redirect("/manageteacher/")
@check_login
def manageTeacherModify(request,nid):
      admName = request.get_signed_cookie("username", salt="dsb")
      if request.method=='GET':
            studentNo=models.Teacher.objects.filter(teacherNo=nid).first()
            return render(request,"Manage/modify-teacher.html",{"n1":studentNo,"nid":nid})
      nid=request.POST.get("nid")
      name=request.POST.get("name")
      user=request.POST.get("user")
      password=request.POST.get("password")
      models.Course.objects.filter(teacherNo=nid).update(teacherNo=nid,name=name,password=password,user=user)
      return redirect("/manageteacher/")
#管理员教师
# 学生签到页面
@check_login
def student(request):
    stuName = request.get_signed_cookie("username", salt="dsb")
    return render(request, "Student/Smain.html", {"stuName": stuName})

@check_login
def sign(request):
    stuName = request.get_signed_cookie("username", salt="dsb")
    return render(request, "Student/Sign.html")

@check_login
def signinfo(request):
    stuName = request.get_signed_cookie("username", salt="dsb")
    return render(request, "Student/SignInfo.html")
