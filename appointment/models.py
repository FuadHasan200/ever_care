from django.db import models
from patient.models import Patient
from doctor.models import Doctor,AvailableTime
from django.utils import timezone
# Create your models here.
APPOINTMENT_TYPE = [
    ('Pending','Pending'),
    ('Running','Running'),
    ('Completed','Completed')
]
APPOINTMENT_STATUS = [
    ('Online','Online'),
    ('Offline','Offline')
]
class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment_type = models.CharField(choices=APPOINTMENT_TYPE,max_length=20, default='Pending')
    appointment_status = models.CharField(choices=APPOINTMENT_STATUS,max_length=20)
    symptom = models.TextField()
    time = models.ForeignKey(AvailableTime, on_delete=models.CASCADE)
    cancel = models.BooleanField(default=False)
    date = models.DateTimeField(default=timezone.now)
    

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["patient", "doctor", "time","date"],
                name="unique_patient_doctor_time_date"
            ),

            # models.UniqueConstraint(
            # fields=['doctor', 'time', 'date'],
            # name='unique_doctor_time_date'
            # ),

            models.UniqueConstraint(
            fields=['patient', 'time', 'date'],
            name='unique_patient_time_date'
            ),
            

        ]