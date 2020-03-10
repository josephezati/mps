from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from hm.models import * 

class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	photo = models.ImageField(default='user_photos/default.png', upload_to='user_photos', blank=True, null=True,)
	address = models.CharField(max_length=200, blank=True, null=True)
	phone = models.CharField(max_length=200, blank=True, null=True)
	staff = models.OneToOneField(Staff, on_delete=models.CASCADE, blank=True, null=True)
	updated = models.DateTimeField(auto_now=True)
	def __str__(self):
		return f'{self.user.first_name} {self.user.last_name}'

class ParentProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	parent = models.OneToOneField(Parent, on_delete=models.CASCADE, blank=True, null=True)
	def __str__(self):
		return f'{self.user.first_name} {self.user.last_name}'
