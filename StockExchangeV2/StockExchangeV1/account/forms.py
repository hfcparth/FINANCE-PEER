from django import forms
from django.contrib.auth.forms import UserCreationForm
from account.models import Account
from django.contrib.auth import authenticate

class RegistrationForm(UserCreationForm):
    email= forms.EmailField(max_length=60,help_text='Required add a valid email')
    adhar=forms.CharField(max_length=12,min_length=10,help_text='aadhar is maindatry')
    first_name=forms.CharField(max_length=30,help_text='enter name')
    last_name=forms.CharField(max_length=30,help_text='enter last name')
    class Meta:
        model = Account
        fields = ('email','adhar','first_name','last_name')

class LoginForm(forms.ModelForm):
    password=forms.CharField(label='password',widget=forms.PasswordInput)

    class Meta:
        model=Account
        fields = ('email','password')

    def clean(self):
        email=self.cleaned_data['email']
        password=self.cleaned_data['password']
        if not authenticate(email=email,password=password):
            raise forms.ValidationError("Invalid login")
