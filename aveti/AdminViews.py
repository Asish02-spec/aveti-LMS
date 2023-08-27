from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
 
from .forms import AddStudentForm, EditStudentForm ,AddTeacherForm, EditTeacherForm
 
from .models import Cususer, Teachers,  Students,Admin
 
 
def admin_home(request): 
    all_student_count = Students.objects.all().count()
    teacher_count = Teachers.objects.all().count()

    # For Saffs
    teacher_name_list=[]
    teacher_ids = []
    teachers = Teachers.objects.all()
    for teacher in teachers:      
        teacher_name_list.append(teacher.admin.first_name)
        teacher_ids.append(teacher.id)
    # For Students

    student_name_list=[]
    student_ids=[]
    students = Students.objects.all()
    for student in students:
        student_name_list.append(student.admin.first_name)
        student_ids.append(student.id)
 
    print(teacher_name_list)
 
    context={
        "all_student_count": all_student_count,
        "teacher_count": teacher_count,
        "teacher_name_list": teacher_name_list, 
        "teacher_ids": teacher_ids,
        "student_name_list": student_name_list,
        "student_ids":student_ids,
    }
    return render(request, "admin_template/admin_home.html", context)
 
def add_teacher(request):
    form = AddTeacherForm()
    context = {
        "form": form
    }
    return render(request, 'admin_template/add_teacher.html', context)
 
 
def add_teacher_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method ")
        return redirect('add_teacher')
    else:
        form = AddTeacherForm()
        form = AddTeacherForm(request.POST)
 
        if form.is_valid():
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
    
            try:
                user = Cususer.objects.create_user(username=username,
                                                    password=password,
                                                    email=email,
                                                    first_name=first_name,
                                                    last_name=last_name,
                                                    user_type=2)
                user.save()
                messages.success(request, "teacher Added Successfully!")
                return redirect('add_teacher')
            except:
                messages.error(request, "Failed to Add teacher!")
                return redirect('add_teacher')
        else:
            return redirect('add_teacher')
 
 
 
 
def edit_teacher(request, teacher_id):
    teacher = Teachers.objects.get(admin=teacher_id)
 
    context = {
        "teacher": teacher,
        "id": teacher_id
    }
    return render(request, "admin_template/edit_teacher.html", context)
 
 
def edit_teacher_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        teacher_id = request.POST.get('teacher_id')
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

 
        try:
            # INSERTING into Customuser Model
            user = Cususer.objects.get(id=teacher_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.save()
             
            # INSERTING into teacher Model
            teacher_model = Teachers.objects.get(admin=teacher_id)
            teacher_model.save()
 
            messages.success(request, "teacher Updated Successfully.")
            return redirect('/edit_teacher/'+teacher_id)
 
        except:
            messages.error(request, "Failed to Update teacher.")
            return redirect('/edit_teacher/'+teacher_id)
 
 
 
def delete_teacher(request, teacher_id):
    teacher = Teachers.objects.get(id=teacher_id)
    try:
        teacher.delete()
        user = Cususer.objects.get(id=teacher_id)
        try:
            user.delete()
        except:
            messages.error(request, "Failed to Delete Teacher.")
        messages.success(request, "teacher Deleted Successfully.")
        return redirect('admin_home')
    except:
        messages.error(request, "Failed to Delete teacher.")
        return redirect('admin_home')
 
 
 
 

 
 
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
            return redirect('admin_home')
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
        return redirect('admin_home')
    except:
        messages.error(request, "Failed to Delete Student.")
        return redirect('admin_home')
 
 

@csrf_exempt
def check_email_exist(request):
    email = request.POST.get("email")
    user_obj = Cususer.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)
 
 
@csrf_exempt
def check_username_exist(request):
    username = request.POST.get("username")
    user_obj = Cususer.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)
 
 
 

def admin_profile(request):
    user = Cususer.objects.get(id=request.user.id)
 
    context={
        "user": user
    }
    return render(request, 'hod_template/admin_profile.html', context)
 
 
def admin_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('admin_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
 
        try:
            customuser = Cususer.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()
            messages.success(request, "Profile Updated Successfully")
            return redirect('admin_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('admin_profile')
     
 
 
def teacher_profile(request):
    pass
 
 
def student_profile(requtest):
    pass

