from django.contrib import admin
from django.urls import path, include

from config.views import home, HomeView
import debug_toolbar
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('courses/', include('courses.urls')),
    path('videos/', include('videos.urls')),
]

from django.conf import settings
from django.conf.urls.static import static

# local(development) 개발 시 아래의 static과 media 파일을 사용한다.
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    urlpatterns = [path('__debug__/', include(debug_toolbar.urls))] + urlpatterns