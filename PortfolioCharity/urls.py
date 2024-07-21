"""
URL configuration for PortfolioCharity project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from donation.views import LandingPage, Login, Register, logout_view, AddDonationView, FormConfirmationView, \
    user_profile, toggle_donation_status, user_settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LandingPage.as_view(), name='landing-page'),
    path('add-donation/', AddDonationView.as_view(), name='add-donation'),
    path('form-confirmation/', FormConfirmationView.as_view(), name='form-confirmation'),
    path('login/', Login.as_view(), name='login'),
    path('register/', Register.as_view(), name='register'),
    path('logout/', logout_view, name='logout'),
    path('toggle-donation-status/<int:donation_id>/', toggle_donation_status, name='toggle-donation-status'),
    path('profile/', user_profile, name='user-profile'),
    path('settings/', user_settings, name='user-settings'),
]