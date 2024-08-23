from django.urls import path

from .views import *
urlpatterns = [
    
    path("patients_records", getPatientRecords.as_view()),
    path("patients_records/<int:pk>", getPatientRecordswithId),
    
    
    path("department", getDepartment.as_view()),
    path("department/<int:pk>", getDepartmentwithId),
    path("department/<int:pk>/doctors", DepartmentDoctorsView),
    
    
    path("patients", getPatient.as_view()),
    path("patients/<int:pk>", getPatientwithId),
    path("department/<int:pk>/patients", DepartmentPatientsView),
    
    
    path("doctors", getDoctor.as_view()),
    path("doctors/<int:pk>", getDoctorwithId),
    
    
    path("auth/callback/", auth0_callback, name="authentication")
]
