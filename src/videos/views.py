from django.shortcuts import render
from django.views.generic import *

from .models import Video


# Create your views here.

# CRUDL

class VideoCreateView(CreateView):
    queryset = Video.objects.all()
    template_name = 'index.html'


class VideoDetailView(DetailView):
    queryset = Video.objects.all()


class VideoListView(ListView):
    queryset = Video.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(VideoListView, self).get_context_data(**kwargs)
        print(context)
        return context


class VideoUpdateView(UpdateView):
    queryset = Video.objects.all()


class VideoDeleteView(DeleteView):
    queryset = Video.objects.all()
