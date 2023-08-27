from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

 
# Overriding the Default Django Auth
# User and adding One More Field (user_type)
class Cususer(AbstractUser):
    ADMIN = '1'
    TEACHER = '2'
    STUDENT = '3'
     
    EMAIL_TO_USER_TYPE_MAP = {
        'admin': ADMIN,
        'teacher': TEACHER,
        'student': STUDENT
    }
 
    user_type_data = ((ADMIN, "HOD"), (TEACHER, "teacher"), (STUDENT, "Student"))
    user_type = models.CharField(default=1, choices=user_type_data, max_length=10)
 
class Admin(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(Cususer, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    
    def __str__(self):
        return self.admin
 
 
class Teachers(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(Cususer, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    
    def __str__(self):
        return self.admin
 
 
 

 
 
 
class Students(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(Cususer, on_delete = models.CASCADE)
    gender = models.CharField(max_length=50)
    profile_pic = models.FileField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    
    def __str__(self):
        return self.admin
 

 
 

@receiver(post_save, sender=Cususer)

def create_user_profile(sender, instance, created, **kwargs):
    # if Created is true (Means Data Inserted)
    if created:
       
        # Check the user_type and insert the data in respective tables
        if instance.user_type == 1:
            Admin.objects.create(admin=instance)
        if instance.user_type == 2:
            Teachers.objects.create(admin=instance)
        if instance.user_type == 3:
            Students.objects.create(admin=instance,
                                    gender="")
     
 
@receiver(post_save, sender=Cususer)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.admin.save()
    if instance.user_type == 2:
        instance.teachers.save()
    if instance.user_type == 3:
        instance.students.save()