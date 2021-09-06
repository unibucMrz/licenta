from django import forms
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.forms import fields
from django.utils.timezone import now

from .models import *
'''
class CreateExercise(forms.Form):
    name = forms.CharField(max_length=50)
    description = forms.CharField(widget=forms.Textarea, max_length=1000, help_text='Enter a brief description of the exercise.',  required=False)
    tutorial = forms.FileField(required=False)

    PRIORITY = (
        (1, 'Start'),
        (2, 'Middle'),
        (3, 'End'),
    )
    priority = forms.ChoiceField(choices=PRIORITY)
'''


class CreateExercise(forms.ModelForm):
     class Meta:
       model = Exercise
       exclude = ['trainer']

class AddWeight(forms.Form):
    weight = forms.FloatField(validators = [MinValueValidator(30), MaxValueValidator(350)], help_text='Enter your weight in kilograms.')
    #date = forms.DateField(widget = forms.HiddenInput(), initial=now) 



class AddExerciseInstance(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        #day = kwargs.pop('day')
        super(AddExerciseInstance, self).__init__(*args, **kwargs)

        self.fields['exercise'] = forms.ModelChoiceField(
                required=True,
                queryset=user.exercise_set.all(),
                #widget=forms.SelectMultiple(attrs={'title': ("Add unit")})

        )

       

    class Meta:
        model = ExerciseInstance
        fields = ['exercise', 'day']
        widgets = {'day': forms.HiddenInput()}


class DateInput(forms.DateInput):
    input_type = 'date'

class CreateDay(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(CreateDay, self).__init__(*args, **kwargs)

        self.fields['user'] = forms.ModelChoiceField(
                required=True,
                queryset=user.account_set.all(),

        )
    
    class Meta:
        model = Day
        fields = '__all__'
        

        
        widgets = {
            'date' : DateInput()
        }

    

class AddDay(forms.ModelForm):
    class Meta:
        model = Day
        exclude = ['user']
        
        widgets = {
            'date' : DateInput()
        }



class CreateSet(forms.Form):
    weight = forms.FloatField(validators = [MinValueValidator(0)]) #Some exercizes don't require the use of aditional weight. Ex pushupps.
    repetitions = forms.IntegerField(validators = [MinValueValidator(1)])


class AddReview(forms.Form):
    review = forms.CharField(max_length=1000, help_text='Enter a review of the performance.',widget=forms.Textarea)


class AddPerformance(forms.Form):
    performance = forms.FileField()

class SelectDate(forms.Form):
    month = forms.IntegerField(min_value=1,max_value=12)
    year = forms.IntegerField(required=0)