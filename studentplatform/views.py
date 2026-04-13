from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserCreationForm
from django.db.models import Q
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render, resolve_url
from django.utils.http import url_has_allowed_host_and_scheme

from .forms import StudentForm
from .models import Course, Student


def _get_safe_redirect_url(request: HttpRequest) -> str:
    """Get a safe URL to redirect to after login."""
    redirect_to = request.POST.get('next') or request.GET.get('next')
    if redirect_to and url_has_allowed_host_and_scheme(
        url=redirect_to,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return redirect_to
    return resolve_url('student_list')


def login_view(request: HttpRequest):
    """Login page"""
    if request.user.is_authenticated:
        return redirect('student_list')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect(_get_safe_redirect_url(request))
    else:
        form = AuthenticationForm(request)

    return render(request, 'account/login.html', {'form': form, 'next': request.GET.get('next', '')})


@login_required
def logout_view(request: HttpRequest):
    """Logout view"""
    logout(request)
    return redirect('home')


def signup_view(request: HttpRequest):
    """Signup page"""
    if request.user.is_authenticated:
        return redirect('student_list')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('student_list')
    else:
        form = UserCreationForm()

    return render(request, 'account/signup.html', {'form': form})


@login_required
def password_change_view(request: HttpRequest):
    """Change password page"""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('student_list')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'account/password_change.html', {'form': form})


def home(request: HttpRequest):
    """Home page — welcome message."""
    return render(request, 'home.html')


def about(request: HttpRequest):
    """About page — course information."""
    return render(request, 'about.html')


@login_required
def student_list(request: HttpRequest):
    """List all students in a table."""
    search_query = request.GET.get('q', '').strip()
    student_queryset = Student.objects.select_related('course')

    if search_query:
        students = student_queryset.filter(Q(name__icontains=search_query) | Q(email__icontains=search_query))
    else:
        students = student_queryset.all()

    return render(
        request,
        'student_list.html',
        {
            'students': students,
            'count': students.count(),
            'search_query': search_query,
        },
    )


@login_required
def student_detail(request: HttpRequest, student_id: int):
    """Show details for a single student."""
    student = get_object_or_404(Student, id=student_id)
    return render(request, 'student_detail.html', {'student': student})


@staff_member_required
def add_student(request: HttpRequest):
    """Show a form (GET) or process the submission (POST)."""
    if request.method == 'POST':
        form = StudentForm(request.POST)  # creates new student on form.save()
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm()

    return render(request, 'add_student.html', {'form': form})


@staff_member_required
def delete_student(request: HttpRequest, student_id: int):
    """Delete a student and redirect to the list."""
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        student.delete()
    return redirect('student_list')


@staff_member_required
def edit_student(request: HttpRequest, student_id: int):
    """Show a form pre-filled with existing data (GET) or process the submission (POST)."""
    student = get_object_or_404(Student, id=student_id)

    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)  # updates student passed to instance on form.save()
        if form.is_valid():
            form.save()
            return redirect('student_detail', student_id=student_id)
    else:
        form = StudentForm(instance=student)

    return render(request, 'edit_student.html', {'form': form, 'student': student})


@login_required
def course_list(request: HttpRequest):
    """List all courses in a table."""
    courses = Course.objects.all()
    return render(request, 'course_list.html', {'courses': courses, 'count': len(courses)})


@login_required
def course_detail(request: HttpRequest, course_id: int):
    """Show details for a single course."""
    course = get_object_or_404(Course, id=course_id)
    students = course.students.all()
    return render(request, 'course_detail.html', {'course': course, 'students': students})
