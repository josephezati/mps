from django.db.models.signals import post_save
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import *

@receiver(post_save, sender=User)
def create_userprifile(sender, instance, created, **kwargs):
	if created:
		UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_userprifile(sender, instance, **kwargs):
	try:
		instance.userprofile.save()
	except ObjectDoesNotExist:
		UserProfile.objects.create(user=instance)