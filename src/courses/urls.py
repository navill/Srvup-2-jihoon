from django.contrib import admin
from django.urls import path

from config.views import home, HomeView
from .views import CourseListView, CourseDetailView, CourseDeleteView, CourseCreateView, CourseUpdateView

app_name = 'courses'

urlpatterns = [
    path('', CourseListView.as_view(), name='list'),
    path('create/', CourseCreateView.as_view(), name='create'),
    path('<slug>', CourseDetailView.as_view(), name='detail'),
    path('<slug>/edit/', CourseUpdateView.as_view(), name='update'),
    path('<slug>/delete/', CourseDeleteView.as_view(), name='delete')

]
