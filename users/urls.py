from django.urls import path
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views as user_views
from .views import *


urlpatterns = [
	path('login_success/', user_views.login_success, name='login-success'),
	path('login/', auth_views.LoginView.as_view(template_name='hm/base.html'), name='login'),
    path('register/', user_views.register, name='register'),
    path('logout/', user_views.logout_page, name='logout'),
    path('profile/', user_views.profile, name='profile'),
    path('upadte_profile/', user_views.updateprofile, name='update-profile'),


]
