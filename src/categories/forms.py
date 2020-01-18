from django import forms
from django.db.models import Q
from videos.models import Video
from .models import Category


class CategoryAdminForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = [
            'order', 'title', 'video', 'description', 'slug'
        ]

    def __init__(self, *args, **kwargs):
        super(CategoryAdminForm, self).__init__(*args, **kwargs)
        obj = kwargs.get('instance')  # Lecture
        # lecture에서 video를 가지고 있지 않은(null) Video 객체를 filtering
        qs = Video.objects.unused()
        if obj:
            if obj.video:
                this_ = Video.objects.filter(pk=obj.video.pk)
                qs = (qs | this_)
            self.fields['video'].queryset = qs
        else:
            self.fields['video'].queryset = qs