from wagtail import hooks
import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from wagtail.admin.rich_text.converters.html_to_contentstate import InlineStyleElementHandler

@hooks.register("register_rich_text_features")
def register_centertext_feature(features):
    """Add centered text option to richtext editor"""

    feature_name = "center"
    type_ = "CENTERTEXT"
    tag = "div"

    control = {
        "type": type_,
        "icon": ["M256 800C256 782.327 270.327 768 288 768H736C753.673 768 768 782.327 768 800C768 817.673 753.673 832 736 832H288C270.327 832 256 817.673 256 800Z", "M128 608C128 590.327 142.327 576 160 576H864C881.673 576 896 590.327 896 608C896 625.673 881.673 640 864 640H160C142.327 640 128 625.673 128 608Z", "M256 416C256 398.327 270.327 384 288 384H736C753.673 384 768 398.327 768 416C768 433.673 753.673 448 736 448H288C270.327 448 256 433.673 256 416Z","M128 224C128 206.327 142.327 192 160 192H864C881.673 192 896 206.327 896 224C896 241.673 881.673 256 864 256H160C142.327 256 128 241.673 128 224Z"],
        "description": "Center Text",
        "style": {"display": "block", "text-align": "center"},
    }

    features.register_editor_plugin(
        "draftail", feature_name, draftail_features.InlineStyleFeature(control)
    )

    db_conversion = {
        "from_database_format": {tag: InlineStyleElementHandler(type_)},
        "to_database_format": {
            "style_map": {
                type_: {
                    "element": tag,
                    "props": {
                        "class": "d-block text-center"
                    }
                }
            }
        }
    }

    features.register_converter_rule("contentstate", feature_name, db_conversion)

    # This will register this feature with all richtext editors by default
    features.default_features.append(feature_name)
