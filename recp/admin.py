from django.contrib import admin
from .models import PaymentHistory, Appointments
# Register your models here.
admin.site.register(PaymentHistory)
admin.site.register(Appointments)