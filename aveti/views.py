from django.shortcuts import render,HttpResponse, redirect,HttpResponseRedirect
from django.contrib.auth import logout, authenticate, login
from .models import Cususer, Teachers, Students, Admin
from django.contrib import messages
 

 
 
# def login(request):
#     return render(request, 'login_page.html')
 
def doLogin(request):
     
    email_id = request.GET.get('email')
    password = request.GET.get('password')
    # user_type = request.GET.get('user_type')

    if not (email_id and password):
        messages.error(request, "Please provide all the details!!")
        return render(request, 'login_page.html')
 
    user = Cususer.objects.get(email=email_id)
    if not user:
        messages.error(request, 'Invalid Login Credentials!!')
        return render(request, 'login_page.html')
    x = user.check_password(password)
    if not x:
        messages.error(request, 'Invalid Login Credentials!!')
        return render(request, 'login_page.html')
 
    login(request, user)
    # print(request.user)
 
    if user.user_type == Cususer.STUDENT:
        return redirect('student_home/')
    elif user.user_type == Cususer.TEACHER:
        return redirect('teacher_home/')
    elif user.user_type == Cususer.ADMIN:
        return redirect('admin_home/')
 
    return render(request, password)
 
     
def registration(request):
    return render(request, 'registration.html')
     
 
def doRegistration(request):
    first_name = request.GET.get('first_name')
    last_name = request.GET.get('last_name')
    email_id = request.GET.get('email')
    user_type = request.GET.get('type')
    password = request.GET.get('password')
    confirm_password = request.GET.get('confirmPassword')
 
    if not (email_id and password and confirm_password):
        messages.error(request, 'Please provide all the details!!')
        return render(request, 'registration.html')
     
    if password != confirm_password:
        messages.error(request, 'Both passwords should match!!')
        return render(request, 'registration.html')
 
    is_user_exists = Cususer.objects.filter(email=email_id).exists()
 
    if is_user_exists:
        messages.error(request, 'User with this email id already exists. Please proceed to login!!')
        return render(request, 'registration.html')
 
 
    if user_type is None:
        messages.error(request, "Please use valid format for the email id: '<username>.<staff|student|hod>@<college_domain>'")
        return render(request, 'registration.html')
 
    username = email_id.split('@')[0].split('.')[0]
 
    if Cususer.objects.filter(username=username).exists():
        messages.error(request, 'User with this username already exists. Please use different username')
        return render(request, 'registration.html')
 
    user = Cususer()
    user.username = username
    user.email = email_id
    user.password = password
    user.user_type = user_type
    user.first_name = first_name
    user.last_name = last_name
    user.save()
     
    if user_type == Cususer.TEACHER:
        Teachers.objects.create(admin=user)
    elif user_type == Cususer.STUDENT:
        Students.objects.create(admin=user)
    elif user_type == Cususer.ADMIN:
        Admin.objects.create(admin=user)
    return render(request, 'login_page.html')
 
     
def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/aveti')
 
