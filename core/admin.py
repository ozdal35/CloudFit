from django.contrib import admin
from .models import Exercise, PersonalWorkout, NutritionPlan, ProgressUpdate, CoachQnA

# Configure Exercise Admin
@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title',)

# Configure Personal Workout Admin
@admin.register(PersonalWorkout)
class PersonalWorkoutAdmin(admin.ModelAdmin):
    list_display = ('user', 'exercise', 'sets', 'reps', 'weight')
    list_filter = ('user',) # Filter workouts by user
    search_fields = ('user__username', 'exercise__title')
    autocomplete_fields = ['exercise'] # Search box for exercises

# Configure Nutrition Plan Admin
@admin.register(NutritionPlan)
class NutritionPlanAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'created_at')
    list_filter = ('user',)

# Configure Progress Update Admin
@admin.register(ProgressUpdate)
class ProgressUpdateAdmin(admin.ModelAdmin):
    list_display = ('user', 'weight', 'date')
    list_filter = ('user', 'date')

# Configure Q&A Admin
@admin.register(CoachQnA)
class CoachQnAAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'is_answered', 'created_at')
    list_filter = ('is_answered', 'user')
    list_editable = ('is_answered',) # Quickly mark as answered