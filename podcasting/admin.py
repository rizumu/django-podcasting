from django.utils.translation import ugettext_lazy as _

from django.contrib import admin

try:
    from imagekit.admin import AdminThumbnail
except ImportError:
    AdminThumbnail = None

from podcasting.forms import AdminShowForm, AdminEpisodeForm
from podcasting.models import Show, Episode, Enclosure, EmbedMedia
from podcasting.utils.twitter import can_tweet


class ShowAdmin(admin.ModelAdmin):
    form = AdminShowForm

    list_display = ["title", "slug", "show_site", "published_flag"]
    list_filter = ["title", "published", "site"]
    if AdminThumbnail:
        list_display.append("admin_thumbnail")
        admin_thumbnail = AdminThumbnail(image_field="admin_thumb_sm")

    if can_tweet():
        fields.append("tweet_text")  # noqa

    def published_flag(self, obj):
        return bool(obj.published)
    published_flag.short_description = _("Published")
    published_flag.boolean = True

    def show_site(self, obj):
        return obj.site.name
    show_site.short_description = "Site"


class EpisodeAdmin(admin.ModelAdmin):
    form = AdminEpisodeForm

    list_display = ["title", "show", "slug", "episode_site", "published_flag"]
    list_filter = ["show", "published"]
    if AdminThumbnail:
        list_display.append("admin_thumbnail")
        admin_thumbnail = AdminThumbnail(image_field="admin_thumb_sm")

    if can_tweet():
        readonly_fields = ("tweet_text",)

    def published_flag(self, obj):
        return bool(obj.published)
    published_flag.short_description = _("Published")
    published_flag.boolean = True

    def episode_site(self, obj):
        return obj.show.site.name
    episode_site.short_description = "Site"

    def save_form(self, request, form, change):
        # this is done for explicitness that we want form.save to commit
        # form.save doesn't take a commit kwarg for this reason
        return form.save()


class EnclosureAdmin(admin.ModelAdmin):
    list_display = ("episode", "mime", "url")
    list_filter = ("episode",)


class EmbedMediaAdmin(admin.ModelAdmin):
    model = EmbedMedia

admin.site.register(Show, ShowAdmin)
admin.site.register(Episode, EpisodeAdmin)
admin.site.register(Enclosure, EnclosureAdmin)
admin.site.register(EmbedMedia, EmbedMediaAdmin)
