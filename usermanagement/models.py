from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    扩展的用户模型 - 适用于学生电子学习平台
    """
    USER_TYPE_CHOICES = [
        ('student', '学生'),
        ('teacher', '教师'),
        ('admin', '管理员'),
    ]
    
    user_type = models.CharField(
        max_length=10, 
        choices=USER_TYPE_CHOICES, 
        default='student',
        verbose_name='用户类型'
    )
    phone = models.CharField(
        max_length=15, 
        blank=True, 
        null=True,
        verbose_name='电话号码'
    )
    avatar = models.URLField(
        blank=True, 
        null=True,
        verbose_name='头像链接'
    )
    is_verified = models.BooleanField(
        default=False,
        verbose_name='是否已验证'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='更新时间'
    )
    
    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"
    
    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户管理'


class StudentProfile(models.Model):
    """
    学生档案信息
    """
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        related_name='student_profile'
    )
    student_id = models.CharField(
        max_length=20, 
        unique=True,
        verbose_name='学号'
    )
    grade = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='年级'
    )
    major = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='专业'
    )
    enrollment_date = models.DateField(
        null=True, 
        blank=True,
        verbose_name='入学日期'
    )
    
    def __str__(self):
        return f"{self.user.username} - {self.student_id}"
    
    class Meta:
        verbose_name = '学生档案'
        verbose_name_plural = '学生档案管理'


class TeacherProfile(models.Model):
    """
    教师档案信息
    """
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        related_name='teacher_profile'
    )
    employee_id = models.CharField(
        max_length=20, 
        unique=True,
        verbose_name='工号'
    )
    department = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='所属部门'
    )
    specialization = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='专业领域'
    )
    hire_date = models.DateField(
        null=True, 
        blank=True,
        verbose_name='入职日期'
    )
    
    def __str__(self):
        return f"{self.user.username} - {self.employee_id}"
    
    class Meta:
        verbose_name = '教师档案'
        verbose_name_plural = '教师档案管理'
