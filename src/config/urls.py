from django.contrib import admin
from django.urls import path

from config.views import home, HomeView
from videos.views import VideoListView, VideoDetailView, VideoCreateView, VideoUpdateView, VideoDeleteView

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('home/', home, name='home'),
    path('', HomeView.as_view(), name='home'),
    path('videos/', VideoListView.as_view(), name='video-list'),
    path('videos/create', VideoCreateView.as_view(), name='video-create'),
    # path('videos/<int:pk>', VideoDetailView.as_view(), name='video-detail'),
    path('videos/<slug>', VideoDetailView.as_view(), name='video-detail-slug'),
    path('videos/<slug>/edit/', VideoUpdateView.as_view(), name='video-update'),
    path('videos/<slug>/delete/', VideoDeleteView.as_view(), name='video-delete')

]
