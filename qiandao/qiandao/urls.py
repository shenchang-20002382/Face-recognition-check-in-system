"""qiandao URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app1 import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    # path("admin/", admin.site.urls),
    path("", views.index),
    path('admin/', admin.site.urls),
    path('updateinfo/', views.updateinfo),
    path("index/", views.index),
    path("users/list/", views.user_list),
    path("tpl/", views.tpl),
    path("register/", views.register),
    path("login/", views.login),
    path("login/post", views.login_post),
    path("pic_upload", views.pic_upload),

#教师页面组
    path("teacher/", views.teacher),
    path("teacher/publishSing/", views.publishSign),
    path("teacher/signResult/", views.signResult),

#管理员页面组
    path("manger/", views.manageIndex),
    path("manger/ManageTeacher/", views.manageTeacher),
    path("manger/ManageStudent/", views.manageStudent),
    path("manage/ManageCourse/", views.manageCourse),

#学生签到页面组
    path("studentQianDao/",),
]
    path("teacher", views.teacher),
    path("teacher/publishSing", views.publishSign),
    # path("teacher/signResult",),

    # path("manager",),
    # path("manger/manageTeacher"),
    # path("manger/manageStudent"),
    # path("manage/manageCourse"),
    # path("manage/teacherCourse"),

    # path("studentQianDao",),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

