from django.db import models

# Create your models here.
from django.db.models import Count, Q
from django.db.models.signals import pre_save, post_save
from django.urls import reverse

from courses.utils import create_slug


class VideoQuerySet(models.QuerySet):
    def active(self):
        return self.filter(active=True)


class VideoManager(models.Manager):
    def get_queryset(self):
        return VideoQuerySet(self.model, using=self._db)

    def unused(self):
        return self.filter(Q(lecture__isnull=True) & Q(category__isnull=True))

    def all(self):
        return super().all()


class Video(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(blank=True, null=True)
    embed_code = models.TextField()
    free = models.BooleanField(default=True)
    member_required = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = VideoManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('videos:detail', kwargs={'slug': self.slug})


def pre_save_video_receiver(sender, instance, *args, **kwargs):
    instance.slug = create_slug(instance)


pre_save.connect(pre_save_video_receiver, sender=Video)
