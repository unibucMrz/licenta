from django.core.exceptions import PermissionDenied
from django.db.models.query import QuerySet
from django.http.response import HttpResponse
from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.urls import reverse
from .forms import *
from .models import *

from django.db import IntegrityError

from register.forms import EditAccoutForm

from django.utils.timezone import now
from django.core.paginator import Paginator

from django.views.decorators.http import require_http_methods

from django.db.models import Q 


from django.views.generic.list import *
# Create your views here.



def paginate(request, list_object, number):
    paginator = Paginator(list_object, number)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return page_obj



def index(request):
    """View function for home page of site."""
    return render(request, 'index.html')



def create_exercise(request):
    user = request.user

    if not user.is_authenticated:
        return redirect('login')

    if not user.is_trainer:
        return redirect("index")


    if request.method == "POST":
        form = CreateExercise(request.POST, request.FILES)

        if form.is_valid():
            form_dict = form.cleaned_data
           

            name = form_dict['name']
            description = form_dict['description']
            tutorial = form_dict['tutorial']
            priority = form_dict['priority']
            
            exercise = Exercise(trainer=user,name=name, description=description, tutorial=tutorial, priority=priority)
            exercise.save()
            
            return redirect('exercises-list')

    form = CreateExercise()

    return render(request, 'fitness/create_exercise.html', {'form':form,'option':'Create'})




def edit_exercise(request, id):

    user = request.user

    if not user.is_authenticated:
        return redirect('login')

    if not user.is_trainer:
        return redirect("index")

    exercise = get_object_or_404(Exercise, pk=id)

    form = CreateExercise(None, instance=exercise)
    
    if request.method == "POST":
        form = CreateExercise(request.POST, request.FILES)

        if form.is_valid():
            form_dict = form.cleaned_data
           

            name = form_dict['name']
            description = form_dict['description']
            tutorial = form_dict['tutorial']
            priority = form_dict['priority']
            
            exercise.name = name
            exercise.description = description
            exercise.tutorial = tutorial
            exercise.priority = priority

            exercise.save()
            
            return redirect('exercises-list')


    form = CreateExercise(None, instance=exercise)

    return render(request, 'fitness/create_exercise.html', {'form':form,'option':'Save'})


