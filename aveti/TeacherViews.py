from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import AddStudentForm, EditStudentForm
from .models import Cususer, Teachers, Students
@login_required
def teacher_home(request):
    teacher = request.user
    
    student_name_list=[]
    student_ids=[]
    students = Students.objects.all()
    for student in students:
        student_name_list.append(student.admin.first_name)
        student_ids.append(student.id)
 
 
    context={
        "student_name_list": student_name_list,
        "student_ids":student_ids,
        "teacher":teacher,
    }
    return render(request, "Teacher_template/teacher_home.html", context)
 
def teacher_profile(request):
    user = Cususer.objects.get(id=request.user.id)
    teacher = Teachers.objects.get(admin=user)
 
    context={
        "user": user,
        "teacher": teacher
    }
    return render(request, 'teacher_template/teacher_profile.html', context)
 
 
def add_student(request):
    form = AddStudentForm()
    context = {
        "form": form
    }
    return render(request, 'admin_template/add_student.html', context)
 
 
 
 
def add_student_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('add_student')
    else:
        form = AddStudentForm()
        form = AddStudentForm(request.POST)
 
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            gender = form.cleaned_data['gender']
            try:
                user = Cususer.objects.create_user(username=username,
                                                      password=password,
                                                      email=email,
                                                      first_name=first_name,
                                                      last_name=last_name,
                                                      user_type=3)

                user.save()
                messages.success(request, "Student Added Successfully!")
                return redirect('add_student')
            except:
                messages.error(request, "Failed to Add Student!")
                return redirect('add_student')
        else:
            return redirect('add_student')
 
 
 
def edit_student(request,pk):
    student_id = Students.objects.get(id=pk)
    form = EditStudentForm()
   # Filling the form with Data from Database
    form.fields['email'].initial = student_id.admin.email
    form.fields['username'].initial = student_id.admin.username
    form.fields['first_name'].initial = student_id.admin.first_name
    form.fields['last_name'].initial = student_id.admin.last_name
    form.fields['gender'].initial = student_id.gender
    if request.method == "POST":
        form = EditStudentForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = Students.objects.get(id=pk)
            user.first_name = cd['first_name']
            user.last_name = cd['last_name']
            user.email = cd['email']
            user.username = cd['username']
            user.save()
            return redirect('teacher_home')
    context = {'form':form}
    return render(request, 'admin_template/edit_student.html', context)
 
 
 
def delete_student(request, student_id):
    student = Students.objects.get(id=student_id)
    try:
        student.delete()
        user = Cususer.objects.get(id=student_id)
        try:
            user.delete()
        except:
            messages.error(request, "Failed to Delete Student.")
        messages.success(request, "Student Deleted Successfully.")
        return redirect('teacher_home')
    except:
        messages.error(request, "Failed to Delete Student.")
        return redirect('teacher_home')
 