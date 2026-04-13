from rest_framework import serializers

from .models import Course, Student


class CourseSerializer(serializers.ModelSerializer[Course]):
    class Meta:
        model = Course
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer[Student]):
    # course_detail = CourseSerializer(read_only=True, source="course")

    class Meta:
        model = Student
        fields = '__all__'
        # fields = [
        #     "id",
        #     "name",
        #     "email",
        #     "date_of_birth",
        #     "grade",
        #     "is_active",
        #     "course", # accepts a course id on POST/PUT/PATCH
        #     "course_detail", # returns full course object on GET
        #     "created_at",
        # ]
