from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.
class PaymentHistory(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    outstanding = models.IntegerField(blank=True, null=True)
    paid = models.IntegerField(blank=True, null=True)
    medical_rec = models.ImageField(default='default.jpg', upload_to='medical_records', blank=True)
    case_paper = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f'{self.user} Payment History'
status_choice = (
    ('', 'Choose...'),
    ('Completed', 'Completed'),
    ('Pending', 'Pending')
)

class Appointments(models.Model):
    date = models.DateField()
    time = models.TimeField()
    doctor_name = models.ForeignKey(User, related_name='doctor', on_delete=models.CASCADE)
    patient_name = models.ForeignKey(User, related_name='patient', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=status_choice)

    def __str__(self):
        return f'Doctor {self.doctor_name} Appointment'