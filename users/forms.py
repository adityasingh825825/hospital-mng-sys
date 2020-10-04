from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import Profile, Prescreption

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    def clean(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email already exists")
        return self.cleaned_data            

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
    

class RegisterTypeForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['registered_as']

class  UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name']

class ProfileUpdateForm(forms.ModelForm):
    class  Meta:
        model = Profile
        fields = ['image', 'phone', 'gender', 'age', 'address', 'blood_group']

class PrescreptionForm(forms.ModelForm):
    class Meta:
        model = Prescreption
        fields = ['symptoms', 'prescreption', 'patient_name']