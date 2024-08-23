from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Department(models.Model):
    dept_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100)
    diagnostics=models.CharField(max_length=200)
    location=models.CharField(max_length=50)
    specialization=models.CharField(max_length=200)
    
    def __str__(self):
        return self.name
 
class Patient_Records(models.Model):
    record_id=models.AutoField(primary_key=True)
    patient=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    created_on = models.DateField(auto_now_add=True,editable=False)
    diagnostics=models.CharField(max_length=100)
    observations=models.TextField()
    treatments=models.TextField()
    dept_id=models.ForeignKey(Department,on_delete=models.CASCADE)
    misc=models.TextField()
    
    def __str__(self):
        return f"Record {self.record_id} for {self.patient.username}"
    
class Doctor(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    department=models.ForeignKey(Department,on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.user.username
    
class Patient(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    doctor=models.ForeignKey(Doctor,on_delete=models.CASCADE)
    department=models.ForeignKey(Department,on_delete=models.CASCADE,null=True,blank=True)
    
    def __str__(self) -> str:
        return self.user.username