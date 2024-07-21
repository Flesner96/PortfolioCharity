from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm

class UserUpdateForm(forms.ModelForm):
    password = forms.CharField(label='Potwierdź hasło', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def clean_password(self):
        password = self.cleaned_data['password']
        if not self.instance.check_password(password):
            raise forms.ValidationError('Niepoprawne hasło')
        return password

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='Stare hasło', widget=forms.PasswordInput)
    new_password1 = forms.CharField(label='Nowe hasło', widget=forms.PasswordInput)
    new_password2 = forms.CharField(label='Potwierdź nowe hasło', widget=forms.PasswordInput)
