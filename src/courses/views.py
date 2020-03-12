from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import *

from analytics.models import CourseEventView
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
        obj.user = self.request.user
        obj.save()
        # int_passed = form.cleaned_data.get('number')  # extra field
        return super(CourseCreateView, self).form_valid(form)


class LectureDetailView(View):
    def get(self, request, cslug=None, lslug=None, *args, **kwargs):
        user = request.user
        # cslug에 해당하는 Course 객체 중, MyCourse에 등록되어있는 course를 prefetch_related(lecture_set)와 함께 가져온다
        # course_obj = filter:cslug + prefetch_related(lecture_set) + MyCourses.filter(user)
        qs = Course.objects.filter(slug=cslug).lectures().owned(user)
        if not qs.exists():
            raise Http404
        # course_obj
        course_ = qs.first()
        if user.is_authenticated:
            view_event, created = CourseEventView.objects.get_or_create(user=user, course=course_)
            if view_event:
                view_event.views += 1
                view_event.save()
        lecture_qs = course_.lecture_set.filter(slug=lslug)  # == Lecture.objects.filter(course=course_)
        if not lecture_qs.exists():
            raise Http404
        # lecture_obj
        obj = lecture_qs.first()

        context = {
            'object': obj,
            'course': course_,
        }
        # 소유자(MyCourse에 등록된 강좌)만 접속할 수 있도록
        # print('Lecture_detail:', course_.is_owner)
        # -> is_onwer가 비어있을 경우 False, 소유한 강좌가 하나라도 있을 경우 True
        if not course_.is_owner and not obj.free:  # and not user.is_member:
            return render(request, 'courses/must_purchase.html', {'object': course_})
        return render(request, 'courses/lecture_detail.html', context=context)


class CourseDetailView(DetailView):

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        user = self.request.user
        qs = None
        # obj = Course.objects.get(slug=slug) # MultipleOjbectsReturned 에러(동일한 slug가 여럿 존재할 경우)
        qs = Course.objects.filter(slug=slug).lectures().owned(user)
        if qs.exists():
            obj = qs.first()
            if self.request.user.is_authenticated:
                view_event, created = CourseEventView.objects.get_or_create(user=user, course=obj)
                if view_event:
                    view_event.views += 1
                    view_event.save()
            return obj
        raise Http404


class CoursePurchaseView(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, slug=None):
        slug = self.kwargs.get('slug')
        qs = Course.objects.filter(slug=slug).owned(self.request.user)  # -> is_owner 속성 사용 가능
        # print(qs)
        if qs.exists():
            user = self.request.user
            print(dir(user))
            if user.is_authenticated:
                my_courses = user.mycourses  # o2o관계이기 때문에 mycourses_set(x)
                # ----거래에 필요한 처리----
                my_courses.courses.add(qs.first())
                return qs.first().get_absolute_url()
        raise Http404


class CourseListView(ListView):
    # 페이지당 9개씩 출력
    paginate_by = 9

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

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
