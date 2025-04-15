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
            return redirect('home')
        all_users = models.CustomUser.objects.exclude(id=request.user.id)
        def room_sort_key(user):
            if user.assigned_room.exists():
                # Get the first room's number if they have one or more
                return (0, user.assigned_room.first().room_number.lower())
            return (1, '')  # Users without a room come later
        users = sorted(all_users, key=room_sort_key)
        return render(request, 'users/admin_dashboard.html', {'users': users})

    def post(self, request):
        if request.user.role != 'superuser':
            return redirect('home')

        user_id = request.POST.get('user_id')
        action = request.POST.get('action')
        role = request.POST.get('new_role')

        try:
            user = models.CustomUser.objects.get(id=user_id)

            if action == 'change_role' and role in ['resident', 'ra', 'superuser']:
                user.role = role
                user.save()
            elif action == 'deactivate':
                user.is_active = not user.is_active  # toggle activation
                user.save()

            elif action == 'delete':
                user.delete()

        except models.CustomUser.DoesNotExist:
            pass

        return redirect('admin-dashboard')

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
        resident_id = request.GET.get('resident')
        selected_resident = None

        if resident_id:
            try:
                selected_resident = models.CustomUser.objects.get(id=resident_id, role='resident')
            except models.CustomUser.DoesNotExist:
                selected_resident = None

        residents = models.CustomUser.objects.filter(role='resident', assigned_room=None)
        rooms = models.Room.objects.all()

        return render(request, 'users/assign_room.html', {
            'residents': residents,
            'rooms': rooms,
            'selected_resident': selected_resident
        })

    def post(self, request):
        resident_id = request.POST.get('resident_id')
        room_id = request.POST.get('room_id')

        try:
            resident = models.CustomUser.objects.get(id=resident_id, role='resident')
            room = models.Room.objects.get(id=room_id)

            if not room.is_full():
                room.occupants.add(resident)
                return redirect('admin-dashboard')  # or 'ra-dashboard' depending on role

            # Room is full
            error = 'Room is full'
        except models.CustomUser.DoesNotExist:
            error = 'Resident not found'
        except models.Room.DoesNotExist:
            error = 'Room not found'

        # Re-render form with error
        residents = models.CustomUser.objects.filter(role='resident', assigned_room=None)
        rooms = models.Room.objects.all()
        return render(request, 'users/assign_room.html', {
            'residents': residents,
            'rooms': rooms,
            'error': error
        })

# Unassign Resident View in the admin dashboard
class UnassignResidentView(LoginRequiredMixin, View):
    def post(self, request, resident_id):
        if request.user.role not in ['ra', 'superuser']:
            return redirect('home')

        try:
            resident = models.CustomUser.objects.get(id=resident_id)
            for room in resident.assigned_room.all():
                room.occupants.remove(resident)
        except models.CustomUser.DoesNotExist:
            pass
        return redirect('admin-dashboard')  # Or 'ra-dashboard' based on context


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

# Room Create View
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

        all_rooms = models.Room.objects.all()
        # Sort rooms by room_number alphabetically (supports alphanumeric values)
        rooms = sorted(all_rooms, key=lambda room: room.room_number.lower())
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
    

