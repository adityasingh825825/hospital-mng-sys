from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from .models import Appointments
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.http import JsonResponse
from users.models import Profile
from users.forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .forms import PaymentHistoryForm
from django.views.generic import (
        ListView,
        DetailView,
        CreateView,
        UpdateView,
        DeleteView
)

# Create your views here.
@staff_member_required
def home(request):
    patients = Profile.objects.filter(registered_as='Patnt')
    appointments = Appointments.objects.order_by('-status')
    context = {
        'patients': patients,
        'appointments': appointments
    }
    return render(request, 'recp/home.html', context)

@staff_member_required
def profile_view(request, id):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=Profile.objects.get(pk=id).user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=Profile.objects.get(pk=id))
        pmt_hst_form = PaymentHistoryForm(request.POST,
                                        request.FILES,
                                        instance=Profile.objects.get(pk=id).user.paymenthistory
                                         )

        if u_form.is_valid() and p_form.is_valid() and pmt_hst_form.is_valid():
            u_form.save()
            p_form.save()        
            pmt_hst_form.save()
            messages.success(request, f'Patient\'s details has been updated!')
            return redirect('recp-home')
    else:
        u_form = UserUpdateForm(instance=Profile.objects.get(pk=id).user)
        p_form = ProfileUpdateForm(instance=Profile.objects.get(pk=id))
        pmt_hst_form = PaymentHistoryForm(instance=Profile.objects.get(pk=id).user.paymenthistory)
    context = {
            'u_form': u_form,
            'p_form': p_form,
            'pmt_hst_form': pmt_hst_form
        }

    return render(request, 'recp/recp_profile_view.html', context)



class AppointmentCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Appointments
    fields = ['date', 'time', 'doctor_name', 'patient_name', 'status']
    def get_success_url(self):
        return reverse('recp-home')    
    def test_func(self):
        user = self.request.user
        return user.is_staff

class PatientDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    def get_success_url(self):
        return reverse('recp-home')

    template_name = 'recp/user_confirm_delete.html'
    def test_func(self):
        user = self.request.user
        user_to_delete = self.get_object()
        if user.is_staff and user_to_delete.profile.registered_as=='Patnt':
            return True
        return False

# core/views.py
def results_view(request):
    ctx = {}
    url_parameter = request.GET.get("q")

    if url_parameter:
        results = User.objects.filter(first_name__icontains=url_parameter)
    else:
        results = User.objects.all()

    ctx["results"] = results

    if request.is_ajax():
        html = render_to_string(
            template_name="recp/search_result.html", 
            context={"results": results}
        )

        data_dict = {"html_from_view": html}

        return JsonResponse(data=data_dict, safe=False)

    return render(request, "recp/search.html", context=ctx)    