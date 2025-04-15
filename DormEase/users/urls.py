from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('ra-dashboard/', views.RADashboardView.as_view(), name='ra-dashboard'),
    path('admin-dashboard/', views.AdminDashboardView.as_view(), name='admin-dashboard'),
    path('dashboard/stats/', views.StatsView.as_view(), name='dashboard-stats'),
    path('resident-dashboard/', views.ResidentDashboardView.as_view(), name='resident-dashboard'),
    path('assign-room/', views.RoomAssignmentView.as_view(), name='assign-room'),
    path('unassign-resident/<int:resident_id>/', views.UnassignResidentView.as_view(), name='unassign-resident'),
    path('add-room/', views.RoomCreateView.as_view(), name='add-room'),
    path('room-list/', views.RoomListView.as_view(), name='room-list'),
    path('rooms/<int:pk>/edit/', views.RoomEditView.as_view(), name='edit-room'),
    path('rooms/<int:pk>/delete/', views.RoomDeleteView.as_view(), name='delete-room'),
    path('register/', views.ResidentRegistrationView.as_view(), name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('password-reset/', views.PasswordResetView.as_view(), name='password_reset'),
    
]

