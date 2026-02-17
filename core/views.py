from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Exercise, PersonalWorkout, NutritionPlan, ProgressUpdate, CoachQnA
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# ==========================================
# 1. DASHBOARD VIEW
# Displays personalized workouts for the logged-in user
# ==========================================
@login_required(login_url='/accounts/login/')
def dashboard(request):
    workouts = PersonalWorkout.objects.filter(user=request.user).order_by('id')
    context = {
        'workouts': workouts,
        'page': 'dashboard'
    }
    return render(request, 'dashboard.html', context)

# ==========================================
# 2. NUTRITION VIEW
# Displays the latest nutrition plan assigned to the user
# ==========================================
@login_required(login_url='/accounts/login/')
def nutrition(request):
    plan = NutritionPlan.objects.filter(user=request.user).last()
    context = {
        'plan': plan,
        'page': 'nutrition'
    }
    return render(request, 'nutrition.html', context)

# ==========================================
# 3. PROGRESS VIEW
# Handles progress photo uploads and displays history
# ==========================================
@login_required(login_url='/accounts/login/')
def progress(request):
    if request.method == 'POST':
        weight = request.POST.get('weight')
        notes = request.POST.get('notes')
        photo_front = request.FILES.get('photo_front')
        photo_side = request.FILES.get('photo_side')
        photo_back = request.FILES.get('photo_back')
        
        ProgressUpdate.objects.create(
            user=request.user,
            weight=weight,
            notes=notes,
            photo_front=photo_front,
            photo_side=photo_side,
            photo_back=photo_back
        )
        return redirect('progress')

    updates = ProgressUpdate.objects.filter(user=request.user).order_by('-date')
    context = {
        'updates': updates,
        'page': 'progress'
    }
    return render(request, 'progress.html', context)

# ==========================================
# 4. COACH Q&A VIEW
# Handles question submission and displays chat history
# ==========================================
@login_required(login_url='/accounts/login/')
def contact_coach(request):
    if request.method == 'POST':
        question = request.POST.get('question')
        if question:
            CoachQnA.objects.create(user=request.user, question=question)
            return redirect('contact_coach')
            
    messages = CoachQnA.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'messages': messages,
        'page': 'contact'
    }
    return render(request, 'contact.html', context)

# ==========================================
# 5. USER REGISTRATION
# Handles new user account creation
# ==========================================
def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})