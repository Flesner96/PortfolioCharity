from django.contrib.auth import authenticate, login as auth_login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.db.models import Sum
from django.views.decorators.http import require_POST

from donation.forms import UserUpdateForm, CustomPasswordChangeForm
from donation.models import Bag, Institution, Category, Donation
from django.urls import reverse
from django.contrib import messages

class LandingPage(View):
    def get(self, request):
        total_bags = Bag.objects.aggregate(Sum('quantity'))['quantity__sum'] or 0
        total_institutions = Institution.objects.count()

        fundations_list = Institution.objects.filter(type='fundacja').order_by('id')
        organizations_list = Institution.objects.filter(type='organizacja pozarządowa').order_by('id')
        collections_list = Institution.objects.filter(type='zbiórka lokalna').order_by('id')

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


class Login(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect(reverse('landing-page'))
        else:
            if not User.objects.filter(username=email).exists():
                return redirect(reverse('register'))
            return render(request, 'login.html', {'error': 'Nieprawidłowy email lub hasło.'})


def logout_view(request):
    logout(request)
    return redirect(reverse('landing-page'))


@method_decorator(login_required, name='dispatch')
class AddDonationView(View):
    def get(self, request):
        categories = Category.objects.all()
        institutions = Institution.objects.all()
        return render(request, 'form.html', {'categories': categories, 'institutions': institutions})

    def post(self, request):
        try:
            bags = request.POST.get('bags')
            organization_id = request.POST.get('organization')
            address = request.POST.get('address')
            city = request.POST.get('city')
            postcode = request.POST.get('postcode')
            phone = request.POST.get('phone')
            pick_up_date = request.POST.get('data')
            pick_up_time = request.POST.get('time')
            pick_up_comment = request.POST.get('more_info')
            categories = request.POST.getlist('categories')

            # Pobranie instytucji i kategorii
            institution = Institution.objects.get(id=organization_id)
            categories_objects = Category.objects.filter(id__in=categories)

            # Utworzenie nowej darowizny
            donation = Donation.objects.create(
                quantity=bags,
                institution=institution,
                address=address,
                phone_number=phone,
                city=city,
                zip_code=postcode,
                pick_up_date=pick_up_date,
                pick_up_time=pick_up_time,
                pick_up_comment=pick_up_comment,
                user=request.user,
            )

            # Dodanie kategorii do darowizny
            donation.categories.set(categories_objects)
            donation.save()

            return redirect('form-confirmation')

        except Institution.DoesNotExist:
            return redirect('add-donation')
        except Exception as e:
            return render(request, 'form.html',
                          {'categories': Category.objects.all(), 'institutions': Institution.objects.all(),
                           'error': str(e)})


class FormConfirmationView(View):
    def get(self, request):
        return render(request, 'form-confirmation.html')


@login_required
def user_profile(request):
    donations = Donation.objects.filter(user=request.user).select_related('institution').prefetch_related(
        'categories').order_by('is_taken', 'pick_up_date')
    return render(request, 'user_profile.html', {
        'user': request.user,
        'donations': donations
    })


@require_POST
@login_required
def toggle_donation_status(request, donation_id):
    try:
        donation = Donation.objects.get(id=donation_id, user=request.user)
        donation.is_taken = not donation.is_taken
        donation.save()
    except Donation.DoesNotExist:
        pass
    return redirect('user-profile')


@login_required
def user_settings(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        password_form = CustomPasswordChangeForm(request.user, request.POST)

        if 'update_profile' in request.POST:
            if user_form.is_valid():
                user_form.save()
                messages.success(request, 'Twoje dane zostały zaktualizowane.')
                return redirect('user-settings')
        elif 'change_password' in request.POST:
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  # Pozostanie zalogowanym po zmianie hasła
                messages.success(request, 'Twoje hasło zostało zaktualizowane.')
                return redirect('user-settings')
    else:
        user_form = UserUpdateForm(instance=request.user)
        password_form = CustomPasswordChangeForm(request.user)

    return render(request, 'user_settings.html', {
        'user_form': user_form,
        'password_form': password_form
    })