from django.contrib import admin

# Register your models here.
from .models import *


@admin.register(TrainerRequest)
class TrainerRequestAdmin(admin.ModelAdmin):
    pass




@admin.register(Day)
class DayAdmin(admin.ModelAdmin):
    list_display = ['user','date','duration']

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(ExerciseInstance)
class ExerciseInstanceAdmin(admin.ModelAdmin):
    list_display = ['exercise','day']



@admin.register(OwnExercise)
class OwnExerciseAdmin(admin.ModelAdmin):
    list_display = ['exercise','day']

@admin.register(Set)
class SetAdmin(admin.ModelAdmin):
    list_display = ['repetitions', 'weight']


@admin.register(SetPair)
class SetPairAdmin(admin.ModelAdmin):
    list_display = ['given_set', 'done_set']

@admin.register(OwnSet)
class OwbSetAdmin(admin.ModelAdmin):
    list_display = ['set']

@admin.register(WeightAtDate)
class SetAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'weight']

from account.models import Account

admin.site.register(Account)