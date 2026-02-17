from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.utils import timezone  # Used to get today's date

# Importing models
from .models import Exercise, PersonalWorkout, NutritionPlan, ProgressUpdate, CoachQnA, WorkoutLog

# ==========================================
# 1. DASHBOARD VIEW
# Displays workouts and handles "Log Set" actions with duplicate prevention
# ==========================================
@login_required(login_url='/accounts/login/')
def dashboard(request):
    today = timezone.now().date()

    # Handle the "Log Set" button click (POST request)
    if request.method == 'POST':
        workout_id = request.POST.get('workout_id')
        workout = get_object_or_404(PersonalWorkout, id=workout_id, user=request.user)
        
        # CHECK: Has this exercise already been logged today?
        already_logged = WorkoutLog.objects.filter(
            user=request.user, 
            exercise=workout.exercise, 
            date=today
        ).exists()

        # Only create a log if it doesn't exist yet
        if not already_logged:
            WorkoutLog.objects.create(
                user=request.user,
                exercise=workout.exercise,
                sets_done=workout.sets,
                reps_done=workout.reps,
                weight_done=workout.weight
            )
        
        return redirect('dashboard')

    # Fetch workouts assigned to the user
    workouts = PersonalWorkout.objects.filter(user=request.user).order_by('id')

    # Get a list of IDs of exercises completed TODAY
    # This helps us disable the button in the HTML template
    completed_exercise_ids = WorkoutLog.objects.filter(
        user=request.user, 
        date=today
    ).values_list('exercise_id', flat=True)

    context = {
        'workouts': workouts,
        'completed_ids': completed_exercise_ids, # Passing the list to the template
        'page': 'dashboard'
    }
    return render(request, 'dashboard.html', context)

# ==========================================
# 2. NUTRITION VIEW
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
# 5. REGISTRATION
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