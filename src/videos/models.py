from django.db import models

# Create your models here.
from django.db.models.signals import pre_save, post_save
from django.urls import reverse

from courses.utils import create_slug


class Video(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(blank=True, null=True)
    embed_code = models.TextField()
    free = models.BooleanField(default=True)
    member_required = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('videos:detail', kwargs={'slug': self.slug})


def pre_save_video_receiver(sender, instance, *args, **kwargs):
    instance.slug = create_slug(instance)


pre_save.connect(pre_save_video_receiver, sender=Video)
