from django.shortcuts import render, redirect
from .models import Food, Consume


def index(request): 
    if request.method =="POST":
        food_consumed = request.POST['food_consumed']
        c = Food.objects.get(name=food_consumed)
        user = request.user
        consume = Consume(user=user, food_consumed=c)
        consume.save()
        foods = Food.objects.all()
    else:
        foods = Food.objects.all()
    consumed_food = Consume.objects.filter(user=request.user)
    return render(request, 'app/index.html', {'foods': foods, 'consumed_food':consumed_food}) 

def delete_consume(request, id):
    consumed_food = Consume.objects.get(id=id)
    if request.method=="POST":
        consumed_food.delete()
        return redirect('/')
    return render(request, 'app/delete.html')

