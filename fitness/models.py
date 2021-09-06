from django.db import models as mo

from django.core.validators import MaxValueValidator, MinValueValidator

from account.models import Account
from .validators import *


from django.utils.timezone import now as today
from datetime import timedelta as td 




def tomorrow():
    return today() + td(days=1)




# Create your models here.



class TrainerRequest(mo.Model):
    trainer = mo.ForeignKey(Account,related_name='trainer_request', on_delete=mo.CASCADE)

    #trainer = mo.OneToOneField(Account,related_name='trainer_request', on_delete=mo.CASCADE)
    #client = mo.ForeignKey(Account,related_name='client_request', on_delete=mo.CASCADE)
    client = mo.OneToOneField(Account,related_name='client_request', on_delete=mo.CASCADE)
    
    
    
    def __str__(self):
        """String for representing the Model object."""
        return f'{self.client} ask {self.trainer} to be his trainer.'


class WeightAtDate(mo.Model):
    weight = mo.FloatField(validators = [MinValueValidator(30), MaxValueValidator(350)]) #In kg
    date = mo.DateField(default=today) 
    user = mo.ForeignKey(Account, on_delete=mo.CASCADE)

    class Meta:
        ordering = ['user' ,'-date']
    
    def __str__(self):
        """String for representing the Model object."""
        return f'On {self.date}, {self.user} has {self.weight} kg.'


class Day(mo.Model):
    '''Model representing a day of trining and alimantation. '''
    user = mo.ForeignKey(Account, on_delete=mo.CASCADE)
    date = mo.DateField(default=tomorrow, validators=[validate_date])

    description = mo.TextField(max_length=1000, help_text='Enter a brief description of the training day.', null=1, blank=1)
    duration = mo.DurationField(null=1, blank=1)


    class Meta:
        unique_together = [['user', 'date']]



    def __str__(self):
        """String for representing the Model object."""
        return f'{self.date}'

    



class Exercise(mo.Model):
    '''Model representing an exercise. '''

    trainer = mo.ForeignKey(Account, on_delete=mo.CASCADE, validators=[validate_trainer])
    name = mo.CharField(max_length=50)
    description = mo.TextField(max_length=1000, help_text='Enter a brief description of the exercise.', null=1, blank=1)
    tutorial = mo.FileField(upload_to='tutorials/', null=1, blank=1)

    PRIORITY = (
        (1, 'Start'),
        (2, 'Middle'),
        (3, 'End'),
    )
    priority = mo.IntegerField(choices=PRIORITY)
    
    class Meta:
        ordering = ['priority']

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.name}'



class ExerciseInstance(mo.Model):
    ''' Model representing a specific performance of a exercise. '''
    
    
    exercise = mo.ForeignKey(Exercise, on_delete=mo.CASCADE)
    day = mo.ForeignKey(Day, on_delete=mo.CASCADE)
    performance = mo.FileField(upload_to='performaces/', null=1, blank=1)
    review = mo.TextField(max_length=1000, help_text='Enter a review of the performance.', null=1, blank=1)



    class Meta:
        ordering = ['exercise', 'day']
        unique_together = [['day', 'exercise']]

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.exercise.name} for {self.day.user} on {self.day}'


class OwnExercise(mo.Model):
    exercise = mo.CharField(max_length=50)
    day = mo.ForeignKey(Day, on_delete=mo.CASCADE)
    performance = mo.FileField(upload_to='performaces/', null=1, blank=1)


    def __str__(self):
        """String for representing the Model object."""
        return f'{self.exercise} on {self.day}'

class Set(mo.Model):
    '''Model representing a set of a exercise. '''

    #Some exercizes don't require the use of aditional weight. Ex pushupps.
    weight = mo.FloatField(validators = [MinValueValidator(0)]) 
    repetitions = mo.IntegerField(validators = [MinValueValidator(1)])

    #exercise = models.ForeignKey(ExerciseInstance, on_delete=models.CASCADE)

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.repetitions}x{self.weight}'


class SetPair(mo.Model):

    exercise = mo.ForeignKey(ExerciseInstance, on_delete=mo.CASCADE, default=None)


    given_set = mo.OneToOneField(Set,related_name='given_set', on_delete=mo.CASCADE)
    done_set = mo.OneToOneField(Set,related_name='done_set', on_delete=mo.SET_NULL,  null=1, blank=1)
    
    def __str__(self):
        """String for representing the Model object."""
        return f'{self.given_set}\n{self.done_set}'



class OwnSet(mo.Model):

    exercise = mo.ForeignKey(OwnExercise, on_delete=mo.CASCADE, default=None)
    set = mo.OneToOneField(Set, on_delete=mo.CASCADE)
    def __str__(self):
        """String for representing the Model object."""
        return f'{self.set}'




def instnce_to_own(instance: ExerciseInstance):
    own = OwnExercise(name=instance.exercise.name, day=instance.day, performance=instance.performance)
    own.save()

    set_pairs = instance.setpairs_set

    for pair in set_pairs:
        own_set = OwnSet(exercise=own, set=pair.done_set)
        own_set.save()

        pair.delete()

    instance.delete()