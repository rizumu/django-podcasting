# See http://djangosnippets.org/snippets/1580/
from django.forms import ClearableFileInput
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string

try:
    import imagekit
    sorl = False
except:
    imagekit = False
    try:
        import sorl
    except:
        sorl = False


class CustomAdminThumbnailWidget(ClearableFileInput):
    """
    A ImageField Widget that displays a 30px thumbnail on the change form.
    """
    def __init__(self, attrs={}):
        super(CustomAdminThumbnailWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        output = []

        if value and imagekit:
            thumb_sm_url = value.instance.admin_thumb_sm.url
            thumb_lg_url = value.instance.admin_thumb_lg.url
            output.append(render_to_string("podcasting/admin_thumbnail_imagekit.html", {
                "original_image_url": value.url,
                "thumb_sm_url": thumb_sm_url,
                "thumb_lg_url": thumb_lg_url,
            }))
        elif value and sorl:
            output.append(render_to_string("podcasting/admin_thumbnail_sorl.html", {
                "original_image": value,
            }))
        else:
            output.append(render_to_string("podcasting/admin_thumbnail_css.html", {
                "original_image": value,
            }))
        output.append(super(CustomAdminThumbnailWidget, self).render(name, value, attrs))
        return mark_safe(u"".join(output))
