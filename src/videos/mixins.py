from django.http import HttpResponse


class MemberRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.free:
            return super(MemberRequiredMixin, self).dispatch(request, *args, **kwargs)
        return HttpResponse('무료로 제공되는 동영상이 아닙니다.')

