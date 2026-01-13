from django.shortcuts import render
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import Appointment
from .serializers import AppointmentSerializer
from rest_framework.permissions import IsAuthenticated

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['patient']
   

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     patient_id = self.request.query_params.get('patient')
    #     if patient_id:
    #         queryset = queryset.filter(patient_id=patient_id)
    #     return queryset

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, "patient"):
            return Appointment.objects.filter(patient=user.patient)
        return Appointment.objects.none()
    
    def perform_create(self, serializer):
        doctor_id = self.request.data.get("doctor")
        serializer.save(
            patient=self.request.user.patient,
            doctor_id=doctor_id,
            appointment_type="Pending"
        )
