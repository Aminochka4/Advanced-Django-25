from django.shortcuts import render, redirect
from .models import Food, Consume, HealthGoal, Food
from django.contrib.auth.decorators import login_required
from .forms import HealthGoalForm, FoodForm
from django.http import JsonResponse 
from django.contrib.auth.forms import UserCreationForm 

def index(request): 
    if request.method == "POST":
        food_consumed = request.POST['food_consumed']
        c = Food.objects.get(name=food_consumed)
        user = request.user
        consume = Consume(user=user, food_consumed=c)
        consume.save()

    foods = Food.objects.all()
    consumed_food = Consume.objects.filter(user=request.user)
    health_goal, created = HealthGoal.objects.get_or_create(user=request.user)

    return render(request, 'app/index.html', {
        'foods': foods,
        'consumed_food': consumed_food,
        'health_goal': health_goal
    })

def delete_consume(request, id):
    consumed_food = Consume.objects.get(id=id)
    if request.method=="POST":
        consumed_food.delete()
        return redirect('/')
    return render(request, 'app/delete.html')

@login_required
def update_goal(request):
    goal, created = HealthGoal.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = HealthGoalForm(request.POST, instance=goal)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = HealthGoalForm(instance=goal)

    return render(request, 'app/update_goal.html', {'form': form})

def chart_data(request): 
    consumed = Consume.objects.filter(user=request.user) 
    data = { 
        "labels": [c.food_consumed.name for c in consumed], 
        "carbs": [c.food_consumed.carbs for c in consumed], 
        "proteins": [c.food_consumed.proteins for c in consumed], 
        "fats": [c.food_consumed.fats for c in consumed], 
        "calorie": [c.food_consumed.calorie for c in consumed], 
    } 
    return JsonResponse(data) 

def register(request): 
    if request.method == "POST": 
        form = UserCreationForm(request.POST) 
        if form.is_valid(): 
            form.save() 
            return redirect("login") 
    else: 
        form = UserCreationForm() 
    return render(request, "app/register.html", {"form": form}) 

def add_food(request): 
    if request.method == "POST": 
        form = FoodForm(request.POST) 
        if form.is_valid(): 
            form.save()  # Saves the food to the global registry 
            return redirect("index")  # Redirects back to the homepage 
    else: 
        form = FoodForm() 
    return render(request, "app/add_food.html", {"form": form}) 
