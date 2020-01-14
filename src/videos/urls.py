from django.urls import path

from videos.views import VideoListView, VideoDetailView, VideoCreateView, VideoUpdateView, VideoDeleteView

app_name = 'videos'

urlpatterns = [
    path('', VideoListView.as_view(), name='list'),
    path('create', VideoCreateView.as_view(), name='create'),
    # path('videos/<int:pk>', VideoDetailView.as_view(), name='video-detail'),
    path('<slug>', VideoDetailView.as_view(), name='detail'),
    path('<slug>/edit/', VideoUpdateView.as_view(), name='update'),
    path('<slug>/delete/', VideoDeleteView.as_view(), name='delete')

]
