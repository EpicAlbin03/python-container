from django.http import HttpRequest

from .models import Student


def students_context(request: HttpRequest):
    students = Student.objects.all()
    return {'students_count': len(students)}
