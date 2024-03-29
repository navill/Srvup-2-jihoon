from django.contrib import admin

# Register your models here.
from courses.forms import LectureAdminForm
from courses.models import Course, Lecture, MyCourses

admin.site.register(MyCourses)


class LectureInline(admin.TabularInline):
    model = Lecture
    prepopulated_fields = {'slug': ('title',)}
    form = LectureAdminForm
    extra = 1


class CourseAdmin(admin.ModelAdmin):
    inlines = [LectureInline]
    list_filter = ['updated', 'timestamp']  # admin 페이지 필터에 사용될 필드 지정
    list_display = ['title', 'updated', 'timestamp']  # 화면에 보여질 필드의 컬럼
    # 읽기 전용 필드(short_title과 같이 메서드 네임도 등록 가능)
    readonly_fields = ['updated', 'timestamp', 'short_title']
    search_fields = ['title', 'embed_code']  # 검색에 사용될 필드의 컬럼
    # list_editable = ['category']

    class Meta:
        model = Course

    def short_title(self, obj):
        # 문자열에서 앞 세개만 화면에 표시하기 위한 메서드
        return obj.title[:3]


admin.site.register(Course, CourseAdmin)
