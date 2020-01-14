from django.db import models
from django.conf import settings

# Create your models here.
from django.db.models.signals import pre_save
from django.urls import reverse
from django.utils.text import slugify

from courses.utils import create_slug


class Course(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    slug = models.SlugField(blank=True, null=True)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('courses:detail', kwargs={'slug': self.slug})


def pre_save_course_receiver(sender, instance, *args, **kwargs):
    instance.slug = create_slug(instance)


pre_save.connect(pre_save_course_receiver, sender=Course)
