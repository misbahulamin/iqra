from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from usermanagement.models import User, StudentProfile, TeacherProfile
import requests
from django.conf import settings


class GoogleAuthSerializer(serializers.Serializer):
    """
    Serializer for Google OAuth authentication
    """
    access_token = serializers.CharField()
    
    def validate_access_token(self, access_token):
        """
        Validate Google access token and get user info
        """
        google_userinfo_url = 'https://www.googleapis.com/oauth2/v2/userinfo'
        
        try:
            response = requests.get(
                google_userinfo_url,
                params={'access_token': access_token}
            )
            
            if response.status_code != 200:
                raise serializers.ValidationError('Invalid access token')
            
            user_data = response.json()
            
            if 'error' in user_data:
                raise serializers.ValidationError('Invalid access token')
            
            return user_data
            
        except requests.RequestException:
            raise serializers.ValidationError('Unable to validate token with Google')


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration
    """
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True)
    user_type = serializers.ChoiceField(choices=User.USER_TYPE_CHOICES, default='student')
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'confirm_password', 'user_type', 'phone']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Password and confirm password don't match")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login
    """
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled')
            attrs['user'] = user
        else:
            raise serializers.ValidationError('Must include username and password')
        
        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile information
    """
    student_profile = serializers.SerializerMethodField()
    teacher_profile = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'user_type', 
                 'phone', 'avatar', 'is_verified', 'student_profile', 'teacher_profile',
                 'date_joined', 'last_login']
        read_only_fields = ['id', 'date_joined', 'last_login']
    
    def get_student_profile(self, obj):
        if hasattr(obj, 'student_profile'):
            return {
                'student_id': obj.student_profile.student_id,
                'grade': obj.student_profile.grade,
                'major': obj.student_profile.major,
                'enrollment_date': obj.student_profile.enrollment_date
            }
        return None
    
    def get_teacher_profile(self, obj):
        if hasattr(obj, 'teacher_profile'):
            return {
                'employee_id': obj.teacher_profile.employee_id,
                'department': obj.teacher_profile.department,
                'specialization': obj.teacher_profile.specialization,
                'hire_date': obj.teacher_profile.hire_date
            }
        return None


class StudentProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for student profile
    """
    class Meta:
        model = StudentProfile
        fields = ['student_id', 'grade', 'major', 'enrollment_date']


class TeacherProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for teacher profile
    """
    class Meta:
        model = TeacherProfile
        fields = ['employee_id', 'department', 'specialization', 'hire_date']
