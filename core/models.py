from django.db import models
from django.contrib.auth.models import User

# ==========================================
# 1. EXERCISE LIBRARY (Managed by Coach/Admin)
# ==========================================
class Exercise(models.Model):
    title = models.CharField(max_length=100, verbose_name="Exercise Name")
    description = models.TextField(verbose_name="Description")
    image = models.ImageField(upload_to='exercises/', verbose_name="Image", blank=True, null=True)
    video_url = models.URLField(verbose_name="YouTube Video URL", blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    # Helper method to extract video ID from YouTube URL for embedding
    def get_video_id(self):
        if not self.video_url:
            return None
        if "v=" in self.video_url:
            return self.video_url.split("v=")[1].split("&")[0]
        elif "youtu.be" in self.video_url:
            return self.video_url.split("/")[-1]
        return None

# ==========================================
# 2. PERSONALIZED WORKOUT (Assigned by Coach -> Read by User)
# ==========================================
class PersonalWorkout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="workouts")
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    
    # Workout Details
    sets = models.PositiveIntegerField(default=3, verbose_name="Sets")
    reps = models.PositiveIntegerField(default=12, verbose_name="Reps")
    weight = models.FloatField(default=0, verbose_name="Target Weight (kg)")
    
    notes = models.CharField(max_length=200, blank=True, verbose_name="Coach Notes")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.exercise.title}"

# ==========================================
# 3. NUTRITION PLAN (Assigned by Coach -> Read by User)
# ==========================================
class NutritionPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="nutrition_plans")
    title = models.CharField(max_length=100, verbose_name="Plan Title (e.g., Cutting Phase)")
    image = models.ImageField(upload_to='nutrition/', verbose_name="Diet Plan Image/PDF")
    description = models.TextField(verbose_name="Plan Details / Notes", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Nutrition Plan"

# ==========================================
# 4. PROGRESS TRACKING (Uploaded by User -> Reviewed by Coach)
# ==========================================
class ProgressUpdate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True, verbose_name="Date")
    weight = models.FloatField(verbose_name="Current Weight (kg)")
    
    # Progress Photos
    photo_front = models.ImageField(upload_to='progress/', verbose_name="Front Photo", blank=True, null=True)
    photo_side = models.ImageField(upload_to='progress/', verbose_name="Side Photo", blank=True, null=True)
    photo_back = models.ImageField(upload_to='progress/', verbose_name="Back Photo", blank=True, null=True)
    
    notes = models.TextField(blank=True, verbose_name="User Notes")

    def __str__(self):
        return f"{self.user.username} - {self.date}"

# ==========================================
# 5. COACH Q&A (Messaging System)
# ==========================================
class CoachQnA(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.TextField(verbose_name="Question")
    answer = models.TextField(verbose_name="Coach Answer", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_answered = models.BooleanField(default=False)

    def __str__(self):
        return f"Q: {self.user.username} - {self.created_at.strftime('%Y-%m-%d')}"