from django.conf import settings
from django.db import models

# Create your models here.
from courses.models import Course


class CourseEventView(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    views = models.IntegerField(default=0)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.views)