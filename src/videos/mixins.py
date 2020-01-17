from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.utils.decorators import method_decorator


class MemberRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user.is_staff:
            return super().dispatch(request, *args, **kwargs)
        try:
            if obj.free:
                return super(MemberRequiredMixin, self).dispatch(request, *args, **kwargs)
        except:
            pass
        return HttpResponse('무료로 제공되는 동영상이 아닙니다.')


# create, update, delete -> video는 관리자가 생성, 수정, 삭제
class StaffMemberRequiredMixin(object):
    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
