import requests

from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings

from rest_framework import generics,status,mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import *
from .serializers import *

# Create your views here.
class getPatient(generics.ListCreateAPIView):
    queryset=Patient.objects.all()
    
    def get_serializer_class(self):
        if self.request.method=="GET":
            return PatientGetSerializer
        elif self.request.method=="POST":
            return PatientPostSerializer
        return super().get_serializer_class()
    
@api_view(['GET','PUT','DELETE'])
def getPatientwithId(request,pk):
    try:
        patient = Patient.objects.get(id=pk)
    except Patient.DoesNotExist:
        return Response({"error": "Patient record not found."}, status=status.HTTP_404_NOT_FOUND)
    if request.method=='GET':
        serializer=PatientGetSerializer(patient)
        return Response({"data":serializer.data})
    
    elif request.method=='PUT':
        data=request.data
        serializer=PatientPostSerializer(patient,data=data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"data":serializer.data},status=status.HTTP_205_RESET_CONTENT)
        else:
            return Response({"errors":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method=='DELETE':
        patient.delete()
        return Response({"message":"Record deleted successfully"})
    
class getDoctor(generics.ListCreateAPIView):
    queryset=Doctor.objects.all()
    
    def get_serializer_class(self):
        if self.request.method=="GET":
            return DoctorGetSerializer
        elif self.request.method=="POST":
            return DoctorPostSerializer
        return super().get_serializer_class()
    
@api_view(['GET','PUT','DELETE'])
def getDoctorwithId(request,pk):
    try:
        doctor = Doctor.objects.get(id=pk)
    except Doctor.DoesNotExist:
        return Response({"error": "Doctor record not found."}, status=status.HTTP_404_NOT_FOUND)
    if request.method=='GET':
        serializer=DoctorGetSerializer(doctor)
        return Response({"data":serializer.data})
    
    elif request.method=='PUT':
        data=request.data
        serializer=DoctorPostSerializer(doctor,data=data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"data":serializer.data},status=status.HTTP_205_RESET_CONTENT)
        else:
            return Response({"errors":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method=='DELETE':
        doctor.delete()
        return Response({"message":"Record deleted successfully"})

class getPatientRecords(generics.ListCreateAPIView):
    queryset=Patient_Records.objects.all()
    serializer_class=PatienRecordSerializer
    
@api_view(['GET','PUT','DELETE'])
def getPatientRecordswithId(request,pk):
        try:
            patient_record = Patient_Records.objects.get(record_id=pk)
        except Patient_Records.DoesNotExist:
            return Response({"error": "Patient record not found."}, status=status.HTTP_404_NOT_FOUND)
        if request.method=='GET':
            serializer=PatienRecordSerializer(patient_record)
            return Response({"data":serializer.data})
        
        elif request.method=='PUT':
            data=request.data
            serializer=PatienRecordSerializer(patient_record,data=data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"data":serializer.data},status=status.HTTP_205_RESET_CONTENT)
            else:
                return Response({"errors":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        
        elif request.method=='DELETE':
            patient_record=Patient_Records.objects.get(record_id=pk)
            patient_record.delete()
            return Response({"message":"Record deleted successfully"})
        
        
    
class getDepartment(generics.ListCreateAPIView):
    queryset=Department.objects.all()
    serializer_class=DepartmentSerializer    
    
@api_view(['GET','PUT','DELETE'])
def getDepartmentwithId(request,pk):
    try:
        department = Department.objects.get(dept_id=pk)
    except Department.DoesNotExist:
        return Response({"error": "Department record not found."}, status=status.HTTP_404_NOT_FOUND)
    if request.method=='GET':
        serializer=DepartmentSerializer(department)
        return Response({"data":serializer.data})
    
    elif request.method=='PUT':
        data=request.data
        serializer=DepartmentSerializer(department,data=data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"data":serializer.data},status=status.HTTP_205_RESET_CONTENT)
        else:
            return Response({"errors":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method=='DELETE':
        department.delete()
        return Response({"message":"Record deleted successfully"})

@api_view()
def DepartmentDoctorsView(request,pk):
    try:
        doctor = Doctor.objects.filter(department=pk).first()
    except Doctor.DoesNotExist:
        return Response({"error": "Department record not found."}, status=status.HTTP_404_NOT_FOUND)
    serializer=DoctorGetSerializer(doctor)
    return Response({"data":serializer.data})

@api_view()
def DepartmentPatientsView(request,pk):
    try:
        patient = Patient.objects.filter(department=pk).first()
    except Patient.DoesNotExist:
        return Response({"error": "Department record not found."}, status=status.HTTP_404_NOT_FOUND)
    serializer=PatientGetSerializer(patient)
    return Response({"data":serializer.data})





def auth0_callback(request):
    code = request.GET.get('code')
    if not code:
        return JsonResponse({'error': 'No code provided'}, status=400)

    token_url = f'https://{settings.DOMAIN}/oauth/token'
    token_data = {
        'grant_type': 'authorization_code',
        'client_id': settings.CLIENT_ID,
        'client_secret': settings.CLIENT_SECRET,
        'code': code,
        'redirect_uri': 'http://localhost:8000/hospital/auth/callback/'
    }

    token_r = requests.post(token_url, json=token_data)
    token_r.raise_for_status()

    tokens = token_r.json()
    access_token = tokens.get('access_token')

    return JsonResponse({'access_token': access_token})
