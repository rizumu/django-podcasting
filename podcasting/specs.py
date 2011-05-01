from imagekit.specs import ImageSpec
from imagekit import processors


class EnchanceSmallImage(processors.Adjustment):
    contrast = 1.2
    sharpness = 1.1


class Png(processors.Format):
    format = 'PNG'
    extension = 'png'


class Resize50(processors.Resize):
    width = 50
    height = 50
    crop = True
    upscale = True


class Resize120(processors.Resize):
    width = 120
    height = 120
    crop = True
    upscale = True


class Resize144(processors.Resize):
    width = 144
    height = 144
    crop = True
    upscale = True


class Resize180(processors.Resize):
    width = 180
    height = 180
    crop = True
    upscale = True


class Resize550(processors.Resize):
    width = 550
    height = 550
    crop = True
    upscale = True


class Resize600(processors.Resize):
    width = 600
    height = 600
    crop = True
    upscale = True


class Resize1000(processors.Resize):
    width = 1000
    height = 1000
    crop = True
    upscale = True


class Podcast50(ImageSpec):
    access_as = "image_50"
    pre_cache = True
    processors = [Png, Resize50, EnchanceSmallImage]


class Podcast120(ImageSpec):
    access_as = "image_120"
    pre_cache = True
    processors = [Png, Resize120, EnchanceSmallImage]


class Podcast144(ImageSpec):
    access_as = "image_144"
    pre_cache = True
    processors = [Png, Resize144, EnchanceSmallImage]


class Podcast180(ImageSpec):
    access_as = "image_180"
    pre_cache = True
    processors = [Png, Resize180, EnchanceSmallImage]


class Podcast550(ImageSpec):
    access_as = "image_550"
    pre_cache = True
    processors = [Png, Resize550]


class Podcast600(ImageSpec):
    access_as = "image_600"
    pre_cache = True
    processors = [Png, Resize600]


class Podcast1000(ImageSpec):
    access_as = "image_1000"
    pre_cache = True
    processors = [Png, Resize1000]
