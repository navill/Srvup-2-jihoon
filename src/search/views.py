from django.db.models import Q
from django.shortcuts import render
from django.views.generic.base import View

from courses.models import Course, Lecture
from categories.models import Category


class SearchView(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        # lectures: prefetch_related('lectures_set')
        qs = None
        c_qs = None
        l_qs = None
        if query:
            # complex lookup
            lec_lookup = Q(title__icontains=query) | Q(description__icontains=query)

            # course.title + course.category.title + course.description + course.category.description + course.lecture.title
            query_lookup = lec_lookup | \
                           Q(category__title__icontains=query) | \
                           Q(category__description__icontains=query) | \
                           Q(lecture__title__icontains=query)

            qs = Course.objects.all().lectures().filter(query_lookup).distinct()
            qs_ids = [x.id for x in qs]

            # course_queryset.ids -> qs_ids를 이용해 관련 category 검색
            cat_lookup = Q(primary_category__in=qs_ids) | Q(secondary_category__in=qs_ids)
            # prefech_related가 필요없으므로 all을 사용하지 않음 -> 단순 검색 결과
            c_qs = Category.objects.filter(cat_lookup).distinct()

            # lecture - title과 description 필터링

            l_qs = Lecture.objects.filter(lec_lookup).distinct()
        context = {'qs': qs, 'c_qs': c_qs, 'l_qs': l_qs}
        return render(request, 'search/default.html', context)
