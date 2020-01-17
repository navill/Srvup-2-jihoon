from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import *
from videos.mixins import MemberRequiredMixin, StaffMemberRequiredMixin
# from .forms import VideoForm
from .forms import CourseForm
from .models import Course, Lecture, MyCourses


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


class LectureDetailView(MemberRequiredMixin, DetailView):
    def get_object(self, queryset=None):
        course_slug = self.kwargs.get('cslug')
        lecture_slug = self.kwargs.get('lslug')
        obj = get_object_or_404(Lecture, course__slug=course_slug, slug=lecture_slug)
        return obj


class CourseDetailView(MemberRequiredMixin, DetailView):

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        # obj = Course.objects.get(slug=slug) # MultipleOjbectsReturned 에러(동일한 slug가 여럿 존재할 경우)
        qs = Course.objects.filter(slug=slug).owned(self.request.user)  # -> is_owner 속성 사용 가능
        if qs.exists():
            return qs.first()
        raise Http404


class CoursePurchaseView(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, slug=None):
        slug = self.kwargs.get('slug')
        qs = Course.objects.filter(slug=slug).owned(self.request.user)  # -> is_owner 속성 사용 가능
        # print(qs)
        if qs.exists():
            user = self.request.user
            if user.is_authenticated:
                my_courses = user.mycourses  # o2o관계이기 때문에 mycourses_set(x)
                # ----거래에 필요한 처리----
                my_courses.courses.add(qs.first())
                return qs.first().get_absolute_url()
        raise Http404


class CourseListView(ListView):
    def get_queryset(self):
        q = self.request.GET.get('q')
        qs = Course.objects.all()
        user = self.request.user
        if q:  # query string이 있을 경우
            qs = qs.filter(title__icontains=q)
        if user.is_authenticated:
            qs = qs.owned(user)
        return qs


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
