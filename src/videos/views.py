from django.shortcuts import render
from django.views.generic import *

from .models import Video


# Create your views here.

# CRUDL

class VideoCreateView(CreateView):
    queryset = Video.objects.all()


class VideoDetailView(DetailView):
    queryset = Video.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(VideoDetailView, self).get_context_data(**kwargs)
        print(context)
        # {'paginator': None, 'page_obj': None, 'is_paginated': False,
        # 'object_list': <QuerySet [<Video: django 2.2>, <Video: django 1.11>]>,
        # 'video_list': <QuerySet [<Video: django 2.2>, <Video: django 1.11>]>,
        # 'view': <videos.views.VideoListView object at 0x10733c1d0>}
        return context


class VideoListView(ListView):
    queryset = Video.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(VideoListView, self).get_context_data(**kwargs)
        print(context)
        # {'object': <Video: django 2.2>, 'video': <Video: django 2.2>,
        # 'view': <videos.views.VideoDetailView object at 0x10c15d4a8>}
        return context


class VideoUpdateView(UpdateView):
    queryset = Video.objects.all()


class VideoDeleteView(DeleteView):
    queryset = Video.objects.all()
