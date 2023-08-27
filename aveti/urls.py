from django.contrib import admin
from django.urls import path, include
from . import AdminViews, views
from . import TeacherViews, StudentViews
 
urlpatterns = [
    path('', views.loginUser, name="login"),
    path('login', views.loginUser, name="login"),
    path('logout_user', views.logout_user, name="logout_user"),
    path('registration/', views.registration, name="registration"),
    path('doLogin', views.doLogin, name="doLogin"),
    path('doRegistration', views.doRegistration, name="doRegistration"),
     
      # URLS for Student
    path('student_home/', StudentViews.student_home, name="student_home"),
    path('student_profile/', StudentViews.student_profile, name="student_profile"),

 
 
     # URLS for teacher
    path('teacher_home/', TeacherViews.teacher_home, name="teacher_home"),
    path('teacher_profile/',TeacherViews.teacher_profile, name="teacher_profile"),


     
    # URL for Admin
    path('admin_home/', AdminViews.admin_home, name="admin_home"),
    path('add_teacher/', AdminViews.add_teacher, name="add_teacher"),
    path('add_teacher_save/', AdminViews.add_teacher_save, name="add_teacher_save"),
    path('manage_teacher/', AdminViews.manage_teacher, name="manage_teacher"),
    path('edit_teacher/<teacher_id>/', AdminViews.edit_teacher, name="edit_teacher"),
    path('edit_teacher_save/', AdminViews.edit_teacher_save, name="edit_teacher_save"),
    path('delete_teacher/<teacher_id>/', AdminViews.delete_teacher, name="delete_teacher"),
    path('add_student/', AdminViews.add_student, name="add_student"),
    path('add_student_save/', AdminViews.add_student_save, name="add_student_save"),
    path('manage_student/', AdminViews.list_stud, name="manage_student"),
    path('edit_student/<student_id>/', AdminViews.edit_student, name="edit_student"),
   # path('edit_student_save/', AdminViews.edit_student_save, name="edit_student_save"),
    path('delete_student/<student_id>/', AdminViews.delete_student, name="delete_student"),
    path('check_email_exist/', AdminViews.check_email_exist, name="check_email_exist"),
    path('check_username_exist/', AdminViews.check_username_exist, name="check_username_exist"),
    path('admin_profile/', AdminViews.admin_profile, name="admin_profile"),
    path('admin_profile_update/', AdminViews.admin_profile_update, name="admin_profile_update"),
     
]