from django.shortcuts import render
from django.views.generic import *

# Create your views here.
from categories.models import Category


class CategoryListView(ListView):
    queryset = Category.objects.all().order_by('title')


class CategoryDetailView(DetailView):
    queryset = Category.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = context['object']
        user = self.request.user
        qs1 = obj.primary_category.all().owned(user)
        context['featured_courses'] = qs1
        qs2 = obj.secondary_category.all().owned(user)

        context['courses'] = (qs1 | qs2).distinct()
        return context
