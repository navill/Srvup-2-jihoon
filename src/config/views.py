from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import View


def home(request):
    return HttpResponse('Hello')


class HomeView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'name': 'navill',
        }
        return render(request, 'home.html', context=context)

    def post(self, request, *args, **kwargs):
        return HttpResponse("Hello")

    def put(self, request, *args, **kwargs):
        return HttpResponse("Hello")

    def delete(self, request, *args, **kwargs):
        return HttpResponse("Hello")
