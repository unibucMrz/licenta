from django import forms
from django.contrib.auth import login, authenticate


from django.core.validators import MaxValueValidator, MinValueValidator
'''
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User




class SignUpForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)

    height = forms.IntegerField(validators = [MinValueValidator(120), MaxValueValidator(230)], help_text='Enter your height in centimetres.') #In centimetres.
    
    birth_date = forms.DateField()

    class Meta:
        model = User
        fields = ["email","first_name",'last_name','height','birth_date', "password1", "password2"]

'''


from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from account.models import Account

YEARS = [y for y in range(1940,2012)]

class DateInput(forms.DateInput):
    input_type = 'date'


class SignUpForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)

    height = forms.IntegerField(validators = [MinValueValidator(120), MaxValueValidator(230)], help_text='Enter your height in centimetres.', required=False) 
    weight = forms.FloatField(validators = [MinValueValidator(30), MaxValueValidator(350)], help_text='Enter your weight in kilograms.', required=False) 
    
    
    profile_picture = forms.ImageField(required=False)
   
    
    gender = forms.ChoiceField(choices=Account.GENDER)
    '''
    birth_date = forms.DateField(
        widget=forms.SelectDateWidget(years=YEARS),
       input_formats=['%d/%m/%Y'], 
       required=False
    )
    '''
    is_trainer = forms.BooleanField(required=False, label='Trainer')
    class Meta:
        model = Account
        fields = ["email","first_name",'last_name','profile_picture','gender','weight','height','birth_date','about','quote', "password1", "password2",'is_trainer']

        widgets = {
            'birth_date' : DateInput()
        }


class EditAccoutForm(UserChangeForm):
    '''
    birth_date = forms.DateField(
        widget=forms.SelectDateWidget(years=YEARS),
       input_formats=['%d/%m/%Y'], 
       required=False
    )
    '''

    #birth_date = DateInput()
    class Meta:
        model = Account
        fields = ["first_name",'last_name','profile_picture','gender','height','birth_date','about','quote','is_trainer']

        widgets = {
            'birth_date' : DateInput()
        }

