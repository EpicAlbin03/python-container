from django.contrib import admin

from .models import Course, Student


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):  # type: ignore
    list_display = ['code', 'name']
    search_fields = ['name', 'code']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):  # type: ignore
    list_display = ['name', 'email', 'course', 'grade', 'is_active']
    list_filter = ['course', 'grade', 'is_active']
    search_fields = ['name', 'email']
    list_per_page = 20
