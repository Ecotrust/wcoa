"""Richtext hooks."""
import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from wagtail.admin.rich_text.converters.html_to_contentstate import (
    InlineStyleElementHandler
)
from wagtail import hooks

@hooks.register("register_rich_text_features")
def register_heading_styling(features):
    """Add a heading style to the richtext editor and page."""

    feature_name = "h1"
    type_ = "HEADING"
    tag = "h1"

    control = {
        "type": type_,
        "label": "h1",
        "description": "h1"
    }

    features.register_editor_plugin(
        "draftail", feature_name, draftail_features.InlineStyleFeature(control)
    )

    db_conversion = {
        "from_database_format": {tag: InlineStyleElementHandler(type_)},
        "to_database_format": {"style_map": {type_: {"element": tag}}}
    }

    features.register_converter_rule("contentstate", feature_name, db_conversion)

    # This will register this feature with all richtext editors by default
    features.default_features.append(feature_name)


@hooks.register("register_rich_text_features")
def register_centertext_feature(features):
    """Add centered text option to richtext editor"""

    feature_name = "center"
    type_ = "CENTERTEXT"
    tag = "div"

    control = {
        "type": type_,
        "icon": [["M 0,100 1024,100"], ["M 0,500 1024,500"], ["M 0,900 1024,900"]],
        "description": "Center Text",
        "style": {
            "display": "block",
            "text-align": "center",
        },
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
