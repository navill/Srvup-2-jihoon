from django import template

from videos.models import Video

register = template.Library()


@register.inclusion_tag('videos/snippets/render_video.html')
def render_video(video_obj):
    video = None
    if isinstance(video_obj, Video):
        video = video_obj.embed_code
    return {'video': video}  # -> render_video.html로 전달