@require_http_methods(["POST"])
def delete_exercise(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')

    if not user.is_trainer:
        return redirect("index")

    id = request.POST.get('id')
    exercise = get_object_or_404(user.exercise_set, pk=id)
    
    exercise.delete()
    
    return redirect('exercises-list')


def exercises_list(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')


    if user.is_trainer:
        exercises = user.exercise_set.all()
    elif user.trainer:
        exercises = user.trainer.exercise_set.all()
    else:
        return redirect('trainers-list')

    
    name = request.GET.get('name')    
    if name:
        exercises = exercises.filter(name__contains=name)

    exercises = exercises.order_by('priority')

    return render(request, 'fitness/exercises_list.html', {'exercises':paginate(request, exercises, 5)})

    
    
    

    
def exercise_detail(request, id):

    user = request.user
    if not user.is_authenticated:
        return redirect('login')
    

    if user.is_trainer:

        exercise = get_object_or_404(user.exercise_set, pk=id)
        #exercise = user.exercise_set.filter(pk=id)[0]
    elif user.trainer:
        exercise = get_object_or_404(user.trainer.exercise_set, pk=id)
        #exercise = user.trainer.exercise_set.filter(pk=id)[0]
    else :
        return redirect('trainers-list')

    return render(request, 'fitness/exercise_detail.html', {'exercise':exercise})


#NEW

def add_exercise_intstance(request, id):
    user = request.user

    if not user.is_authenticated:
        return redirect('login')

    if not user.is_trainer:
        return redirect("index")

    day = get_object_or_404(Day.objects, pk=id)
    if day.user.trainer != user:
        raise PermissionDenied  



    if request.method == "POST":
        form =AddExerciseInstance(request.POST, user=user)
        exercise = get_object_or_404(user.exercise_set, pk=form['exercise'].value())

        try:
            exercise_instance = ExerciseInstance(day=day, exercise=exercise)
            exercise_instance.save()
            return redirect('add-given-set', id=exercise_instance.id)

        except IntegrityError:
                return redirect(request.META.get('HTTP_REFERER', '/'))




    form = AddExerciseInstance(user=user)
    form.fields['day'].widget = forms.HiddenInput()
    
    return render(request, 'fitness/create_exercise_instance.html', {'form':form, 'day':day})




def add_given_set(request, id):
    user = request.user

    if not user.is_authenticated:
        return redirect('login')

    if not user.is_trainer:
        return redirect("index")

    exercise_instance = get_object_or_404(ExerciseInstance.objects, pk=id)

    if exercise_instance.day.user.trainer != user:
        raise PermissionDenied  

    if request.method == "POST":
        form = CreateSet(request.POST)

        if form.is_valid():
            form_dict = form.cleaned_data
            weight = form_dict['weight']
            repetitions = form_dict['repetitions']

            given_set = Set(weight=weight, repetitions=repetitions)
            given_set.save()

            set_pair = SetPair(exercise=exercise_instance, given_set=given_set)
            set_pair.save()
            return redirect(request.META.get('HTTP_REFERER', '/'))



    form = CreateSet()
    
    print(exercise_instance.setpair_set.all())

    return render(request, 'fitness/add_set.html', {'form':form, 'exercise':exercise_instance}) 






def create_day(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')

    if not user.is_trainer:
        return redirect("index")
   
    if request.method == "POST":
        form = CreateDay(request.POST, user=user)

        if form.is_valid():
            form_dict = form.cleaned_data
            
            client = form_dict['user']
            duration = form_dict['duration']
            date = form_dict['date']
            description = form_dict['description']


            day = Day(user=client, duration=duration, date=date, description=description)
            day.save()

            return redirect('add-exercise-instance', id=day.pk)


    form = CreateDay(user=user)


    return render(request, 'fitness/create_day.html', {'form':form})



def add_day(request, id):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')

    if not user.is_trainer:
        return redirect("index")
    
    client = get_object_or_404(user.account_set, pk=id)

    if request.method == "POST":
        form = AddDay(request.POST)

        if form.is_valid():
            form_dict = form.cleaned_data

            duration = form_dict['duration']
            date = form_dict['date']
            description = form_dict['description']

            try:
                day = Day(user=client, duration=duration, date=date, description=description)
                day.save()
                return redirect('add-exercise-instance', id=day.pk)

            except IntegrityError:
                return redirect(request.META.get('HTTP_REFERER', '/'))


    form = AddDay()

    return render(request, 'fitness/add_day.html', {'form':form, 'client':client})




def edit_profile(request):
    user = request.user

    if not user.is_authenticated:
        return redirect('login')
    
    if request.method == "POST":
        form = EditAccoutForm(request.POST, request.FILES)

        if form.is_valid():
            form_dict = form.cleaned_data

            user.first_name = form_dict['first_name']
            user.last_name = form_dict['last_name']
            user.gender = form_dict['gender']
            user.birth_date = form_dict['birth_date']
            user.height = form_dict['height']
            user.about = form_dict['about']
            user.quote = form_dict['quote']

            user.is_trainer = form_dict['is_trainer']

            user.save()

            return redirect('index')
            
    
    form = EditAccoutForm(None, instance=user)
    
    return render(request, 'fitness/edit_profile.html', {'form':form})





def day_detail(request, id):
    user = request.user

    if not user.is_authenticated:
        return redirect('login')

    day = get_object_or_404(Day, pk=id)

    
    if user == day.user:
        return render(request, 'fitness/day_detail.html', {'day':day})

    if user == day.user.trainer:
        return redirect('add-exercise-instance', id=id)



def exercise_instance_detail(request, id):
    user = request.user

    if not user.is_authenticated:
        return redirect('login')

    exercise = get_object_or_404(ExerciseInstance, pk=id)

    if user == exercise.day.user:

        form_performance = AddPerformance()
        form_performance.fields['performance'].initial = exercise.performance

        form_set = CreateSet()

        return render(request, 'fitness/exercise_instance_detail.html', {'exercise':exercise, 'form_performance':form_performance,  'form_set':form_set})

    if user == exercise.day.user.trainer:

        form_review = AddReview()
        form_review.fields['review'].initial = exercise.review

        form_set = CreateSet()
        return render(request, 'fitness/exercise_instance_detail_trainer.html', {'exercise':exercise, 'form_review':form_review, 'form_set':form_set})


@require_http_methods(["POST"])
def add_review(request, id):
    user = request.user

    if not user.is_authenticated:
        return redirect('login')

    exercise = get_object_or_404(ExerciseInstance, pk=id)
    form = AddReview(request.POST)

    if form.is_valid():
        exercise.review = form.cleaned_data['review']
        exercise.save()
    
    return redirect(request.META.get('HTTP_REFERER', '/'))


@require_http_methods(["POST"])
def add_done_set(request, id):
    user = request.user

    if not user.is_authenticated:
        return redirect('login')

    set_pair = get_object_or_404(SetPair, pk=id)
    form = CreateSet(request.POST)
    
    if form.is_valid():
        set = Set(weight=form.cleaned_data['weight'], repetitions=form.cleaned_data['repetitions'])
        set.save()

        set_pair.done_set = set
        set_pair.save()
    
    return redirect(request.META.get('HTTP_REFERER', '/'))




@require_http_methods(["POST"])
def add_performance(request, id):
    user = request.user

    if not user.is_authenticated:
        return redirect('login')

    exercise = get_object_or_404(ExerciseInstance, pk=id)
    form = AddPerformance(request.POST,request.FILES)
    
    if form.is_valid():
        print('valid')
        exercise.performance = form.cleaned_data['performance']
        exercise.save()
        
    return redirect(request.META.get('HTTP_REFERER', '/'))


def day_list(request):
    user = request.user

    if not user.is_authenticated:
        return redirect('login')


    month = request.GET.get('month')
    year = request.GET.get('year')
    if year == '':
        year = now().year

    if not month:
        year = now().year
        month = now().month

    #days = get_list_or_404(Day,user=user,date__year=year, date__month=month)

    days = Day.objects.filter(user=user,date__year=year, date__month=month)
    form = SelectDate()

    return render(request, 'fitness/day_list.html', {'days':paginate(request=request,list_object=days,number=10), 'form':form,'year':year, 'month':month})



def day_list_trainer(request, id):
    user = request.user

    if not user.is_authenticated:
        return redirect('login')

    client = get_object_or_404(user.account_set, pk=id)
    

    month = request.GET.get('month')
    year = request.GET.get('year')
    if year == '':
        year = now().year

    if not month:
        year = now().year
        month = now().month

    days = Day.objects.filter(user=client,date__year=year, date__month=month)
    form = SelectDate()
    print(year, month)

    return render(request, 'fitness/day_list.html', {'days':paginate(request=request,list_object=days,number=10), 'form':form,'year':year, 'month':month,'client':client})

#END NEW




def weight_progression(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')



    if request.method == "POST":
        form = AddWeight(request.POST)

        
        if form.is_valid():
            form_dict = form.cleaned_data
            
            weight = form_dict['weight']
            date = now()
            user.weight = weight
            user.save()
            
            existing_weight = WeightAtDate.objects.filter(user=user).filter(date=date)
            if existing_weight:
                existing_weight = existing_weight[0]
                existing_weight.weight = weight
                existing_weight.save()
            else:
                weight_at_date = WeightAtDate(weight=weight, date=date, user=user)
                weight_at_date.save()
            
        

    weights = user.weightatdate_set.all()

    form = AddWeight()
    
    return render(request, 'fitness/weight_progression.html', {'weights':paginate(request,weights,4), 'form':form})


def delete_weight_date(request,id):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')
    
    weight = WeightAtDate.objects.get(pk=id)
    
    if not user == weight.user:
        return redirect('index') 
    
    weight.delete()
    
    return redirect('weight-progression')


def trainers_list(request):
    trainers = Account.objects.filter(is_trainer=True)

    name = request.GET.get('name')

    if name:
        for aux in name.split():
            trainers = trainers.filter( Q(first_name__contains=aux) | Q(last_name__contains=aux))



    return render(request, 'fitness/accounts_list.html', {'users':paginate(request,trainers,4)})



def my_clients(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')

    if not user.is_trainer:
        return redirect('index')

    clients = user.account_set.all()


    name = request.GET.get('name')

    if name:
        for aux in name.split():
            clients = clients.filter( Q(first_name__contains=aux) | Q(last_name__contains=aux))

    paginator = Paginator(clients, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'fitness/accounts_list.html', {'users':page_obj})


@require_http_methods(["POST"])
def trainer_request(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')


    id = request.POST.get('id')
    trainer = Account.objects.filter(pk=id)

    if not trainer:
        return redirect(request.META.get('HTTP_REFERER', '/'))

    trainer = trainer[0]

    already_asked = TrainerRequest.objects.filter(client=user)
    if already_asked or user == trainer:
        return redirect(request.META.get('HTTP_REFERER', '/'))


    req = TrainerRequest(client=user, trainer=trainer)
    req.save()

    return redirect(request.META.get('HTTP_REFERER', '/'))



def trainer_response(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')

    if not user.is_trainer:
        return redirect('index')

    requests_list = TrainerRequest.objects.filter(trainer=user)
    clients = [ tr.client for tr in requests_list]


    return render(request, 'fitness/accounts_list.html', {'users':paginate(request=request,list_object=clients,number=4)})


@require_http_methods(["POST"])
def cancel_request(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')

    id = request.POST.get('id')
    trainer = Account.objects.filter(pk=id)
    
    if not trainer:
        return redirect(request.META.get('HTTP_REFERER', '/'))
    

    trainer = trainer[0]
    req = TrainerRequest.objects.filter(client=user, trainer=trainer)
    req[0].delete()

    return redirect(request.META.get('HTTP_REFERER', '/'))



@require_http_methods(["POST"])
def trainer_response_yes(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')

    id = request.POST.get('id')

    client = Account.objects.filter(pk=id)

    if not client:
        return redirect(request.META.get('HTTP_REFERER', '/'))

    client = client[0]

    client.trainer = user
    client.save()

    req = TrainerRequest.objects.filter(client=client, trainer=user)
    req[0].delete()


    return redirect(request.META.get('HTTP_REFERER', '/'))



@require_http_methods(["POST"])
def trainer_response_no(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')

    id = request.POST.get('id')

    client = Account.objects.filter(pk=id)

    if not client:
        return redirect(request.META.get('HTTP_REFERER', '/'))

    client = client[0]


    req = TrainerRequest.objects.filter(client=client, trainer=user)
    req[0].delete()


    return redirect(request.META.get('HTTP_REFERER', '/'))


def my_account(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')

    return render(request, 'fitness/account_detail.html', {'profile':user})



def profile(request, id):
    profile = get_object_or_404(Account, pk=id)

    return render(request, 'fitness/account_detail.html', {'profile':profile})