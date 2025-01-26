from django.urls import path

from .views import LoginView, PatientListView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('patients/', PatientListView.as_view(), name='patient')
]

