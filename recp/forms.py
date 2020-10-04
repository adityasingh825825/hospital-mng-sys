from django import forms
from .models import PaymentHistory

class PaymentHistoryForm(forms.ModelForm):

    class Meta:
        model = PaymentHistory
        fields = ['outstanding', 'paid', 'medical_rec', 'case_paper']