from django.http import Http404
from django.views.generic import *

from videos.mixins import MemberRequiredMixin, StaffMemberRequiredMixin
# from .forms import VideoForm
from .forms import CourseForm
from .models import Course


# CRUDL
class CourseCreateView(StaffMemberRequiredMixin, CreateView):
    model = Course
    form_class = CourseForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        print(id(obj), id(form))
        obj.user = self.request.user
        obj.save()
        # int_passed = form.cleaned_data.get('number')  # extra field
        return super(CourseCreateView, self).form_valid(form)


class CourseDetailView(MemberRequiredMixin, DetailView):
    queryset = Course.objects.all()

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        # obj = Course.objects.get(slug=slug) # MultipleOjbectsReturned 에러(동일한 slug가 여럿 존재할 경우)
        obj = Course.objects.filter(slug=slug)
        if obj.exists():
            return obj.first()
        raise Http404


class CourseListView(ListView):
    def get_queryset(self):
        q = self.request.GET.get('q')
        qs = Course.objects.all()
        if q:  # query string이 있을 경우
            qs = qs.filter(title__icontains=q)
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CourseListView, self).get_context_data(**kwargs)
        return context


class CourseUpdateView(StaffMemberRequiredMixin, UpdateView):
    queryset = Course.objects.all()
    form_class = CourseForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        if not self.request.user.is_staff:
            obj.user = self.request.user
        obj.save()
        return super(CourseUpdateView, self).form_valid(form)

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        obj = Course.objects.filter(slug=slug)
        if obj.exists():
            return obj.first()
        raise Http404


class CourseDeleteView(StaffMemberRequiredMixin, DeleteView):
    queryset = Course.objects.all()
    success_url = '/videos/'

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        obj = Course.objects.filter(slug=slug)
        if obj.exists():
            return obj.first()
        raise Http404
