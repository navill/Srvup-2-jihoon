from django.db import models
from django.conf import settings
from django.db.models import Prefetch
from django.db.models.signals import pre_save, post_save
from django.urls import reverse

from courses.fields import PositionField
from courses.utils import create_slug, make_display_price
from videos.models import Video

POS_CHOICES = (
    ('main', 'Main'),
    ('sec', 'Secondary'),
)


class CourseQuerySet(models.QuerySet):
    def active(self):
        print('active')
        return self.filter(active=True)

    def owned(self, user):
        return self.prefetch_related(
            # owned: MyCourses가 가리키고있는 Course에 대한 related_name
            Prefetch('owned', queryset=MyCourses.objects.filter(user=user), to_attr='is_owner'))


class CourseManager(models.Manager):
    def get_queryset(self):
        return CourseQuerySet(self.model, using=self._db)

    def all(self):
        # return self.get_queryset.all().active()  # -> error
        return super().all().active()


class Course(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    slug = models.SlugField(blank=True, null=True)
    category = models.CharField(max_length=120, choices=POS_CHOICES, default='main')
    order = PositionField(collection='category')
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=100)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CourseManager()

    class Meta:
        # slug+course = unique -> 두 개의 필드가 동일하지 않도록 함
        ordering = ['category', 'order']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('courses:detail', kwargs={'slug': self.slug})

    def get_purchase_url(self):
        return reverse('courses:purchase', kwargs={'slug': self.slug})

    # template에서 {{ item.price | intcomma }}로 사용할 수 있음
    def display_price(self):
        return make_display_price(self.price)


# # 관리자의 입장에서 유저들이 등록한 courses를 나타낼 때
# class OwnedCourses(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     courses = models.ForeignKey('Course', on_delete=models.CASCADE, blank=True)
#     timestamp = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)


# 유저의 입장에서 한 명의 유저가 등록한 여러개의 courses를 나타낼 때
class MyCourses(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    courses = models.ManyToManyField(Course, related_name='owned', blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.courses.all().count())

    class Meta:
        verbose_name = 'My Courses'
        verbose_name_plural = 'My Courses'


def post_save_user_create(sender, instance, created, *args, **kwargs):
    if created:
        MyCourses.objects.get_or_create(user=instance)


post_save.connect(post_save_user_create, sender=settings.AUTH_USER_MODEL)


# 
# 


class Lecture(models.Model):
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    video = models.ForeignKey(Video, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=120)
    order = PositionField(collection='course')
    slug = models.SlugField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        # slug+course = unique -> 두 개의 필드가 동일하지 않도록 함
        unique_together = ('slug', 'course'),
        ordering = ['order']

    def get_absolute_url(self):
        return reverse('courses:lecture-detail', kwargs={
            'cslug': self.course.slug,
            'lslug': self.slug,
        })


def pre_save_course_receiver(sender, instance, *args, **kwargs):
    instance.slug = create_slug(instance)


pre_save.connect(pre_save_course_receiver, sender=Course)
# pre_save.connect(pre_save_course_receiver, sender=Lecture)
