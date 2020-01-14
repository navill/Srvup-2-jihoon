from django.shortcuts import render, get_object_or_404
from django.views.generic import *

from .mixins import MemberRequiredMixin, StaffMemberRequiredMixin
from .forms import VideoForm
from .models import Video


# CRUDL
class VideoCreateView(StaffMemberRequiredMixin, CreateView):
    # queryset = Video.objects.all()  # ImproperlyConfigured 에러를 일으킨다.
    model = Video
    form_class = VideoForm


class VideoDetailView(MemberRequiredMixin, DetailView):
    queryset = Video.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(VideoDetailView, self).get_context_data(**kwargs)
        return context


class VideoListView(ListView):
    def get_queryset(self):
        q = self.request.GET.get('q')
        qs = Video.objects.all()
        if q:  # query string이 있을 경우
            qs = qs.filter(title__icontains=q)
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(VideoListView, self).get_context_data(**kwargs)
        return context


class VideoUpdateView(StaffMemberRequiredMixin, UpdateView):
    queryset = Video.objects.all()
    form_class = VideoForm


class VideoDeleteView(StaffMemberRequiredMixin, DeleteView):
    queryset = Video.objects.all()
    success_url = '/videos/'
