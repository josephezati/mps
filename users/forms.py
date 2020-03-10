from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *

class UserRegisterForm(UserCreationForm):
	email = forms.EmailField()
	first_name = forms.CharField(max_length=200)
	last_name = forms.CharField(max_length=200)
	class Meta:
		model = User
		fields = ['first_name','last_name','username','email','password1','password2']

class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField()
	first_name = forms.CharField(max_length=200)
	last_name = forms.CharField(max_length=200)
	class Meta:
		model = User
		fields = ['first_name','last_name','username','email']

class UserProfileUpdateForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ['address','phone','photo']