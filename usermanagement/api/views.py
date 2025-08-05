from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from usermanagement.models import User, StudentProfile, TeacherProfile
from .serializers import (
    GoogleAuthSerializer, 
    UserRegistrationSerializer, 
    UserLoginSerializer, 
    UserProfileSerializer,
    StudentProfileSerializer,
    TeacherProfileSerializer
)
import datetime
import uuid


@api_view(['GET'])
def health_check(request):
    """
    Simple health check endpoint - Test if project is running properly
    """
    return Response({
        'status': 'success',
        'message': '🎓 Student E-Learning Platform Backend System is running normally!',
        'timestamp': datetime.datetime.now().isoformat(),
        'version': '1.0.0',
        'app': 'usermanagement'
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
def project_info(request):
    """
    Project information endpoint
    """
    return Response({
        'project_name': 'IQRA Backend - Student E-Learning Platform',
        'description': 'Backend API system providing online learning services for students',
        'features': [
            'User Management',
            'Course Management',
            'Learning Progress Tracking',
            'Online Examinations',
            'Grade Management',
            'Google OAuth Authentication'
        ],
        'status': 'In Development',
        'api_version': 'v1',
        'framework': 'Django REST Framework'
    }, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def test_endpoint(request):
    """
    Test endpoint - Supports GET and POST requests
    """
    if request.method == 'GET':
        return Response({
            'method': 'GET',
            'message': 'GET request test successful!',
            'data': 'This is a test endpoint proving the API is working'
        })
    
    elif request.method == 'POST':
        return Response({
            'method': 'POST',
            'message': 'POST request test successful!',
            'received_data': request.data,
            'timestamp': datetime.datetime.now().isoformat()
        }, status=status.HTTP_201_CREATED)


# ==============================================================================
# AUTHENTICATION VIEWS
# ==============================================================================

@api_view(['POST'])
@permission_classes([AllowAny])
def google_auth(request):
    """
    Google OAuth authentication endpoint
    Expects: {"access_token": "google_access_token"}
    Returns: User data and authentication token
    """
    serializer = GoogleAuthSerializer(data=request.data)
    
    if serializer.is_valid():
        google_user_data = serializer.validated_data['access_token']
        
        try:
            # Check if user already exists
            user, created = User.objects.get_or_create(
                email=google_user_data['email'],
                defaults={
                    'username': google_user_data['email'],
                    'first_name': google_user_data.get('given_name', ''),
                    'last_name': google_user_data.get('family_name', ''),
                    'is_verified': google_user_data.get('verified_email', False),
                    'avatar': google_user_data.get('picture', ''),
                }
            )
            
            # Create or get authentication token
            token, created = Token.objects.get_or_create(user=user)
            
            # Serialize user data
            user_serializer = UserProfileSerializer(user)
            
            return Response({
                'success': True,
                'message': 'Google authentication successful' if not created else 'User registered successfully via Google',
                'user': user_serializer.data,
                'token': token.key,
                'is_new_user': created
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'success': False,
                'message': 'Authentication failed',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({
        'success': False,
        'message': 'Invalid data provided',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """
    User registration endpoint
    """
    serializer = UserRegistrationSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'success': True,
            'message': 'User registered successfully',
            'user': UserProfileSerializer(user).data,
            'token': token.key
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        'success': False,
        'message': 'Registration failed',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    """
    User login endpoint
    """
    serializer = UserLoginSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'success': True,
            'message': 'Login successful',
            'user': UserProfileSerializer(user).data,
            'token': token.key
        }, status=status.HTTP_200_OK)
    
    return Response({
        'success': False,
        'message': 'Login failed',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    """
    User logout endpoint
    """
    try:
        request.user.auth_token.delete()
        return Response({
            'success': True,
            'message': 'Logout successful'
        }, status=status.HTTP_200_OK)
    except:
        return Response({
            'success': False,
            'message': 'Logout failed'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    """
    Get or update user profile
    """
    if request.method == 'GET':
        serializer = UserProfileSerializer(request.user)
        return Response({
            'success': True,
            'user': serializer.data
        }, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'message': 'Profile updated successfully',
                'user': serializer.data
            }, status=status.HTTP_200_OK)
        
        return Response({
            'success': False,
            'message': 'Profile update failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_student_profile(request):
    """
    Create student profile for authenticated user
    """
    if request.user.user_type != 'student':
        return Response({
            'success': False,
            'message': 'Only students can create student profiles'
        }, status=status.HTTP_403_FORBIDDEN)
    
    if hasattr(request.user, 'student_profile'):
        return Response({
            'success': False,
            'message': 'Student profile already exists'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = StudentProfileSerializer(data=request.data)
    if serializer.is_valid():
        student_profile = serializer.save(user=request.user)
        return Response({
            'success': True,
            'message': 'Student profile created successfully',
            'profile': StudentProfileSerializer(student_profile).data
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        'success': False,
        'message': 'Profile creation failed',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_teacher_profile(request):
    """
    Create teacher profile for authenticated user
    """
    if request.user.user_type != 'teacher':
        return Response({
            'success': False,
            'message': 'Only teachers can create teacher profiles'
        }, status=status.HTTP_403_FORBIDDEN)
    
    if hasattr(request.user, 'teacher_profile'):
        return Response({
            'success': False,
            'message': 'Teacher profile already exists'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = TeacherProfileSerializer(data=request.data)
    if serializer.is_valid():
        teacher_profile = serializer.save(user=request.user)
        return Response({
            'success': True,
            'message': 'Teacher profile created successfully',
            'profile': TeacherProfileSerializer(teacher_profile).data
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        'success': False,
        'message': 'Profile creation failed',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)
