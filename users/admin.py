from django.contrib import admin
from .models import *
from django.db import models
admin.site.register( UserProfile )
admin.site.register( ParentProfile )