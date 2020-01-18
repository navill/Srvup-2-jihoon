from django.contrib import admin
from django.urls import path

from config.views import home, HomeView
from .views import CategoryListView, CategoryDetailView

app_name = 'categories'

urlpatterns = [
    path('', CategoryListView.as_view(), name='list'),
    path('<slug>/', CategoryDetailView.as_view(), name='detail'),

]
