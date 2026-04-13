from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from studentplatform.serializers import CourseSerializer, StudentSerializer

from .models import Course, Student


# GET, POST /students/
class StudentListCreateAPIView(generics.ListCreateAPIView[Student]):
    # queryset = Student.objects.all() # no relations / fk
    queryset = Student.objects.select_related('course').all()  # more efficient
    serializer_class = StudentSerializer

    # only admin users can create students
    def get_permissions(self):
        if self.request.method == 'POST':
            permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    # filter students by grade or active status
    def get_queryset(self):
        queryset = super().get_queryset()
        grade = self.request.query_params.get('grade')
        is_active = self.request.query_params.get('is_active')

        if grade is not None:
            queryset = queryset.filter(grade=grade)
        if is_active is not None:
            # bools require .lower() to work with query params
            queryset = queryset.filter(is_active=is_active.lower() == 'true')

        return queryset


# GET, PUT, PATCH, DELETE /students/<int:pk>/
class StudentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView[Student]):
    queryset = Student.objects.select_related('course').all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


# GET, POST /courses/
class CourseListCreateAPIView(generics.ListCreateAPIView[Course]):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


# GET, PUT, PATCH, DELETE /courses/<int:pk>/
class CourseRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView[Course]):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


# GET /courses/<int:pk>/students/
class CourseStudentListAPIView(generics.ListAPIView[Student]):
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        course = get_object_or_404(Course, pk=self.kwargs['pk'])
        return course.students.select_related('course').all()
