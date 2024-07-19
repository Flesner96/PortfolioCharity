from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View
from django.db.models import Sum
from donation.models import Bag, Institution

class LandingPage(View):
    def get(self, request):
        total_bags = Bag.objects.aggregate(Sum('quantity'))['quantity__sum'] or 0
        total_institutions = Institution.objects.count()

        # Pobieranie instytucji z bazy danych
        fundations_list = Institution.objects.filter(type='fundacja')
        organizations_list = Institution.objects.filter(type='organizacja pozarządowa')
        collections_list = Institution.objects.filter(type='zbiórka lokalna')

        # Paginacja
        paginator_fundations = Paginator(fundations_list, 5)
        paginator_organizations = Paginator(organizations_list, 5)
        paginator_collections = Paginator(collections_list, 5)

        page_number_fundations = request.GET.get('page_fundations') or 1
        page_number_organizations = request.GET.get('page_organizations') or 1
        page_number_collections = request.GET.get('page_collections') or 1

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