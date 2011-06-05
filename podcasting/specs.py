from imagekit.specs import ImageSpec
from imagekit import processors


class EnchanceSmallImage(processors.Adjustment):
    contrast = 1.2
    sharpness = 1.1


class Png(processors.Format):
    format = 'PNG'
    extension = 'png'

### podcasting naming
# img_admin_sm

# img_episode_sm
# img_episode_lg


# img_itunes_sm
# img_itunes_lg

class ResizeAdmin(processors.Resize):
    width = 50
    height = 50
    crop = True
    upscale = True

class ResizeEpisodeSm(processors.Resize):
    width = 120
    height = 120
    crop = True
    upscale = True

class ResizeEpisodeLg(processors.Resize):
    width = 550
    height = 550
    crop = True
    upscale = True

class ResizeItunesSm(processors.Resize):
    width = 144
    height = 144
    crop = True
    upscale = True

class ResizeItunesLg(processors.Resize):
    width = 1000
    height = 1000
    crop = True
    upscale = True


##############################################################################

class PodcastAdmin(ImageSpec):
    access_as = "img_admin_sm"
    pre_cache = True
    processors = [Png, ResizeAdmin, EnchanceSmallImage]

class PodcastEpisodeSm(ImageSpec):
    access_as = "img_episode_sm"
    pre_cache = True
    processors = [Png, ResizeEpisodeSm, EnchanceSmallImage]

class PodcastEpisodeLg(ImageSpec):
    access_as = "img_episode_lg"
    pre_cache = True
    processors = [Png, ResizeEpisodeLg]

class PodcastItunesSm(ImageSpec):
    access_as = "img_itunes_sm"
    pre_cache = True
    processors = [Png, ResizeItunesSm, EnchanceSmallImage]

class PodcastItunesLg(ImageSpec):
    access_as = "img_itunes_lg"
    pre_cache = True
    processors = [Png, ResizeItunesLg]

