# See http://djangosnippets.org/snippets/1580/
from django.forms import ClearableFileInput
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string


class CustomAdminThumbnailWidget(ClearableFileInput):
    """
    A ImageField Widget that displays a 30px thumbnail on the change form.
    """
    def __init__(self, attrs={}):
        super(CustomAdminThumbnailWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        output = []
        thumb_sm_url = None
        thumb_lg_url = None

        if value and hasattr(value.instance, "admin_thumb_sm") and hasattr(value.instance, "admin_thumb_lg"):
            thumb_sm_url = value.instance.admin_thumb_sm.url
            thumb_lg_url = value.instance.admin_thumb_lg.url
        if value:
            output.append(render_to_string("podcasting/imagekit_custom_admin_thumbnail.html", {
                "original_image_url": value.url,
                "thumb_sm_url": thumb_sm_url,
                "thumb_lg_url": thumb_lg_url,
            }))
        output.append(super(CustomAdminThumbnailWidget, self).render(name, value, attrs))
        return mark_safe(u"".join(output))
