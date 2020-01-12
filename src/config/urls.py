from django.contrib import admin
from django.urls import path

from config.views import home, HomeView
from videos.views import VideoListView, VideoDetailView

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('home/', home, name='home'),
    path('', HomeView.as_view(), name='home'),
    path('videos/', VideoListView.as_view(), name='video-list'),
    path('videos/<int:pk>', VideoDetailView.as_view(), name='video-detail')
]
