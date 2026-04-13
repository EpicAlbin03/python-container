from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .api_views import (
    CourseListCreateAPIView,
    CourseRetrieveUpdateDestroyAPIView,
    CourseStudentListAPIView,
    StudentListCreateAPIView,
    StudentRetrieveUpdateDestroyAPIView,
)

# pk = primary key
urlpatterns = [
    path(
        'token/',
        TokenObtainPairView.as_view(),
        name='token_obtain',
    ),
    path(
        'token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh',
    ),
    path(
        'students/',
        StudentListCreateAPIView.as_view(),
    ),
    path(
        'students/<int:pk>/',
        StudentRetrieveUpdateDestroyAPIView.as_view(),
    ),
    path(
        'courses/',
        CourseListCreateAPIView.as_view(),
    ),
    path(
        'courses/<int:pk>/',
        CourseRetrieveUpdateDestroyAPIView.as_view(),
    ),
    path(
        'courses/<int:pk>/students/',
        CourseStudentListAPIView.as_view(),
    ),
]
