# Google OAuth Setup Guide

## Overview
This guide explains how to set up Google OAuth authentication for the IQRA E-Learning Platform.

## Google Cloud Console Setup

### 1. Create a Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable the Google+ API and Google OAuth2 API

### 2. Create OAuth 2.0 Credentials
1. Navigate to **APIs & Services** > **Credentials**
2. Click **+ CREATE CREDENTIALS** > **OAuth client ID**
3. Choose **Web application** as application type
4. Add authorized origins:
   - `http://localhost:8000` (for development)
   - Your production domain
5. Add authorized redirect URIs:
   - `http://localhost:8000/auth/callback` (for development)
   - Your production callback URL
6. Save and note down:
   - **Client ID**
   - **Client Secret**

## Frontend Integration

### JavaScript Example (Vanilla JS)
```javascript
// Initialize Google OAuth
function initializeGoogleAuth() {
    gapi.load('auth2', function() {
        gapi.auth2.init({
            client_id: 'YOUR_GOOGLE_CLIENT_ID'
        });
    });
}

// Handle Google Sign-In
function handleGoogleSignIn() {
    const authInstance = gapi.auth2.getAuthInstance();
    authInstance.signIn().then(function(googleUser) {
        const accessToken = googleUser.getAuthResponse().access_token;
        
        // Send token to your backend
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
                // Store authentication token
                localStorage.setItem('authToken', data.token);
                // Redirect to dashboard or handle success
                console.log('Login successful:', data.user);
            }
        });
    });
}
```

### React Example
```jsx
import { GoogleLogin } from '@react-oauth/google';

function GoogleAuthButton() {
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
                localStorage.setItem('authToken', data.token);
                // Handle successful login
            }
        } catch (error) {
            console.error('Login failed:', error);
        }
    };

    return (
        <GoogleLogin
            onSuccess={handleGoogleSuccess}
            onError={() => console.log('Login Failed')}
        />
    );
}
```

## API Testing with cURL

### Test Google Authentication
```bash
curl -X POST http://localhost:8000/api/usermanagement/auth/google/ \
  -H "Content-Type: application/json" \
  -d '{
    "access_token": "YOUR_GOOGLE_ACCESS_TOKEN"
  }'
```

### Expected Response
```json
{
    "success": true,
    "message": "Google authentication successful",
    "user": {
        "id": 1,
        "username": "user@example.com",
        "email": "user@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "user_type": "student",
        "is_verified": true
    },
    "token": "your-auth-token-here",
    "is_new_user": false
}
```

## Security Notes

1. **Never expose Client Secret** in frontend code
2. **Use HTTPS** in production
3. **Validate tokens** on the backend
4. **Implement rate limiting** for authentication endpoints
5. **Set appropriate CORS** headers

## Environment Variables (Optional)
You can add these to your Django settings for better security:

```python
# settings.py
GOOGLE_OAUTH2_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
GOOGLE_OAUTH2_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
```