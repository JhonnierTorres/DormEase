from django import forms
from .models import CustomUser, Room

# Resident Registration Form
class ResidentRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'student_id', 'move_in_date']

# RA Check-In Form
class CheckInForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['check_in_status']

# Room Assignment Form
class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_number', 'room_type', 'capacity']
