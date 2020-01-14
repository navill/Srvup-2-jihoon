# slug generator
import random
import string

from django.utils.text import slugify


# from .models import Course

def unique_string_generator(size=5, chars=string.ascii_lowercase + string.digits):
    return "".join(random.choice(chars) for _ in range(size))


def create_slug(instance, new_slug=None):
    if not new_slug:
        slug = slugify(instance.title)
    else:
        slug = new_slug
    Klass = instance.__class__
    qs = Klass.objects.filter(slug=slug)
    if qs.exists():
        unique_string = unique_string_generator()
        new_created_slug = slug + f'-{unique_string}'
        return create_slug(instance, new_slug=new_created_slug)
    return slug
