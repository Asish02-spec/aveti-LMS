from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import  Students

@login_required
def student_home(request):
    student = request.user
    context = {'student': student}
    return render(request,'Student_template/student_home.html', context)
  
@login_required
def student_profile(request):
    student = Students.objects.get(admin = request.user)
    context = {'student': student}
    return render(request,'student_profile.html', context)
 
