# image_formats.py
from wagtail.images.formats import Format, register_image_format

register_image_format(
    Format("thumbnail-120", "Thumbnail 120", "richtext-image thumbnail", "max-120x120")
)

register_image_format(
    Format("square-300", "Square 300", "richtext-image square", "fill-300x300")
)

register_image_format(
    Format("square-600", "Square 600", "richtext-image square", "fill-600x600")
)

register_image_format(
    Format("max-600x600", "Max 600x600", "richtext-image max-600x600", "max-600x600")
)

register_image_format(
    Format("max-1000x1000", "Max 1000x1000", "richtext-image max-1000x1000", "max-1000x1000")
)

register_image_format(
    Format("original", "Original", "richtext-image original", "original")
)