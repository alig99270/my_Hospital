from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import User, DoctorProfile, StaffProfile, PatientProfile
from .serializers import UserSerializer, DoctorProfileSerializer, StaffProfileSerializer, PatientProfileSerializer, RegisterSerializer
from hms.permissions import IsAdmin, IsDoctor, IsStaff, IsPatient

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]

    def get_queryset(self):
        if self.request.user.role == 'Admin':
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)

class DoctorProfileViewSet(viewsets.ModelViewSet):
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorProfileSerializer
    permission_classes = [IsAdmin | IsDoctor]

    def get_queryset(self):
        if self.request.user.role == 'Admin':
            return DoctorProfile.objects.all()
        return DoctorProfile.objects.filter(user=self.request.user)

class StaffProfileViewSet(viewsets.ModelViewSet):
    queryset = StaffProfile.objects.all()
    serializer_class = StaffProfileSerializer
    permission_classes = [IsAdmin | IsStaff]

    def get_queryset(self):
        if self.request.user.role == 'Admin':
            return StaffProfile.objects.all()
        return StaffProfile.objects.filter(user=self.request.user)

class PatientProfileViewSet(viewsets.ModelViewSet):
    queryset = PatientProfile.objects.all()
    serializer_class = PatientProfileSerializer
    permission_classes = [IsAdmin | IsPatient]

    def get_queryset(self):
        if self.request.user.role == 'Admin':
            return PatientProfile.objects.all()
        return PatientProfile.objects.filter(user=self.request.user)

class RegisterViewSet(viewsets.GenericViewSet):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({"message": "User created successfully", "id": user.id}, status=status.HTTP_201_CREATED)