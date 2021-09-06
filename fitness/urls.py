from django.contrib import admin
from django.urls import path

from . import views as v


urlpatterns = [
    path('', v.index, name='index'),
    path('exercises-list/', v.exercises_list, name='exercises-list'),
    path('create-exercise/', v.create_exercise, name='create-exercise'),
    path('exercise-detail/<int:id>', v.exercise_detail, name='exercise-detail'),
    path('delete-exercise/', v.delete_exercise, name='delete-exercise'),
    path('edit-exercise/<int:id>', v.edit_exercise, name='edit-exercise'),

   

    path('weight-progression/', v.weight_progression, name='weight-progression'),
    path('delete-weight/<int:id>', v.delete_weight_date, name='delete-weight'),

]

urlpatterns += [ 
    path('trainer-request/', v.trainer_request, name='trainer-request'),
    path('trainers-list/', v.trainers_list, name='trainers-list'),
    path('my-clients/', v.my_clients, name='my-clients'),
    path("profile/<int:id>", v.profile, name="profile"),
    path('my-account/', v.my_account, name='my-account'),
    
    #path('create-exercise-instance/', v.create_exercise_intstance, name='create-exercise-instance'),
    path('create-day/', v.create_day, name='create-day'),
    path('day-list/', v.day_list, name='day-list'),
    path('day-list/<int:id>', v.day_list_trainer, name='day-list-trainer'),
    path('add-day/<int:id>', v.add_day, name='add-day'),
    path('day-detail/<int:id>', v.day_detail, name='day-detail'),

    path('add-exercise-instance/<int:id>', v.add_exercise_intstance, name='add-exercise-instance'),
    path('add-given-set/<int:id>', v.add_given_set, name='add-given-set'),
    path('add-done-set/<int:id>', v.add_done_set, name='add-done-set'),

    path('trainer-response/', v.trainer_response, name='trainer-response'),
    path('trainer-response-yes/', v.trainer_response_yes, name='trainer-response-yes'),
    path('trainer-response-no/', v.trainer_response_no, name='trainer-response-no'),
    path('cancel-request/', v.cancel_request, name='cancel-request'),

    path('edit-profile/', v.edit_profile, name='edit-account'),

    path('exercise-instance-detail/<int:id>', v.exercise_instance_detail, name='exercise-instance-detail'),
    path('add-review/<int:id>', v.add_review, name='add-review'),
    path('add-performance/<int:id>', v.add_performance, name='add-performance'),

    ]