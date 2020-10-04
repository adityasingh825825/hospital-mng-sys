from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, RegisterTypeForm
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Profile, Prescreption
from recp.models import Appointments
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
        ListView,
        DetailView,
        CreateView,
        UpdateView,
        DeleteView
)

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        reg_type_form = RegisterTypeForm(request.POST)
        if form.is_valid() and reg_type_form.is_valid():
            user = form.save()
            user.refresh_from_db()
            reg_type_form = RegisterTypeForm(request.POST, instance=user.profile)
            reg_type_form.full_clean()
            reg_type_form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')

    else:
        form = UserRegisterForm()
        reg_type_form = RegisterTypeForm()
    context = {
            'form': form,
            'reg_type_form': reg_type_form
                }        
    return render(request, 'users/register.html', context)

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)

class AppointmentListView(ListView):
    model = Appointments
    template_name = 'users/appointments.html'
    paginate_by = 10
    ordering = '-status'
    context_object_name = 'appointments'
    def get_queryset(self):
        user = self.request.user
        user_type = user.profile.registered_as      
        if user_type=="Doc":
            return Appointments.objects.filter(doctor_name=user).order_by('-status')
        else:
            return Appointments.objects.filter(patient_name=user).order_by('-status')            
    
    
class PrescreptionCreateViews(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Prescreption
    fields = ['symptoms', 'prescreption', 'patient_name']
    
    def get_success_url(self):
        return reverse('prescreption_view')

    def form_valid(self, form):
        form.instance.doctor_name=self.request.user
        return super().form_valid(form)    
    
    def test_func(self):        
        return self.request.user.profile.registered_as == 'Doc'            

class PrescreptionaListView(LoginRequiredMixin, ListView):
    model = Prescreption
    context_object_name = 'prescreptions'
    paginate_by = 5
    def get_queryset(self):
        user = self.request.user       
        if user.profile.registered_as == 'Doc':
            return Prescreption.objects.filter(doctor_name=user).order_by('-date_added')
        return Prescreption.objects.filter(patient_name=user).order_by('-date_added')            