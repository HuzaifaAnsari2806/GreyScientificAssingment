from rest_framework.permissions import BasePermission

class isDoctor(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='doctor').exists()
    
class isPatient(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='patient').exists()