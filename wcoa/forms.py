import warnings

from django import forms
from django.core import validators
from django.forms.widgets import TextInput, CheckboxInput
from django.utils.translation import gettext_lazy as _

from wagtail.models import Locale
from wagtail.search.backends import get_search_backend
from wagtail.admin.forms.choosers import URLOrAbsolutePathField


class NewTabLinkChooserForm(forms.Form):
    url = URLOrAbsolutePathField(required=True, label=_("url"))
    link_text = forms.CharField(required=False)
    newtab = forms.BooleanField(required=False, widget=CheckboxInput, label=_("Open in new tab"),)
