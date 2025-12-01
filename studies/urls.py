from django.urls import path
from .apps import StudiesConfig
from rest_framework.routers import DefaultRouter

from studies import views

app_name = StudiesConfig.name

router = DefaultRouter()
router.register(r'courses', views.CourseViewSet, basename='courses')

urlpatterns = [
    path('lesson_create/', views.LessonCreateAPIView.as_view(), name='lesson_create'),
    path('lessons/', views.LessonListAPIView.as_view(), name='lessons'),
    path('lesson/<int:pk>/', views.LessonRetrieveAPIView.as_view(), name='lesson'),
    path('lesson_update/<int:pk>/', views.LessonUpdateAPIView.as_view(), name='lesson_update'),
    path('lesson_delete/<int:pk>/', views.LessonDestroyAPIView.as_view(), name='lesson_delete'),
    path('subscribe/', views.SubscribeAPIView.as_view(), name='subscribe'),
] + router.urls
