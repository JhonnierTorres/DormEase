from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.views import View
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, UpdateView, DeleteView

from . import models, forms

# Create your views here.

User = get_user_model()

# Admin Dashboard View
class AdminDashboardView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.role != 'superuser':
            return redirect('home')  # restrict access

        users = models.CustomUser.objects.all()
        return render(request, 'users/admin_dashboard.html', {'users': users})

# RA Dashboard View with check-in functionality
class RADashboardView(LoginRequiredMixin, View):
    def get(self, request):
        residents = models.CustomUser.objects.filter(role='resident')
        rooms = models.Room.objects.all()
        checkin_forms = {resident.id: forms.CheckInForm(instance=resident) for resident in residents}
        return render(request, 'users/dashboard.html', {
            'residents': residents,
            'rooms': rooms,
            'checkin_forms': checkin_forms
        })

    def post(self, request):
        resident_id = request.POST.get('resident_id')
        resident = models.CustomUser.objects.get(id=resident_id)
        form = forms.CheckInForm(request.POST, instance=resident)
        if form.is_valid():
            form.save()
        return redirect('ra-dashboard')

# Resident Dashboard View
class ResidentDashboardView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        if user.role != 'resident':
            return redirect('ra-dashboard')
        room = user.assigned_room
        return render(request, 'users/resident_dashboard.html', {'user': user, 'room': room})


# Resident Registration View
class ResidentRegistrationView(View):

    def get(self, request):
        form = forms.ResidentRegistrationForm()
        return render(request, 'users/register.html', {'form': form})
    
    def post(self, request):
        form = forms.ResidentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.role = 'resident'
            user.save()

            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login')
        return render(request, 'users/register.html', {'form': form})

# Room Assignment View
class RoomAssignmentView(View):
    def get(self, request):
        residents = models.CustomUser.objects.filter(role='resident', assigned_room=None)
        rooms = models.Room.objects.all()
        return render(request, 'users/assign_room.html', {'residents': residents, 'rooms': rooms})

    def post(self, request):
        resident_id = request.POST.get('resident_id')
        room_id = request.POST.get('room_id')
        resident = models.CustomUser.objects.get(id=resident_id)
        room = models.Room.objects.get(id=room_id)

        if not room.is_full():
            room.occupants.add(resident)
            return redirect('ra-dashboard')
        return render(request, 'users/assign_room.html', {'error': 'Room is full'})

# Login View
class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        user = self.request.user
        if user.role == 'resident':
            return reverse('resident-dashboard')
        elif user.role == 'ra':
            return reverse('ra-dashboard')
        elif user.role == 'superuser':
            return reverse('admin-dashboard')
        else:
            return reverse('home')  # fallback in case of undefined role

# Home View
class HomeView(TemplateView):
    template_name = 'users/home.html'

# Password Reset View
class PasswordResetView(TemplateView):
    template_name = 'users/password_reset.html'

class RoomCreateView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.role != 'superuser':
            return redirect('home')
        form = forms.RoomForm()
        return render(request, 'users/add_room.html', {'form': form})

    def post(self, request):
        # Single room creation
        form = forms.RoomForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Room created successfully')
            return redirect('room-list')
        return render(request, 'users/add_room.html', {'form': form, 'bulk_mode': False})
    
# Room List View
class RoomListView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.role not in ['ra', 'superuser']:
            return redirect('home')
        rooms = models.Room.objects.all().order_by('room_number')
        return render(request, 'users/room_list.html', {'rooms': rooms})

# Room Edit View
class RoomEditView(LoginRequiredMixin, UpdateView):
    model = models.Room
    form_class = forms.RoomForm
    template_name = 'users/edit_room.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.role not in ['ra', 'superuser']:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('room-list')

# Room Delete View
class RoomDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Room
    template_name = 'users/delete_room.html'
    success_url = reverse_lazy('room-list')

    def dispatch(self, request, *args, **kwargs):
        if request.user.role not in ['ra', 'superuser']:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)
    

