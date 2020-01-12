from django.contrib import admin
from django.urls import path

from config.views import home, HomeView
from videos.views import VideoListView

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('home/', home, name='home'),
    path('home/', HomeView.as_view(), name='home'),
    path('video/', VideoListView.as_view(), name='video-list')
]
