from rest_framework import serializers
from . models import Appointment
from doctor.serializers import AvailableTimeSerializer,DoctorSerializer,SpecializationSerializer
from patient.serializers import PatientSerialzer
class AppointmentSerializer(serializers.ModelSerializer):
    available_time = AvailableTimeSerializer(read_only=True)
    patient = PatientSerialzer(read_only=True)
    doctor = DoctorSerializer(read_only=True)
    specialization = SpecializationSerializer(read_only=True)
    class Meta:
        model = Appointment
        fields = '__all__'
        read_only_fields = ["patient", "cancel", "appointment_type"]

    def validate(self, attrs):
        user = self.context["request"].user

        if hasattr(user, 'doctor'):
            raise serializers.ValidationError(
                {
                   'duplicate': ["Doctors are not allowed to take appointment"]
                }
            )

        if not hasattr(user, "patient"):
            raise serializers.ValidationError({'duplicate': ["Only patients can take appointment"]})
        
        patient = user.patient
        doctor = attrs.get("doctor")
        time = attrs.get("time")
        date = attrs.get("date") 

        if Appointment.objects.filter(
            patient=patient,
            doctor=doctor,
            time=time,
            date=date,
        ).exists():
            raise serializers.ValidationError(
                {'duplicate': ["You already have an appointment with this doctor at this time"]}
            )
        
        if Appointment.objects.filter(
            patient=patient,
            time=time,
            date=date,
            cancel=False
        ).exists():
            raise serializers.ValidationError(
                {'duplicate': ["You already have an appointment at this time"]}
            )
           

        if not attrs.get("time"):
            raise serializers.ValidationError("Time is required")
   
        return attrs