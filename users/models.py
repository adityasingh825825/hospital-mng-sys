from django.db import models
from django.contrib.auth.models import User
from PIL import Image



bloodgroup = (
    ('', 'Choose...'),
    ('A', 'A'), 
    ('A+', 'A+'),
    ('B', 'B'),
    ('B+', 'B+'),
    ('O+', 'O+'),)

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    phone = models.IntegerField(blank=True, null=True)
    registered_as = models.CharField(max_length=20, choices=(('', 'Choose...'),('Doc', 'Doctor'), ('Patnt', 'Patient')))
    gender = models.CharField(max_length=20, choices=(('', 'Choose...'),('M', 'Male'), ('F', 'Female')))
    age = models.IntegerField(blank=True, null=True)
    address = models.CharField(max_length=100, blank=True)
    blood_group = models.CharField(max_length=10, choices=(bloodgroup))
    def __str__(self):
        return f'{self.user.username} Profile'


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)

class Prescreption(models.Model):
    date_added = models.DateTimeField(auto_now=False, auto_now_add=True)
    symptoms = models.CharField(max_length=50)
    prescreption =  models.TextField(max_length=500)
    patient_name = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient_prescribed')
    doctor_name = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor_prescribed')

    def __str__(self):
        return f'{self.patient_name.username} patient\'s prescreption'
