from account.models import Account
from django.shortcuts import render, redirect
from .forms import SignUpForm
from fitness.models import WeightAtDate

# Create your views here.

def signup(request):

    if request.method == "POST":
        f = SignUpForm(request.POST)

        if f.is_valid():
            user = f.save()

            weight = f.cleaned_data['weight']
            if weight:
                weight_at_date = WeightAtDate(weight=weight, user=user)
                weight_at_date.save()
                
        
            return redirect('/')
    
    
    form = SignUpForm()

    return render(request, 'register/signup.html', {'form':form})
