from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Sum
from donation.models import Bag, Institution
from django.urls import reverse

class LandingPage(View):
    def get(self, request):
        total_bags = Bag.objects.aggregate(Sum('quantity'))['quantity__sum'] or 0
        total_institutions = Institution.objects.count()

        # Pobieranie instytucji z bazy danych i dodanie sortowania
        fundations_list = Institution.objects.filter(type='fundacja').order_by('id')
        organizations_list = Institution.objects.filter(type='organizacja pozarządowa').order_by('id')
        collections_list = Institution.objects.filter(type='zbiórka lokalna').order_by('id')

        # Paginacja
        paginator_fundations = Paginator(fundations_list, 5)
        paginator_organizations = Paginator(organizations_list, 5)
        paginator_collections = Paginator(collections_list, 5)

        page_number_fundations = request.GET.get('page_fundations', 1)
        page_number_organizations = request.GET.get('page_organizations', 1)
        page_number_collections = request.GET.get('page_collections', 1)

        fundations = paginator_fundations.get_page(page_number_fundations)
        organizations = paginator_organizations.get_page(page_number_organizations)
        collections = paginator_collections.get_page(page_number_collections)

        context = {
            'total_bags': total_bags,
            'total_institutions': total_institutions,
            'fundations': fundations,
            'organizations': organizations,
            'collections': collections,
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

    def post(self, request):
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            return render(request, 'register.html', {'error': 'Hasła muszą być takie same.'})

        if User.objects.filter(username=email).exists():
            return render(request, 'register.html', {'error': 'Użytkownik o podanym adresie email już istnieje.'})

        user = User.objects.create_user(username=email, email=email, password=password)
        user.first_name = name
        user.last_name = surname
        user.save()

        return redirect(reverse('login'))