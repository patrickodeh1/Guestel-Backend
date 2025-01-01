from django import forms
from django.contrib.auth.models import User
from .models import Hotel

class UserRegistrationForm(forms.ModelForm):
  """
  Form for user registration.
  """
  password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
  password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

  class Meta:
    model = User
    fields = ('first_name', 'last_name', 'email', 'phone_number', 'password1', 'password2')

  def clean_password2(self):
    """
    Ensures both password fields match.
    """
    password1 = self.cleaned_data.get('password1')
    password2 = self.cleaned_data.get('password2')
    if password1 and password2 and password1 != password2:
      raise forms.ValidationError('Passwords don\'t match.')
    return password2

  def save(self, commit=True):
    """
    Hashes the password before saving the user.
    """
    user = super().save(commit=False)
    user.set_password(self.cleaned_data['password1'])
    if commit:
      user.save()
    return user

class HotelRegistrationForm(forms.ModelForm):
  """
  Form for hotel profile creation.
  """

  class Meta:
    model = Hotel
    fields = ('name', 'address', 'description', 'phone_number', 'email', 'logo', 'amenities')

  def __init__(self, *args, **kwargs):
    super(HotelRegistrationForm, self).__init__(*args, **kwargs)
    self.fields['amenities'].widget = forms.CheckboxSelectMultiple()