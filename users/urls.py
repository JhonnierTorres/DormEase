from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterUserView.as_view(), name='register'),
    path('ra-dashboard/', views.RADashboardView.as_view(), name='ra-dashboard'),
]

