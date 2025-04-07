from django import forms
from .models import CustomUser

class ResidentRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'student_id', 'move_in_date']

class CheckInForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['check_in_status']