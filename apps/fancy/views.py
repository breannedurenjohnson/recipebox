from django.shortcuts import render, redirect
from .models import User, Recipe
import bcrypt
from django.contrib import messages

def index(request):
    return render(request, 'fancy/index.html')


def register(request):
    return render(request, 'fancy/register.html')

def submit_registration(request):
    errors = User.objects.reg_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/register')
    else:
        password = request.POST['password']
        hash1 = bcrypt.hashpw(password.encode(), bcrypt.gensalt()) 
        User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=hash1)
        last_user = User.objects.last()
        request.session['user_name'] = last_user.first_name
        request.session['user_id'] = last_user.id
    return redirect('/dashboard')

def login(request):
    errors = {}
    user = User.objects.filter(email=request.POST['email'])
    if user:
        logged_user = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['user_id'] = logged_user.id
            request.session['user_name'] = logged_user.first_name
            return redirect('/dashboard')
        else: 
            errors['login_match'] = "Email and password do not match."
    else:
        errors['email_nonexist'] = "Email does not exist."
    for key, value in errors.items():
        messages.error(request, value)
        print(messages)
    return redirect('/')

def dashboard(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user_first_name =request.session['user_name']
    user_id = request.session['user_id']
    context = {
        "user_name": user_first_name,
        "user_id": user_id,
        "all_recipes": Recipe.objects.all().order_by("created_at"),
        "liked_recipes": Recipe.objects.filter(users_who_like = User.objects.get(id=request.session['user_id'])).order_by("-created_at"),
        "unliked_recipes": Recipe.objects.exclude(users_who_like = User.objects.get(id=request.session['user_id'])).order_by("-created_at"),
    }
    return render(request, 'fancy/dashboard.html', context)

def recipe(request, id):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        "user_id": request.session['user_id'],
        "recipe": Recipe.objects.get(id=id),
    }
    return render(request, 'fancy/recipe.html', context)

def meal(request, meal):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        "user_id": request.session['user_id'],
        "meal": meal,
        "recipes_by_meal": Recipe.objects.filter(meal = meal)
    }
    return render(request, 'fancy/meal.html', context)

def like_recipe(request, id):
    if 'user_id' not in request.session:
        return redirect('/')
    if request.method == "POST":
        this_recipe = Recipe.objects.get(id=id)
        this_user = User.objects.get(id=request.session['user_id'])
        this_recipe.users_who_like.add(this_user)
        return redirect('/dashboard')

def unlike_recipe(request, id):
    if 'user_id' not in request.session:
        return redirect('/')
    if request.method == "POST":
        this_recipe = Recipe.objects.get(id=id)
        this_user = User.objects.get(id=request.session['user_id'])
        this_recipe.users_who_like.remove(this_user)
        return redirect('/dashboard')

def profile(request, user_id):
    if 'user_id' not in request.session:
        return redirect('/')
    user_id = request.session['user_id']
    context = {
        "user": User.objects.get(id=user_id),
        "liked_recipes": Recipe.objects.filter(users_who_like = User.objects.get(id=request.session['user_id'])).order_by("-created_at"),    }
    return render(request, 'fancy/profile.html', context)

def logout(request):
    request.session.clear()
    return redirect('/')