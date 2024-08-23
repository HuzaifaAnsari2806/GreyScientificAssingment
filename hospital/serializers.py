from .models import *
from rest_framework import serializers


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Department
        fields="__all__"
        
class PatienRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model=Patient_Records
        fields="__all__"
        
class DoctorPostSerializer(serializers.ModelSerializer):
    class Meta:
        model=Doctor
        fields="__all__"
        
class DoctorGetSerializer(serializers.ModelSerializer):
    doctor=serializers.SerializerMethodField()
    department=serializers.SerializerMethodField()
    class Meta:
        model=Doctor
        fields=['id','doctor','department']
    
    def get_doctor(self,obj):
        return obj.user.username
    
    def get_department(self,obj):
        return obj.department.name
        
class PatientPostSerializer(serializers.ModelSerializer):
    class Meta:
        model=Patient
        fields="__all__"
        
    def validate(self, data):
        
        patient_user = data.get('user')  
        doctor_instance = data.get('doctor')
        
        
        if patient_user and doctor_instance:
            doctor_user = doctor_instance.user  
            
            if patient_user == doctor_user:
                raise serializers.ValidationError("Patient and doctor cannot be the same user.")
        
        return data
        
class PatientGetSerializer(serializers.ModelSerializer):
    patient=serializers.SerializerMethodField()
    doctor=serializers.SerializerMethodField()
    department=serializers.SerializerMethodField()
    class Meta:
        model=Patient
        fields=['id','patient','doctor','department']
        
    def get_patient(self,obj):
        return obj.user.username
    
    def get_doctor(self,obj):
        return obj.doctor.user.username
    
    def get_department(self,obj):
        return obj.department.name