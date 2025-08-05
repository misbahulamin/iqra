# IQRA E-Learning Platform - Authentication API Documentation

## Table of Contents
1. [Overview](#overview)
2. [Authentication Flow](#authentication-flow)
3. [API Endpoints](#api-endpoints)
4. [Request/Response Examples](#requestresponse-examples)
5. [Google OAuth Integration](#google-oauth-integration)
6. [Token Management](#token-management)
7. [Frontend Integration Examples](#frontend-integration-examples)
8. [Error Handling](#error-handling)
9. [Security Best Practices](#security-best-practices)
10. [Testing Guide](#testing-guide)

---

## Overview

The IQRA E-Learning Platform provides a comprehensive authentication system supporting:
- **Google OAuth 2.0** authentication
- **Traditional email/password** registration and login
- **Token-based authentication** for API access
- **Role-based access** (Student, Teacher, Administrator)
- **User profile management**

### Base URL
```
Development: http://127.0.0.1:8000
Production: [Your production URL]
```

### Authentication Method
- **Token Authentication**: Include `Authorization: Token <your-token>` in headers for authenticated requests

---

## Authentication Flow

```mermaid
graph TD
    A[User Visits Login] --> B{Login Method}
    B -->|Google OAuth| C[Redirect to Google]
    B -->|Email/Password| D[Traditional Login]
    C --> E[Google Returns Access Token]
    E --> F[Send Token to Backend]
    F --> G[Backend Validates with Google]
    G --> H[Backend Returns User + Django Token]
    D --> I[Validate Credentials]
    I --> H
    H --> J[Store Token in Frontend]
    J --> K[Use Token for API Calls]
```

---

## API Endpoints

### Base Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/api/usermanagement/health/` | Health check | ❌ |
| `GET` | `/api/usermanagement/info/` | Project information | ❌ |
| `POST` | `/api/usermanagement/auth/google/` | Google OAuth login | ❌ |
| `POST` | `/api/usermanagement/auth/register/` | User registration | ❌ |
| `POST` | `/api/usermanagement/auth/login/` | Traditional login | ❌ |
| `POST` | `/api/usermanagement/auth/logout/` | Logout user | ✅ |
| `GET` | `/api/usermanagement/profile/` | Get user profile | ✅ |
| `PUT` | `/api/usermanagement/profile/` | Update user profile | ✅ |
| `POST` | `/api/usermanagement/profile/student/` | Create student profile | ✅ |
| `POST` | `/api/usermanagement/profile/teacher/` | Create teacher profile | ✅ |

---

## Request/Response Examples

### 1. Google OAuth Authentication

**Endpoint:** `POST /api/usermanagement/auth/google/`

**Request:**
```json
{
    "access_token": "ya29.a0AfH6SMB..."
}
```

**Success Response (200):**
```json
{
    "success": true,
    "message": "Google authentication successful",
    "user": {
        "id": 1,
        "username": "john.doe@example.com",
        "email": "john.doe@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "user_type": "student",
        "phone": null,
        "avatar": "https://lh3.googleusercontent.com/...",
        "is_verified": true,
        "student_profile": null,
        "teacher_profile": null,
        "date_joined": "2025-01-01T00:00:00Z",
        "last_login": "2025-01-01T12:00:00Z"
    },
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
    "is_new_user": false
}
```

### 2. Traditional Registration

**Endpoint:** `POST /api/usermanagement/auth/register/`

**Request:**
```json
{
    "username": "john_doe",
    "email": "john.doe@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "password": "SecurePassword123!",
    "confirm_password": "SecurePassword123!",
    "user_type": "student",
    "phone": "+1234567890"
}
```

**Success Response (201):**
```json
{
    "success": true,
    "message": "User registered successfully",
    "user": {
        "id": 2,
        "username": "john_doe",
        "email": "john.doe@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "user_type": "student",
        "phone": "+1234567890",
        "avatar": null,
        "is_verified": false,
        "student_profile": null,
        "teacher_profile": null,
        "date_joined": "2025-01-01T00:00:00Z",
        "last_login": null
    },
    "token": "8833a08088c51bcf8307ad745dd0e3aadfc5dd3a"
}
```

### 3. Traditional Login

**Endpoint:** `POST /api/usermanagement/auth/login/`

**Request:**
```json
{
    "username": "john_doe",
    "password": "SecurePassword123!"
}
```

**Success Response (200):**
```json
{
    "success": true,
    "message": "Login successful",
    "user": {
        "id": 2,
        "username": "john_doe",
        "email": "john.doe@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "user_type": "student",
        "phone": "+1234567890",
        "avatar": null,
        "is_verified": false,
        "student_profile": null,
        "teacher_profile": null,
        "date_joined": "2025-01-01T00:00:00Z",
        "last_login": "2025-01-01T12:00:00Z"
    },
    "token": "8833a08088c51bcf8307ad745dd0e3aadfc5dd3a"
}
```

### 4. Get User Profile

**Endpoint:** `GET /api/usermanagement/profile/`

**Headers:**
```
Authorization: Token 8833a08088c51bcf8307ad745dd0e3aadfc5dd3a
```

**Success Response (200):**
```json
{
    "success": true,
    "user": {
        "id": 2,
        "username": "john_doe",
        "email": "john.doe@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "user_type": "student",
        "phone": "+1234567890",
        "avatar": null,
        "is_verified": false,
        "student_profile": {
            "student_id": "STU001",
            "grade": "10th Grade",
            "major": "Computer Science",
            "enrollment_date": "2025-01-01"
        },
        "teacher_profile": null,
        "date_joined": "2025-01-01T00:00:00Z",
        "last_login": "2025-01-01T12:00:00Z"
    }
}
```

### 5. Create Student Profile

**Endpoint:** `POST /api/usermanagement/profile/student/`

**Headers:**
```
Authorization: Token 8833a08088c51bcf8307ad745dd0e3aadfc5dd3a
```

**Request:**
```json
{
    "student_id": "STU001",
    "grade": "10th Grade",
    "major": "Computer Science",
    "enrollment_date": "2025-01-01"
}
```

**Success Response (201):**
```json
{
    "success": true,
    "message": "Student profile created successfully",
    "profile": {
        "student_id": "STU001",
        "grade": "10th Grade",
        "major": "Computer Science",
        "enrollment_date": "2025-01-01"
    }
}
```

### 6. Logout

**Endpoint:** `POST /api/usermanagement/auth/logout/`

**Headers:**
```
Authorization: Token 8833a08088c51bcf8307ad745dd0e3aadfc5dd3a
```

**Success Response (200):**
```json
{
    "success": true,
    "message": "Logout successful"
}
```

---

## Google OAuth Integration

### Frontend Setup Steps

#### 1. Install Google OAuth Library

**For React:**
```bash
npm install @react-oauth/google
# or
yarn add @react-oauth/google
```

**For Vanilla JavaScript:**
```html
<script src="https://apis.google.com/js/platform.js" async defer></script>
```

#### 2. Get Google Client ID

1. Visit [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable Google+ API
4. Create OAuth 2.0 credentials
5. Add your domain to authorized origins

#### 3. React Implementation

```jsx
import { GoogleOAuthProvider, GoogleLogin } from '@react-oauth/google';

function App() {
    const GOOGLE_CLIENT_ID = 'your-google-client-id.googleusercontent.com';

    const handleGoogleSuccess = async (credentialResponse) => {
        try {
            const response = await fetch('/api/usermanagement/auth/google/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    access_token: credentialResponse.credential
                })
            });

            const data = await response.json();
            
            if (data.success) {
                // Store token
                localStorage.setItem('authToken', data.token);
                localStorage.setItem('user', JSON.stringify(data.user));
                
                // Redirect to dashboard
                window.location.href = '/dashboard';
            } else {
                console.error('Login failed:', data.message);
            }
        } catch (error) {
            console.error('Login error:', error);
        }
    };

    const handleGoogleError = () => {
        console.error('Google login failed');
    };

    return (
        <GoogleOAuthProvider clientId={GOOGLE_CLIENT_ID}>
            <div>
                <GoogleLogin
                    onSuccess={handleGoogleSuccess}
                    onError={handleGoogleError}
                    useOneTap
                />
            </div>
        </GoogleOAuthProvider>
    );
}
```

#### 4. Vanilla JavaScript Implementation

```html
<!DOCTYPE html>
<html>
<head>
    <meta name="google-signin-client_id" content="your-google-client-id.googleusercontent.com">
</head>
<body>
    <div class="g-signin2" data-onsuccess="onSignIn"></div>
    
    <script>
        function onSignIn(googleUser) {
            const accessToken = googleUser.getAuthResponse().access_token;
            
            fetch('/api/usermanagement/auth/google/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    access_token: accessToken
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    localStorage.setItem('authToken', data.token);
                    localStorage.setItem('user', JSON.stringify(data.user));
                    window.location.href = '/dashboard';
                }
            })
            .catch(error => console.error('Error:', error));
        }
    </script>
    <script src="https://apis.google.com/js/platform.js" async defer></script>
</body>
</html>
```

---

## Token Management

### Storing Tokens

**Recommended: localStorage**
```javascript
// Store token after login
localStorage.setItem('authToken', data.token);

// Retrieve token for API calls
const token = localStorage.getItem('authToken');
```

**Alternative: sessionStorage**
```javascript
// Store token (expires when browser closes)
sessionStorage.setItem('authToken', data.token);
```

### Using Tokens in API Calls

**Fetch API:**
```javascript
const makeAuthenticatedRequest = async (url, options = {}) => {
    const token = localStorage.getItem('authToken');
    
    const defaultHeaders = {
        'Content-Type': 'application/json',
        'Authorization': `Token ${token}`
    };

    const config = {
        ...options,
        headers: {
            ...defaultHeaders,
            ...options.headers
        }
    };

    try {
        const response = await fetch(url, config);
        
        if (response.status === 401) {
            // Token expired or invalid
            localStorage.removeItem('authToken');
            window.location.href = '/login';
            return;
        }
        
        return await response.json();
    } catch (error) {
        console.error('API request failed:', error);
        throw error;
    }
};

// Usage
const userProfile = await makeAuthenticatedRequest('/api/usermanagement/profile/');
```

**Axios Example:**
```javascript
import axios from 'axios';

// Create axios instance with interceptors
const apiClient = axios.create({
    baseURL: 'http://127.0.0.1:8000',
});

// Request interceptor to add token
apiClient.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('authToken');
        if (token) {
            config.headers.Authorization = `Token ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

// Response interceptor to handle auth errors
apiClient.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            localStorage.removeItem('authToken');
            window.location.href = '/login';
        }
        return Promise.reject(error);
    }
);

// Usage
const getUserProfile = async () => {
    try {
        const response = await apiClient.get('/api/usermanagement/profile/');
        return response.data;
    } catch (error) {
        console.error('Failed to get profile:', error);
    }
};
```

---

## Frontend Integration Examples

### Complete Authentication Service (JavaScript)

```javascript
class AuthService {
    constructor() {
        this.baseURL = 'http://127.0.0.1:8000/api/usermanagement';
        this.token = localStorage.getItem('authToken');
    }

    // Google OAuth Login
    async googleLogin(accessToken) {
        try {
            const response = await fetch(`${this.baseURL}/auth/google/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ access_token: accessToken })
            });

            const data = await response.json();
            
            if (data.success) {
                this.setAuthData(data.token, data.user);
                return { success: true, user: data.user };
            } else {
                return { success: false, error: data.message };
            }
        } catch (error) {
            return { success: false, error: 'Network error' };
        }
    }

    // Traditional Login
    async login(username, password) {
        try {
            const response = await fetch(`${this.baseURL}/auth/login/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password })
            });

            const data = await response.json();
            
            if (data.success) {
                this.setAuthData(data.token, data.user);
                return { success: true, user: data.user };
            } else {
                return { success: false, error: data.message };
            }
        } catch (error) {
            return { success: false, error: 'Network error' };
        }
    }

    // Registration
    async register(userData) {
        try {
            const response = await fetch(`${this.baseURL}/auth/register/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(userData)
            });

            const data = await response.json();
            
            if (data.success) {
                this.setAuthData(data.token, data.user);
                return { success: true, user: data.user };
            } else {
                return { success: false, errors: data.errors };
            }
        } catch (error) {
            return { success: false, error: 'Network error' };
        }
    }

    // Logout
    async logout() {
        try {
            await fetch(`${this.baseURL}/auth/logout/`, {
                method: 'POST',
                headers: {
                    'Authorization': `Token ${this.token}`,
                },
            });
        } catch (error) {
            console.error('Logout error:', error);
        } finally {
            this.clearAuthData();
        }
    }

    // Get User Profile
    async getProfile() {
        try {
            const response = await fetch(`${this.baseURL}/profile/`, {
                headers: {
                    'Authorization': `Token ${this.token}`,
                },
            });

            const data = await response.json();
            return data.success ? data.user : null;
        } catch (error) {
            console.error('Profile fetch error:', error);
            return null;
        }
    }

    // Update Profile
    async updateProfile(profileData) {
        try {
            const response = await fetch(`${this.baseURL}/profile/`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Token ${this.token}`,
                },
                body: JSON.stringify(profileData)
            });

            const data = await response.json();
            return data;
        } catch (error) {
            return { success: false, error: 'Network error' };
        }
    }

    // Helper methods
    setAuthData(token, user) {
        this.token = token;
        localStorage.setItem('authToken', token);
        localStorage.setItem('user', JSON.stringify(user));
    }

    clearAuthData() {
        this.token = null;
        localStorage.removeItem('authToken');
        localStorage.removeItem('user');
    }

    isAuthenticated() {
        return !!this.token;
    }

    getCurrentUser() {
        const user = localStorage.getItem('user');
        return user ? JSON.parse(user) : null;
    }
}

// Usage
const authService = new AuthService();

// Login
const loginResult = await authService.login('username', 'password');
if (loginResult.success) {
    console.log('User logged in:', loginResult.user);
}

// Check if authenticated
if (authService.isAuthenticated()) {
    const profile = await authService.getProfile();
    console.log('User profile:', profile);
}
```

### React Hook for Authentication

```jsx
import { useState, useEffect, createContext, useContext } from 'react';

// Create Auth Context
const AuthContext = createContext();

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
};

// Auth Provider Component
export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [token, setToken] = useState(localStorage.getItem('authToken'));
    const [loading, setLoading] = useState(true);

    const baseURL = 'http://127.0.0.1:8000/api/usermanagement';

    useEffect(() => {
        if (token) {
            fetchUserProfile();
        } else {
            setLoading(false);
        }
    }, [token]);

    const fetchUserProfile = async () => {
        try {
            const response = await fetch(`${baseURL}/profile/`, {
                headers: {
                    'Authorization': `Token ${token}`,
                },
            });

            if (response.ok) {
                const data = await response.json();
                setUser(data.user);
            } else {
                // Token invalid
                logout();
            }
        } catch (error) {
            console.error('Profile fetch error:', error);
            logout();
        } finally {
            setLoading(false);
        }
    };

    const login = async (username, password) => {
        try {
            const response = await fetch(`${baseURL}/auth/login/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password })
            });

            const data = await response.json();
            
            if (data.success) {
                setToken(data.token);
                setUser(data.user);
                localStorage.setItem('authToken', data.token);
                return { success: true };
            } else {
                return { success: false, error: data.message };
            }
        } catch (error) {
            return { success: false, error: 'Network error' };
        }
    };

    const googleLogin = async (accessToken) => {
        try {
            const response = await fetch(`${baseURL}/auth/google/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ access_token: accessToken })
            });

            const data = await response.json();
            
            if (data.success) {
                setToken(data.token);
                setUser(data.user);
                localStorage.setItem('authToken', data.token);
                return { success: true };
            } else {
                return { success: false, error: data.message };
            }
        } catch (error) {
            return { success: false, error: 'Network error' };
        }
    };

    const register = async (userData) => {
        try {
            const response = await fetch(`${baseURL}/auth/register/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(userData)
            });

            const data = await response.json();
            
            if (data.success) {
                setToken(data.token);
                setUser(data.user);
                localStorage.setItem('authToken', data.token);
                return { success: true };
            } else {
                return { success: false, errors: data.errors };
            }
        } catch (error) {
            return { success: false, error: 'Network error' };
        }
    };

    const logout = async () => {
        try {
            if (token) {
                await fetch(`${baseURL}/auth/logout/`, {
                    method: 'POST',
                    headers: {
                        'Authorization': `Token ${token}`,
                    },
                });
            }
        } catch (error) {
            console.error('Logout error:', error);
        } finally {
            setToken(null);
            setUser(null);
            localStorage.removeItem('authToken');
        }
    };

    const value = {
        user,
        token,
        loading,
        login,
        googleLogin,
        register,
        logout,
        isAuthenticated: !!token && !!user,
    };

    return (
        <AuthContext.Provider value={value}>
            {children}
        </AuthContext.Provider>
    );
};

// Usage in components
const LoginComponent = () => {
    const { login, googleLogin, loading } = useAuth();
    const [credentials, setCredentials] = useState({ username: '', password: '' });

    const handleLogin = async (e) => {
        e.preventDefault();
        const result = await login(credentials.username, credentials.password);
        if (result.success) {
            // Redirect to dashboard
        } else {
            alert(result.error);
        }
    };

    const handleGoogleSuccess = async (credentialResponse) => {
        const result = await googleLogin(credentialResponse.credential);
        if (result.success) {
            // Redirect to dashboard
        } else {
            alert(result.error);
        }
    };

    if (loading) return <div>Loading...</div>;

    return (
        <div>
            <form onSubmit={handleLogin}>
                <input
                    type="text"
                    placeholder="Username"
                    value={credentials.username}
                    onChange={(e) => setCredentials({...credentials, username: e.target.value})}
                />
                <input
                    type="password"
                    placeholder="Password"
                    value={credentials.password}
                    onChange={(e) => setCredentials({...credentials, password: e.target.value})}
                />
                <button type="submit">Login</button>
            </form>
            
            <GoogleLogin
                onSuccess={handleGoogleSuccess}
                onError={() => alert('Google login failed')}
            />
        </div>
    );
};
```

---

## Error Handling

### Common Error Responses

**Authentication Failed (400):**
```json
{
    "success": false,
    "message": "Invalid credentials",
    "errors": ["Username or password is incorrect"]
}
```

**Validation Error (400):**
```json
{
    "success": false,
    "message": "Registration failed",
    "errors": {
        "email": ["User with this email already exists."],
        "password": ["Password must be at least 8 characters long."]
    }
}
```

**Unauthorized (401):**
```json
{
    "detail": "Invalid token."
}
```

**Forbidden (403):**
```json
{
    "success": false,
    "message": "Only students can create student profiles"
}
```

### Error Handling Best Practices

```javascript
const handleApiError = (error, response) => {
    // Network error
    if (!response) {
        return 'Network error. Please check your connection.';
    }

    // Server errors
    if (response.status >= 500) {
        return 'Server error. Please try again later.';
    }

    // Client errors
    if (response.status >= 400) {
        if (response.status === 401) {
            // Clear auth and redirect to login
            localStorage.removeItem('authToken');
            window.location.href = '/login';
            return 'Session expired. Please login again.';
        }

        if (response.status === 403) {
            return 'You do not have permission to perform this action.';
        }

        // Try to get error message from response
        try {
            const errorData = JSON.parse(error.message);
            return errorData.message || 'Request failed';
        } catch {
            return 'Request failed';
        }
    }

    return 'An unexpected error occurred';
};
```

---

## Security Best Practices

### 1. Token Storage
- **✅ Do:** Use `localStorage` for persistent sessions
- **✅ Do:** Use `sessionStorage` for temporary sessions
- **❌ Don't:** Store tokens in cookies without proper security flags
- **❌ Don't:** Store tokens in plain text files

### 2. Token Transmission
- **✅ Do:** Always use HTTPS in production
- **✅ Do:** Send tokens in Authorization header
- **❌ Don't:** Send tokens in URL parameters
- **❌ Don't:** Log tokens in console/files

### 3. Token Validation
```javascript
// Check if token exists and user is authenticated
const isValidSession = () => {
    const token = localStorage.getItem('authToken');
    const user = localStorage.getItem('user');
    
    if (!token || !user) {
        return false;
    }
    
    // Additional validation can be added here
    return true;
};

// Redirect to login if not authenticated
const requireAuth = () => {
    if (!isValidSession()) {
        window.location.href = '/login';
        return false;
    }
    return true;
};
```

### 4. Auto Logout on Token Expiry
```javascript
// Monitor API responses for 401 errors
const setupAuthMonitoring = () => {
    // Intercept all fetch requests
    const originalFetch = window.fetch;
    window.fetch = async (...args) => {
        const response = await originalFetch(...args);
        
        if (response.status === 401) {
            // Token expired
            localStorage.removeItem('authToken');
            localStorage.removeItem('user');
            window.location.href = '/login';
        }
        
        return response;
    };
};
```

---

## Testing Guide

### 1. API Testing with cURL

**Test Health Endpoint:**
```bash
curl -X GET http://127.0.0.1:8000/api/usermanagement/health/
```

**Test Registration:**
```bash
curl -X POST http://127.0.0.1:8000/api/usermanagement/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "first_name": "Test",
    "last_name": "User",
    "password": "TestPassword123!",
    "confirm_password": "TestPassword123!",
    "user_type": "student"
  }'
```

**Test Login:**
```bash
curl -X POST http://127.0.0.1:8000/api/usermanagement/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "TestPassword123!"
  }'
```

**Test Authenticated Endpoint:**
```bash
curl -X GET http://127.0.0.1:8000/api/usermanagement/profile/ \
  -H "Authorization: Token your-token-here"
```

### 2. Frontend Testing Checklist

- [ ] Google OAuth button appears and is clickable
- [ ] Google OAuth flow redirects correctly
- [ ] Traditional login form validates inputs
- [ ] Registration form handles validation errors
- [ ] Token is stored correctly after login
- [ ] Authenticated requests include token in headers
- [ ] Auto-logout works on token expiry
- [ ] User profile loads correctly
- [ ] Logout clears stored data
- [ ] Error messages display properly

### 3. Integration Testing

```javascript
// Example test suite (Jest)
describe('Authentication Service', () => {
    let authService;

    beforeEach(() => {
        authService = new AuthService();
        localStorage.clear();
    });

    test('should login with valid credentials', async () => {
        const result = await authService.login('testuser', 'password');
        expect(result.success).toBe(true);
        expect(result.user).toBeDefined();
        expect(localStorage.getItem('authToken')).toBeTruthy();
    });

    test('should handle login failure', async () => {
        const result = await authService.login('invalid', 'credentials');
        expect(result.success).toBe(false);
        expect(result.error).toBeDefined();
    });

    test('should logout correctly', async () => {
        // First login
        await authService.login('testuser', 'password');
        
        // Then logout
        await authService.logout();
        expect(localStorage.getItem('authToken')).toBeNull();
        expect(authService.isAuthenticated()).toBe(false);
    });
});
```

---

## Support and Questions

For technical support or questions about the authentication system:

1. **Check this documentation** for common implementation patterns
2. **Review error responses** in the Error Handling section
3. **Test with cURL** to verify API functionality
4. **Contact the backend team** for API-specific issues

---

**Version:** 1.0.0  
**Last Updated:** January 2025  
**Maintained by:** IQRA Backend Team