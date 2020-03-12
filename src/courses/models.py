from django.db import models
from django.conf import settings
from django.db.models import Prefetch, Q
from django.db.models.signals import pre_save, post_save
from django.urls import reverse

from categories.models import Category
from courses.fields import PositionField
from courses.utils import create_slug, make_display_price
from videos.models import Video


# POS_CHOICES = (
#     ('main', 'Main'),
#     ('sec', 'Secondary'),
# )


class CourseQuerySet(models.QuerySet):
    def active(self):
        return self.filter(active=True)

    def lectures(self):
        # course_obj에 연결된 lecture
        return self.prefetch_related('lecture_set')

    def featured(self):
        return self.filter(Q(category__slug__iexact='featured') | Q(secondary__slug__iexact='featured'))

    # MyCourse에 연결된 Course를 가져오기위한 메서드
    def owned(self, user):
        if user.is_authenticated:
            qs = MyCourses.objects.filter(user=user)
            print('if: ', qs)
        else:
            qs = MyCourses.objects.none()
        return self.prefetch_related(
            # 'owned': MyCourses가 가리키고있는 Course에 대한 related_name
            Prefetch('owned', queryset=qs, to_attr='is_owner'))


class CourseManager(models.Manager):
    def get_queryset(self):
        return CourseQuerySet(self.model, using=self._db)

    def all(self):
        # return self.get_queryset().all().active()
        return super(CourseManager, self).all()


def handle_upload(instance, filename):
    if instance.slug:
        return f"{instance.slug}/images/{filename}"
    return f"unknown/images/{filename}"


class Course(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    slug = models.SlugField(blank=True, null=True)
    image_height_field = models.IntegerField(blank=True, null=True)
    image_width_field = models.IntegerField(blank=True, null=True)
    image = models.ImageField(upload_to=handle_upload,
                              height_field='image_height_field',
                              width_field='image_width_field',
                              blank=True, null=True)
    category = models.ForeignKey(Category, related_name='primary_category', on_delete=models.SET_NULL, null=True,
                                 blank=True)
    secondary = models.ManyToManyField(Category, related_name='secondary_category', blank=True)
    order = PositionField(collection='category')
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=100)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CourseManager()

    # class Meta:
    #     # slug+course = unique -> 두 개의 필드가 동일하지 않도록 함
    #     ordering = ['category', 'order']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('courses:detail', kwargs={'slug': self.slug})

    def get_purchase_url(self):
        return reverse('courses:purchase', kwargs={'slug': self.slug})

    # template에서 {{ item.price | intcomma }}로 사용할 수 있음
    def display_price(self):
        return make_display_price(self.price)


def post_save_course_receiver(sender, instance, created, *args, **kwargs):
    if instance.category not in instance.secondary.all():
        instance.secondary.add(instance.category)


post_save.connect(post_save_course_receiver, sender=Course)


# # 관리자의 입장에서 유저들이 등록한 courses를 나타낼 때
# ex: course1 - user1, user2, user3, ...
# class OwnedCourses(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     courses = models.ForeignKey('Course', on_delete=models.CASCADE, blank=True)
#     timestamp = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)


# 유저의 입장에서 한 명의 유저가 등록한 여러개의 courses를 나타낼 때
# ex: user1 - course1, course2, course3, ...
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
    free = models.BooleanField(default=False)
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
