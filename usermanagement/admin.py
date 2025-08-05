from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, StudentProfile, TeacherProfile


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    自定义用户管理界面
    """
    list_display = ['username', 'email', 'user_type', 'is_verified', 'is_active', 'date_joined']
    list_filter = ['user_type', 'is_verified', 'is_active', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    
    fieldsets = UserAdmin.fieldsets + (
        ('额外信息', {
            'fields': ('user_type', 'phone', 'avatar', 'is_verified')
        }),
    )


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    """
    学生档案管理界面
    """
    list_display = ['user', 'student_id', 'grade', 'major', 'enrollment_date']
    list_filter = ['grade', 'major', 'enrollment_date']
    search_fields = ['user__username', 'student_id', 'grade', 'major']


@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    """
    教师档案管理界面
    """
    list_display = ['user', 'employee_id', 'department', 'specialization', 'hire_date']
    list_filter = ['department', 'hire_date']
    search_fields = ['user__username', 'employee_id', 'department', 'specialization']