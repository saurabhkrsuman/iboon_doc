from django.urls import path
from .views import (
    CustomUserView,
    LoginAPIView,
    PatientCreateAPIView,
    PatientListAPIView,
    PatientUpdateAPIView,
    PrescriptionCreateAPIView,
    PrescriptionListAPIView
)


urlpatterns = [
    path('user/', CustomUserView.as_view(), name="user_register"),
    path('api/login/', LoginAPIView.as_view(), name='login'),
    path('patients/', PatientListAPIView.as_view(), name='patient-list'),
    path('patients/create/', PatientCreateAPIView.as_view(), name='patient-create'),
    path('patients/<int:pk>/update/', PatientUpdateAPIView.as_view(), name='patient-update'),
    path('prescriptions/create/', PrescriptionCreateAPIView.as_view(), name='prescription-create'),
    path('prescriptions/<int:patient_id>/', PrescriptionListAPIView.as_view(), name='prescription-list'),
]
