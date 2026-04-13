# Student Management Platform — Phase 4

## Overview

Add **authentication and security** to your student platform. By the end, the website requires login for protected pages, and the API requires JWT tokens.

---

## What Changes From Yesterday

| Yesterday (Phase 3)                | Today (Phase 4)                 |
| ---------------------------------- | ------------------------------- |
| All pages accessible without login | Protected pages require login   |
| API open to anyone                 | API requires JWT token          |
| No login/logout pages              | Full login/logout flow          |
| No security configuration          | CORS, env variables, .gitignore |

---

## Setup

```bash
pip install djangorestframework-simplejwt django-cors-headers
```

---

## Part 1: Protect the Website

### 1.1 Create login and logout views

In `core/views.py`, add two new views. You'll need these imports:

```python
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
```

**login_view:**

- If the request is GET → render `login.html`
- If the request is POST → get `username` and `password` from `request.POST`
- Use `authenticate(request, username=..., password=...)` to check credentials
- If the user is valid → call `login(request, user)` and redirect to `student_list`
- If invalid → render `login.html` again with an error message in the context

**logout_view:**

- Call `logout(request)` and redirect to `home`

### 1.2 Create the login template

Create `core/templates/login.html`. It should:

- Extend `base.html`
- Show `{{ error }}` if present (for invalid credentials)
- Have a `<form method="POST">` with `{% csrf_token %}`
- Include username input (`type="text"`), password input (`type="password"`), and a submit button

### 1.3 Add URLs

Add to `core/urls.py`:

```python
path('login/', views.login_view, name='login'),
path('logout/', views.logout_view, name='logout'),
```

### 1.4 Configure settings

Add to `settings.py`:

```python
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'student_list'
```

### 1.5 Protect views with @login_required

Add `@login_required` above each view that should require login. Put the decorator on the line before `def`:

```python
@login_required
def student_list(request):
    ...
```

Protect these views: `student_list`, `student_detail`, `add_student`, `edit_student`, `delete_student`, `course_list`, `course_detail`.

Keep these public: `home`, `about`, `login_view`.

### 1.6 Update navigation

Update `base.html` to show different links depending on whether the user is logged in. Use `{% if user.is_authenticated %}` in the nav:

- **Logged in:** show Students, Courses, Add Student, Admin, a greeting (`Hi, {{ user.username }}!`), and Logout
- **Not logged in:** show About and Login only

### 1.7 Test the website auth

- Open an incognito window and visit `/students/` → should redirect to `/login/`
- Log in with your superuser credentials → should see the students page
- Click Logout → should redirect to home
- Try `/students/` again → should redirect to login

---

## Part 2: Protect the API

### 2.1 Configure JWT authentication

Add to `settings.py`:

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}
```

### 2.2 Add token endpoints

In `core/api_urls.py`, add imports and URL patterns for JWT:

```python
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
```

Add two paths:

- `token/` → `TokenObtainPairView` (this is where clients POST username/password to get tokens)
- `token/refresh/` → `TokenRefreshView` (this is where clients POST a refresh token to get a new access token)

### 2.3 Protect API views

In `core/api_views.py`, import `IsAuthenticated`:

```python
from rest_framework.permissions import IsAuthenticated
```

Then add `permission_classes = [IsAuthenticated]` to every API view class. For example:

```python
class StudentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]   # ← add this line
```

Do this for all your API view classes.

### 2.4 Test the API auth

**Without a token (should fail):**

```bash
curl.exe http://127.0.0.1:8000/api/students/
# Expected: 401 Unauthorized
```

**Get a token:**

```bash
curl.exe -X POST http://127.0.0.1:8000/api/token/ -H "Content-Type: application/json" --data-raw "{""username"":""yourusername"",""password"":""yourpassword""}"
# Returns: {"access": "eyJ...", "refresh": "eyJ..."}
```

**Use the token (should work):**

```bash
curl.exe http://127.0.0.1:8000/api/students/ -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"
# Expected: 200 OK with student data
```

Note: on Mac/Linux use `curl` with single quotes. On Windows PowerShell use `curl.exe` with `""` for escaping as shown above.

You can also test by visiting `http://127.0.0.1:8000/api/token/` in the browser — DRF's browsable API has a form you can use.

---

## Part 3: Security Basics

### 3.1 CORS

Install and configure `django-cors-headers` so that a future Vue frontend can call your API:

```python
# settings.py
INSTALLED_APPS = [..., 'corsheaders']

# Add CorsMiddleware BEFORE CommonMiddleware in MIDDLEWARE:
MIDDLEWARE = [
    ...,
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    ...,
]

CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
]
```

---

## Checklist

- [x] Login view and template working
- [x] Logout view working
- [x] Navigation changes based on auth status
- [x] @login_required on all protected views
- [x] Public pages (home, about) still accessible without login
- [x] JWT configured in settings.py
- [x] Token endpoints added (/api/token/ and /api/token/refresh/)
- [x] IsAuthenticated on all API views
- [x] API returns 401 without token
- [x] API returns 200 with valid token
- [x] CORS configured
- [x] .env and .gitignore created

---

## Bonus Challenges

- [x] **Registration page** — create a signup view that creates new users with `User.objects.create_user()` (I used UserCreationForm)
- [x] **Password change** — add a page where logged-in users can change their password
- [ ] **User-specific data** — only show students created by the logged-in user
- [x] **Role-based access** — admin users can delete, regular users can only view

---

## When You're Done

See dependencies in `pyproject.toml`.

```bash
pip freeze > requirements.txt
git add .
git commit -m "Session 6: Auth, JWT, security, CORS, env variables"
git push
```

**Next session**: Containerization with Docker.
