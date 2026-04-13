from typing import cast

from django import forms
from django.db import models

from .models import Course, Student


class CourseChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj: models.Model) -> str:
        return cast(Course, obj).name


class StudentForm(forms.ModelForm):
    course = CourseChoiceField(
        queryset=Course.objects.all(),
        empty_label=None,
    )

    class Meta:
        model = Student
        fields = '__all__'
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }
