# image_formats.py
from wagtail.images.formats import Format, register_image_format, unregister_image_format

# DO NOT USE
# TODO: Remove format once all images are updated
register_image_format(
    Format(
        "square-286.5",
        "DO NOT USE Square 286.5",
        "richtext-image square square286.5",
        "fill-286.5x286.5",
    )
)

register_image_format(
    Format(
        "square-small",
        "Square 3/12",
        "richtext-image square-img square-small",
        "fill-288x288",
    )
)

# TODO: Remove format once all images are updated
register_image_format(
    Format(
        "square-382",
        "DO NOT USE Square 382",
        "richtext-image square square382",
        "fill-382x382",
    )
)

# unregister_image_format("square-382")

register_image_format(
    Format(
        "square-medium", 
        "Square 4/12", 
        "richtext-image square-img square-medium", 
        "fill-384x384"
    )
)

# TODO: Add Max medium image

# TODO: Remove format once all images are updated
register_image_format(
    Format(
        "square-573", 
        "DO NOT USE Square 573", 
        "richtext-image square square573", 
        "fill-573x573"
    )
)

register_image_format(
    Format(
        "square-large",
        "Square 6/12",
        "richtext-image square-img square-large",
        "fill-576x576",
    )
)

# TODO: Remove format once all images are updated
register_image_format(
    Format(
        "max-573x573", 
        "Max 573x573", 
        "richtext-image max-573x573", 
        "max-573x573"
    )
)

# TODO: Remove format once all images are updated
register_image_format(
    Format(
        "max-1146x1146",
        "DO NOT USE Max 1146x1146",
        "richtext-image max-1146x1146",
        "max-1146x1146",
    )
)

register_image_format(
    Format(
        "square-xl",
        "Square 12/12",
        "richtext-image square-img square-xl",
        "fill-1152x1152",
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
