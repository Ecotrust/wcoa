# image_formats.py
from wagtail.images.formats import Format, register_image_format

register_image_format(
    Format(
        "square-286.5",
        "Square 286.5",
        "richtext-image square squre286.5",
        "fill-286.5x286.5",
    )
)

register_image_format(
    Format(
        "square-382", 
        "Square 382", 
        "richtext-image square square382", 
        "fill-382x382"
    )
)

register_image_format(
    Format(
        "square-573", 
        "Square 573", 
        "richtext-image square square573", 
        "fill-573x573"
    )
)

register_image_format(
    Format(
        "max-573x573", 
        "Max 573x573", 
        "richtext-image max-573x573", 
        "max-573x573"
    )
)

register_image_format(
    Format(
        "max-1146x1146",
        "Max 1146x1146",
        "richtext-image max-1146x1146",
        "max-1146x1146",
    )
)

register_image_format(
    Format(
        "original", 
        "Original", 
        "richtext-image original", 
        "original"
    )
)
