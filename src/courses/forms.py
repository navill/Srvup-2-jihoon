from django import forms

from videos.models import Video
from .models import Course, Lecture


class LectureAdminForm(forms.ModelForm):
    class Meta:
        model = Lecture
        fields = [
            'order', 'title', 'video', 'description', 'slug'
        ]

    def __init__(self, *args, **kwargs):
        super(LectureAdminForm, self).__init__(*args, **kwargs)
        obj = kwargs.get('instance')  # Lecture
        # lecture에서 video를 가지고 있지 않은(null) Video 객체를 filtering
        qs = Video.objects.filter(lecture__isnull=True)  # video0, ...
        if obj:
            if obj.video:
                this_ = Video.objects.filter(pk=obj.video.pk)
                qs = (qs | this_)
            self.fields['video'].queryset = qs
        else:
            self.fields['video'].queryset = qs


class CourseForm(forms.ModelForm):
    # number = forms.IntegerField()
    class Meta:
        model = Course
        fields = [
            'title',
            'description',
            'slug',
            'price'
        ]

    # 사용자가 form에서 직접 slug를 입력할 경우 validation이 필요하다.
    # db에 저장하기 위함이 아닌 page 단계에서의 유효성 검사
    def clean_slug(self):  # clean_<field_name> -> field에 대한 validation
        slug = self.cleaned_data.get('slug')
        qs = Course.objects.filter(slug=slug)
        # if qs.exists():  # -> course를 업데이트할 때 마다 새로운 slug로 변경해야한다.
        if qs.count() > 1:
            raise forms.ValidationError('동일한 slug가 존재합니다.')
        return slug
