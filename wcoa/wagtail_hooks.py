from wagtail import hooks
import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from wagtail.admin.rich_text.converters.html_to_contentstate import InlineStyleElementHandler
from wagtail.admin.rich_text.editors.draftail.features import Feature


# @hooks.register("register_rich_text_features")
# def register_lefttext_feature(features):
#     """Add left text option to richtext editor"""

#     feature_name = "lefttext"
#     type_ = "LEFTTEXT"
#     tag = "div"

#     control = {
#         "type": type_,
#         "icon": ["M128 800C128 782.327 142.327 768 160 768H608C625.673 768 640 782.327 640 800C640 817.673 625.673 832 608 832H160C142.327 832 128 817.673 128 800Z M128 608C128 590.327 142.327 576 160 576H864C881.673 576 896 590.327 896 608C896 625.673 881.673 640 864 640H160C142.327 640 128 625.673 128 608Z M128 416C128 398.327 142.327 384 160 384H608C625.673 384 640 398.327 640 416C640 433.673 625.673 448 608 448H160C142.327 448 128 433.673 128 416Z M128 224C128 206.327 142.327 192 160 192H864C881.673 192 896 206.327 896 224C896 241.673 881.673 256 864 256H160C142.327 256 128 241.673 128 224Z"],
#         "description": "Left Text",
#         "style": {"display": "block", "textAlign": "left"},
#     }

#     features.register_editor_plugin(
#         "draftail", feature_name, draftail_features.InlineStyleFeature(control)
#     )

#     db_conversion = {
#         "from_database_format": {tag: InlineStyleElementHandler(type_)},
#         "to_database_format": {
#             "style_map": {
#                 type_: {
#                     "element": tag,
#                     "props": {
#                         "class": "d-block text-left"
#                     }
#                 }
#             }
#         }
#     }

#     features.register_converter_rule("contentstate", feature_name, db_conversion)

#     # This will register this feature with all richtext editors by default
#     features.default_features.append(feature_name)

@hooks.register("register_rich_text_features")
def register_centertext_feature(features):
    """Add centered text option to richtext editor"""

    feature_name = "centertext"
    type_ = "CENTERTEXT"
    tag = "div"

    # Configure how Draftail handles the feature in its toolbar.
    control = {
        "type": type_,
        "icon": ["M256 800C256 782.327 270.327 768 288 768H736C753.673 768 768 782.327 768 800C768 817.673 753.673 832 736 832H288C270.327 832 256 817.673 256 800Z", "M128 608C128 590.327 142.327 576 160 576H864C881.673 576 896 590.327 896 608C896 625.673 881.673 640 864 640H160C142.327 640 128 625.673 128 608Z", "M256 416C256 398.327 270.327 384 288 384H736C753.673 384 768 398.327 768 416C768 433.673 753.673 448 736 448H288C270.327 448 256 433.673 256 416Z","M128 224C128 206.327 142.327 192 160 192H864C881.673 192 896 206.327 896 224C896 241.673 881.673 256 864 256H160C142.327 256 128 241.673 128 224Z"],
        "style": {"display": "block", "textAlign": "center"},
    }

    # Call register_editor_plugin to register the configuration for Draftail.
    features.register_editor_plugin(
        "draftail", feature_name, draftail_features.InlineStyleFeature(control)
    )
    
    # Configure the content transform from the DB to the editor and back.
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

    # Call register_converter_rule to register the content transformation conversion.
    features.register_converter_rule("contentstate", feature_name, db_conversion)

    # This will register this feature with all richtext editors by default
    features.default_features.append(feature_name)


# @hooks.register("register_rich_text_features")
# def register_righttext_feature(features):
#     """Add right text option to richtext editor"""

#     feature_name = "righttext"
#     type_ = "RIGHTTEXT"
#     tag = "div"

#     control = {
#         "type": type_,
#         "icon": ["M384 800C384 782.327 398.327 768 416 768H864C881.673 768 896 782.327 896 800C896 817.673 881.673 832 864 832H416C398.327 832 384 817.673 384 800Z M128 608C128 590.327 142.327 576 160 576H864C881.673 576 896 590.327 896 608C896 625.673 881.673 640 864 640H160C142.327 640 128 625.673 128 608Z M384 416C384 398.327 398.327 384 416 384H864C881.673 384 896 398.327 896 416C896 433.673 881.673 448 864 448H416C398.327 448 384 433.673 384 416Z M128 224C128 206.327 142.327 192 160 192H864C881.673 192 896 206.327 896 224C896 241.673 881.673 256 864 256H160C142.327 256 128 241.673 128 224Z"],
#         "description": "Right Text",
#         "style": {"display": "block", "textAlign": "right"},
#     }

#     features.register_editor_plugin(
#         "draftail", feature_name, draftail_features.InlineStyleFeature(control)
#     )

#     db_conversion = {
#         "from_database_format": {tag: InlineStyleElementHandler(type_)},
#         "to_database_format": {
#             "style_map": {
#                 type_: {
#                     "element": tag,
#                     "props": {
#                         "class": "d-block text-right"
#                     }
#                 }
#             }
#         }
#     }

#     features.register_converter_rule("contentstate", feature_name, db_conversion)

#     # This will register this feature with all richtext editors by default
#     features.default_features.append(feature_name)
