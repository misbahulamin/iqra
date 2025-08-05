from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Extended user model for student e-learning platform
    """
    USER_TYPE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Administrator'),
    ]
    
    user_type = models.CharField(
        max_length=10, 
        choices=USER_TYPE_CHOICES, 
        default='student',
        verbose_name='User Type'
    )
    phone = models.CharField(
        max_length=15, 
        blank=True, 
        null=True,
        verbose_name='Phone Number'
    )
    avatar = models.URLField(
        blank=True, 
        null=True,
        verbose_name='Avatar URL'
    )
    is_verified = models.BooleanField(
        default=False,
        verbose_name='Is Verified'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created At'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Updated At'
    )
    
    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class StudentProfile(models.Model):
    """
    Student profile information
    """
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        related_name='student_profile'
    )
    student_id = models.CharField(
        max_length=20, 
        unique=True,
        verbose_name='Student ID'
    )
    grade = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Grade'
    )
    major = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Major'
    )
    enrollment_date = models.DateField(
        null=True, 
        blank=True,
        verbose_name='Enrollment Date'
    )
    
    def __str__(self):
        return f"{self.user.username} - {self.student_id}"
    
    class Meta:
        verbose_name = 'Student Profile'
        verbose_name_plural = 'Student Profiles'


class TeacherProfile(models.Model):
    """
    Teacher profile information
    """
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        related_name='teacher_profile'
    )
    employee_id = models.CharField(
        max_length=20, 
        unique=True,
        verbose_name='Employee ID'
    )
    department = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Department'
    )
    specialization = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Specialization'
    )
    hire_date = models.DateField(
        null=True, 
        blank=True,
        verbose_name='Hire Date'
    )
    
    def __str__(self):
        return f"{self.user.username} - {self.employee_id}"
    
    class Meta:
        verbose_name = 'Teacher Profile'
        verbose_name_plural = 'Teacher Profiles'