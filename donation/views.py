from django.shortcuts import render
from django.views import View
from django.db.models import Sum
from donation.models import Bag, Institution

class LandingPage(View):
    def get(self, request):
        total_bags = Bag.objects.aggregate(Sum('quantity'))['quantity__sum'] or 0
        total_institutions = Institution.objects.count()
        context = {
            'total_bags': total_bags,
            'total_institutions': total_institutions,
        }
        return render(request, 'index.html', context)
class AddDonation(View):
    def get(self, request):
        return render(request, 'form.html')

class Login(View):
    def get(self, request):
        return render(request, 'login.html')

class Register(View):
    def get(self, request):
        return render(request, 'register.html')