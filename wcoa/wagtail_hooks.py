from django.urls import reverse_lazy
from django.utils.html import escape, format_html_join
from django.templatetags.static import static
from wagtail import hooks
from wagtail.admin.rich_text.converters.html_to_contentstate import InlineStyleElementHandler, LinkElementHandler
from wagtail.admin.rich_text.editors.draftail.features import Feature, InlineStyleFeature, EntityFeature
from wagtail.rich_text import LinkHandler, features


@hooks.register("register_rich_text_features")
def register_centertext_feature(features):
    """Add centered text option to richtext editor"""

    feature_name = "centertext"
    type_ = "CENTERTEXT"
    tag = "div"

    # Configure how Draftail handles the feature in its toolbar.
    control = {
        "type": type_,
        # icon is a list of SVG paths for a center align custom icon
        "icon": ["M256 800C256 782.327 270.327 768 288 768H736C753.673 768 768 782.327 768 800C768 817.673 753.673 832 736 832H288C270.327 832 256 817.673 256 800Z", "M128 608C128 590.327 142.327 576 160 576H864C881.673 576 896 590.327 896 608C896 625.673 881.673 640 864 640H160C142.327 640 128 625.673 128 608Z", "M256 416C256 398.327 270.327 384 288 384H736C753.673 384 768 398.327 768 416C768 433.673 753.673 448 736 448H288C270.327 448 256 433.673 256 416Z","M128 224C128 206.327 142.327 192 160 192H864C881.673 192 896 206.327 896 224C896 241.673 881.673 256 864 256H160C142.327 256 128 241.673 128 224Z"],
        "style": {"display": "block", "textAlign": "center"},
    }

    # Call register_editor_plugin to register the configuration for Draftail.
    features.register_editor_plugin(
        "draftail", feature_name, InlineStyleFeature(control)
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

### DLP WORK Prior to 09.09.2024 ###

# from wagtail.rich_text import LinkHandler

# class CustomLinkHandler(LinkHandler):
#     identifier = 'external'

#     @classmethod
#     def get_model(cls):
#         return None

#     @classmethod
#     def get_template(cls):
#         return 'wcoa/blocks/link_with_target.html'

#     @classmethod
#     def expand_db_attributes(cls, attrs):
#         href = attrs["href"]
#         target_blank = attrs.get("target", "_self")
#         if target_blank == "_blank":
#             target_attr = ' target="_blank"'
#         else:
#             target_attr = ''
#         return f'<a href="{href}"{target_attr}>{attrs.get("link_text", href)}</a>'


# @hooks.register('register_rich_text_features')
# def register_external_link(features):
#     feature_name = 'external'
#     type_ = 'LINK'
#     control = {
#         'type': type_,
#         'label': 'Link',
#         'description': 'Link with option to open in new tab',
#     }
    
#     features.register_editor_plugin(
#         'draftail',
#         feature_name,
#         EntityFeature(control)
#     )

#     features.register_link_type(CustomLinkHandler)

# @hooks.register('insert_editor_js')
# def editor_js():
#     return '<script src="/static/wcoa/js/wagtail/custom_richtext_link.js"></script>'

### End DLP WORK Prior to 09.09.2024 ###

#############################################

### DLP and RH Pair Programming & DLP WORK After 09.09.2024 ###

# from typing import List
# from wagtail.admin.rich_text.converters.contentstate import link_entity
# from wagtail.admin.rich_text.converters.html_to_contentstate import ExternalLinkElementHandler


# class NewWindowExternalLinkHandler(LinkHandler):
#     # This specifies to do this override for newtab links only.
#     identifier = "newtab"

#     # @classmethod
#     # def get_instance(cls, attrs):
#     #     model = cls.get_model()
#     #     return model._default_manager.get(id=attrs["id"])
        
#     @classmethod
#     def expand_db_attributes(cls, attrs):
#         href = attrs["href"]
#         return '<a href="%s" target="_blank">' % escape(href)

# @hooks.register("register_rich_text_features")
# def register_newtab_link(features):
#     # features.register_link_type(NewWindowExternalLinkHandler)
#     features.register_editor_plugin(
#         "draftail",
#         "newtab",
#         draftail_features.EntityFeature(
#             {
#                 "type": "LINK",
#                 "icon": "link",
#                 "attributes": ["url", "id", "parentId"],
#                 "allowlist": {
#                     # Keep pasted links with http/https protocol, and not-pasted links (href = undefined).
#                     "href": "^(http:|https:|undefined$)",
#                 },
#                 "chooserUrls": {
#                     "newTab": reverse_lazy("wagtailadmin_choose_page_newtab_link"),
#                 },
#             },
#         ),
#     )
#     features.register_converter_rule(
#         "contentstate",
#         "newtab",
#         {
#             "from_database_format": {
#                 "a[href]": NewWindowExternalLinkHandler(),
#             },
#             "to_database_format": {"entity_decorators": {"LINK": link_entity}},
#         },
#     )

### End DLP and RH Pair Programming & DLP WORK After 09.09.2024 ###