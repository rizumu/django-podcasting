from django.conf import settings  # noqa

from appconf import AppConf


class PodcastingAppConf(AppConf):
    PAGINATE_BY = 10
    FEED_ENTRIES = None
    IMG_PATH = 'img'
