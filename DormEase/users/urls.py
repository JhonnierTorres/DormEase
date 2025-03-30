from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('register/', views.ResidentRegistrationView.as_view(), name='register'),
    path('dashboard/', views.RADashboardView.as_view(), name='ra-dashboard'),
    path('assign-room/', views.RoomAssignmentView.as_view(), name='assign-room'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('', views.HomeView.as_view(), name='home'),
]

