# See http://djangosnippets.org/snippets/1580/
from django.forms import FileInput
from django.utils.safestring import mark_safe


class ThumbnailImageWidget(FileInput):
    """
    A ImageField Widget that displays a 30px thumbnail on the change form.
    """

    def __init__(self, attrs={}):
        super(ThumbnailImageWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        output = []
        if value and hasattr(value.instance, "image_50"):
            output.append(('<a target="_blank" href="%s">'
                           '<img src="%s"/></a> '
                           % (value.url, value.instance.image_50.url)))
        output.append(super(ThumbnailImageWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))
