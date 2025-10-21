from django import forms
from .models import Farmer

class FarmerForm(forms.ModelForm):
    class Meta:
        model = Farmer
        fields = ['name', 'farm', 'phone', 'email', 'gender', 'employment_type']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter farmer full name',
                'required': True
            }),
            'farm': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter farm name',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter phone number',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email address',
                'required': True
            }),
            'gender': forms.RadioSelect(attrs={
                'class': 'form-check-input'
            }),
            'employment_type': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
        labels = {
            'name': 'Full Name',
            'farm': 'Farm Name',
            'phone': 'Phone Number',
            'email': 'Email Address',
            'gender': 'Gender',
            'employment_type': 'Employment Type',
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and len(phone) < 10:
            raise forms.ValidationError("Phone number must be at least 10 digits long.")
        return phone

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            # Check if email already exists (excluding current instance if updating)
            existing = Farmer.objects.filter(email=email)
            if self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)
            if existing.exists():
                raise forms.ValidationError("A farmer with this email already exists.")
        return email