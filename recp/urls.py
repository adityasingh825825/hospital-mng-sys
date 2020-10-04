from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='recp-home'),
    path('profile-view/<int:id>', views.profile_view, name='profile_view'),
    path('profile-view/<int:pk>/delete/', views.PatientDeleteView.as_view(), name='patient_delete'),
    path('create-appointment/', views.AppointmentCreateView.as_view(), name='create_appointment'),
    path('search/', views.results_view, name='search')

]