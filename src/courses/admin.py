from django.contrib import admin

# Register your models here.
from courses.models import Course


class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']


admin.site.register(Course, CourseAdmin)
