from django.urls import path
from . import views

urlpatterns = [
    # Health check and info endpoints
    path('health/', views.health_check, name='health_check'),
    path('info/', views.project_info, name='project_info'),
    path('test/', views.test_endpoint, name='test_endpoint'),
    
    # Authentication endpoints
    path('auth/google/', views.google_auth, name='google_auth'),
    path('auth/register/', views.register, name='register'),
    path('auth/login/', views.login_user, name='login'),
    path('auth/logout/', views.logout_user, name='logout'),
    
    # User profile endpoints
    path('profile/', views.user_profile, name='user_profile'),
    path('profile/student/', views.create_student_profile, name='create_student_profile'),
    path('profile/teacher/', views.create_teacher_profile, name='create_teacher_profile'),
]
