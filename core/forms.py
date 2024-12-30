from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Hotel


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class EstablishmentRegistrationForm(UserCreationForm):
    establishment_name = forms.CharField(max_length=255, required=True)
    address = forms.CharField(widget=forms.Textarea, required=True)
    phone_number = forms.CharField(max_length=20, required=True)

    class Meta:
        model = get_user_model()
        fields = ['username', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            Hotel.objects.create(
                user=user,
                name=self.cleaned_data['establishment_name'],
                address=self.cleaned_data['address'],
                phone_number=self.cleaned_data['phone_number']
            )
        return user
