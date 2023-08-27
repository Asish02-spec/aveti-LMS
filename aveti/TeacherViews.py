from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import AddStudentForm, EditStudentForm
from .models import Cususer, Teachers, Students
 
def teacher_home(request):
    teacher = Teachers.objects.get(User=request.user)
    students = teacher.get_students()
    context = {'teacher': teacher, 'students': students}
    return render(request, 'teacher_home.html', context)
 
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
 
 
 
def edit_student(request, student_id):
   
 
    student = get_object_or_404(Students,id=student_id)
    form = EditStudentForm(request.POST or None, instance= student)
     
    # Filling the form with Data from Database
    form.fields['email'].initial = student.admin.email
    form.fields['username'].initial = student.admin.username
    form.fields['first_name'].initial = student.admin.first_name
    form.fields['last_name'].initial = student.admin.last_name
    form.fields['gender'].initial = student.gender
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/"+ student_id)
    context ={
        "form": form
    }
    return render(request, "admin_template/edit_student.html", context)
 
 
def delete_student(request, student_id):
    student = Students.objects.get(admin=student_id)
    try:
        student.delete()
        messages.success(request, "Student Deleted Successfully.")
        return redirect('manage_student')
    except:
        messages.error(request, "Failed to Delete Student.")
        return redirect('manage_student')
 