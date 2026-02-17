from django.contrib import admin
from .models import Exercise, PersonalWorkout, NutritionPlan, ProgressUpdate, CoachQnA, WorkoutLog

# ==========================================
# 1. EXERCISE LIBRARY MANAGEMENT
# (Global library of exercises, not specific to any user)
# ==========================================
@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('title', 'video_url', 'created_at')
    search_fields = ('title',) # Enables search box for exercises
    list_per_page = 20

# ==========================================
# 2. PERSONALIZED WORKOUT ASSIGNMENT
# (This is where the Coach assigns specific exercises to specific Athletes)
# ==========================================
@admin.register(PersonalWorkout)
class PersonalWorkoutAdmin(admin.ModelAdmin):
    # Columns shown in the list view for quick overview
    list_display = ('user', 'exercise', 'sets', 'reps', 'weight', 'created_at')
    
    # Sidebar filters (Crucial for filtering workouts by a specific Athlete)
    list_filter = ('user', 'exercise')
    
    # Search bar (Search by username or exercise title)
    search_fields = ('user__username', 'exercise__title')
    
    # Allows editing sets/reps/weight directly from the list view (Increases efficiency)
    list_editable = ('sets', 'reps', 'weight')
    
    # Uses a search input for selecting exercises instead of a long dropdown list
    autocomplete_fields = ['exercise']

# ==========================================
# 3. NUTRITION PLAN MANAGEMENT
# ==========================================
@admin.register(NutritionPlan)
class NutritionPlanAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'created_at')
    list_filter = ('user',) # Filter plans by user

# ==========================================
# 4. PROGRESS TRACKING MANAGEMENT
# ==========================================
@admin.register(ProgressUpdate)
class ProgressUpdateAdmin(admin.ModelAdmin):
    list_display = ('user', 'weight', 'date')
    list_filter = ('user', 'date')

# ==========================================
# 5. COACH Q&A MANAGEMENT
# ==========================================
@admin.register(CoachQnA)
class CoachQnAAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'is_answered', 'created_at')
    list_filter = ('is_answered', 'user')
    list_editable = ('is_answered',) # Quickly mark as answered/unanswered

# ==========================================
# 6. WORKOUT LOGS (HISTORY)
# (View-only for the coach to see completed sets by athletes)
# ==========================================
@admin.register(WorkoutLog)
class WorkoutLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'exercise', 'weight_done', 'date')
    list_filter = ('user', 'date', 'exercise')
    # These fields should be read-only as they are historical data
    readonly_fields = ('user', 'exercise', 'sets_done', 'reps_done', 'weight_done', 'date')