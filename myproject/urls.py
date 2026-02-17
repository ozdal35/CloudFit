from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core import views

urlpatterns = [
    # Admin Panel
    path('admin/', admin.site.urls),
    
    # Core Application URLs
    path('', views.dashboard, name='dashboard'),           # Main Dashboard
    path('nutrition/', views.nutrition, name='nutrition'), # Nutrition Plan Page
    path('progress/', views.progress, name='progress'),    # Progress Tracking Page
    path('contact/', views.contact_coach, name='contact_coach'), # Coach Communication Page
    
    # Authentication URLs (Login/Register/Logout)
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
]

# Media Files Configuration (For displaying images in Debug mode)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)