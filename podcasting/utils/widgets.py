from __future__ import unicode_literals

# See http://djangosnippets.org/snippets/1580/
from django.forms import ClearableFileInput
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string

try:
    import imagekit
    easy_thumbnails = False
    sorl = False
except:
    pass

try:
    import easy_thumbnails
    imagekit = False  # noqa
    sorl = False
except:
    pass

try:
    import sorl
    imagekit = False
    easy_thumbnails = False  # noqa
except:
    pass


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
        elif value and easy_thumbnails:
            output.append(render_to_string("podcasting/admin_thumbnail_easy-thumbnails.html", {
                "original_image": value,
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
        return mark_safe("".join(output))
