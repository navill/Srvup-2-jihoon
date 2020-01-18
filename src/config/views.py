from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import View

from analytics.models import CourseEventView
from courses.models import Course


def home(request):
    return HttpResponse('Hello')


class HomeView(View):
    def get(self, request, *args, **kwargs):
        course_qs = Course.objects.all().owned(request.user)
        qs = course_qs.featured().order_by("?")[:6]

        event_qs = CourseEventView.objects.all().prefetch_related('course')

        if self.request.user.is_authenticated:
            event_views = event_qs.filter(user=request.user)
        else:
            event_views = event_qs.filter(views__gte=10)

        event_views = event_views.order_by('views')[:20]
        ids_ = [x.course.id for x in event_views]
        rec_courses = course_qs.filter(id__in=ids_).order_by("?")

        context = {
            'rec_courses': rec_courses,
            'qs': qs,
            'name': 'navill',
        }
        return render(request, 'home.html', context=context)

    # def post(self, request, *args, **kwargs):
    #     return HttpResponse("Hello")
    #
    # def put(self, request, *args, **kwargs):
    #     return HttpResponse("Hello")
    #
    # def delete(self, request, *args, **kwargs):
    #     return HttpResponse("Hello")
