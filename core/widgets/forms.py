from datetime import time, datetime
from time import strptime, strftime
import json
from django import forms
from django.forms.utils import flatatt
from django.utils.encoding import force_str
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string
from django.db import models
from core.authorize.cache import LoggedInUserCache
from django.urls import reverse
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from .models import WidgetTemplate, Widget
from .loading import registry
from core.forms.widgets import JsonPairWidget


class DateWidget(forms.DateInput):
    """A more-friendly date widget with a pop-up calendar."""

    class Media:
        css = {
            "screen": ("css/blitzer/jquery-ui.custom.css",)
        }
        js = (
            "js/jquery.min.js",
            "js/jquery-ui.custom.min.js",
            "js/splitdatetime.js",
        )

    def __init__(self, attrs=None):
        self.date_class = 'datepicker'
        if not attrs:
            attrs = {}
        if 'date_class' in attrs:
            self.date_class = attrs.pop('date_class')
        if 'class' not in attrs:
            attrs['class'] = 'date'
        super(DateWidget, self).__init__(attrs=attrs)

    def render(self, name, value, attrs=None):
        return '%s' % (self.date_class, super(DateWidget, self).render(name, value, attrs))

class TimeWidget(forms.MultiWidget):
    """A more-friendly time widget."""

    def __init__(self, attrs=None, only_quarters=False):
        if not attrs:
            attrs = {}
        if 'class' not in attrs:
            attrs['class'] = 'time'
        self.time_class = attrs.pop('time_class', 'timepicker')
        minutes = range(0, 60)
        if only_quarters:
            minutes = (0, 15, 30, 45)
        widgets = (
            forms.Select(attrs=attrs, choices=[(i+1, "%02d" % (i+1)) for i in range(0, 12)]),
            forms.Select(attrs=attrs, choices=[(i, "%02d" % i) for i in minutes]),
            forms.Select(attrs=attrs, choices=[('AM', _('AM')),('PM', _('PM'))])
        )
        super(TimeWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        # Convert string to time.
        if isinstance(value, str):
            try:
                value = datetime.strptime(value, "%I:%M %p").time()
            except:
                value = datetime.strptime(value, "%I:%M:%S").time()
        # Convert time to tuple.
        if isinstance(value, time):
            hour = int(value.strftime("%I"))
            minute = int(value.strftime("%M"))
            meridian = value.strftime("%p")
            return (hour, minute, meridian)
        return (None, None, None)

    def value_from_datadict(self, data, files, name):
        value = super(TimeWidget, self).value_from_datadict(data, files, name)
        t = strptime("%02d:%02d %s" % (int(value[0]), int(value[1]), value[2]), "%I:%M %p")
        return strftime("%H:%M:%S", t)

    def format_output(self, rendered_widgets):
        return '%s%s%s' % (self.time_class, rendered_widgets[0], rendered_widgets[1], rendered_widgets[2])

class DateTimeWidget(forms.SplitDateTimeWidget):
    """A more-friendly date/time widget."""

    def __init__(self, attrs=None, date_format=None, time_format=None, only_quarters=False):
        super(DateTimeWidget, self).__init__(attrs, date_format, time_format)
        self.widgets = (
            DateWidget(attrs=attrs),
            TimeWidget(attrs=attrs, only_quarters=only_quarters),
        )

    def decompress(self, value):
        if value:
            d = strftime("%Y-%m-%d", value.timetuple())
            t = strftime("%I:%M %p", value.timetuple())
            return (d, t)
        else:
            return (None, None)

    def format_output(self, rendered_widgets):
        return '%s%s' % (rendered_widgets[0], rendered_widgets[1])

class AddLinkMixin(object):
    class Media:
        css = {
            "screen": ("css/blitzer/jquery-ui.custom.css",)
        }
        js = (
            "js/jquery.min.js",
            "js/jquery-ui.custom.min.js",
            "js/addlink.js",
        )

    def _add_link_decorator(self, render_func):
        def _wrapped_render(name, *args, **kwargs):
            output = render_func(name, *args, **kwargs)
            user = LoggedInUserCache().current_user
            if self.add_url and (not self.with_perms or user.has_perms(self.with_perms)):
                tokens = {
                    'name': name,
                    'add_url': self.add_url,
                    'label': _('Add'),
                }
                output += '%(label)s\n' % tokens
            return mark_safe('\n%(output)s\n\n' % {'name': name, 'output': output})
        return _wrapped_render

class SelectAndAddWidget(forms.Select, AddLinkMixin):
    """A select widget with an optional "add" link."""

    def __init__(self, *args, **kwargs):
        self.add_url = kwargs.pop('add_url', None)
        self.with_perms = kwargs.pop('with_perms', [])
        super(SelectAndAddWidget, self).__init__(*args, **kwargs)
        self.render = self._add_link_decorator(self.render)

class SelectMultipleAndAddWidget(forms.SelectMultiple, AddLinkMixin):
    """A multiple-select widget with an optional "add" link."""

    def __init__(self, *args, **kwargs):
        self.add_url = kwargs.pop('add_url', None)
        self.with_perms = kwargs.pop('with_perms', [])
        super(SelectMultipleAndAddWidget, self).__init__(*args, **kwargs)
        self.render = self._add_link_decorator(self.render)

class JsonPairWidget(forms.Widget):
    """A widget that displays a list of text key/value pairs."""

    def __init__(self, *args, **kwargs):
        key_attrs = {}
        val_attrs = {}
        if "key_attrs" in kwargs:
            key_attrs = kwargs.pop("key_attrs")
        if "val_attrs" in kwargs:
            val_attrs = kwargs.pop("val_attrs")
        if "class" not in key_attrs:
            key_attrs['class'] = ''
        if "class" not in val_attrs:
            val_attrs['class'] = ''
        key_attrs['class'] = ' '.join(['json-key', key_attrs['class']])
        val_attrs['class'] = ' '.join(['json-val', val_attrs['class']])
        self.attrs = {'key_attrs': key_attrs, 'val_attrs': val_attrs}
        super(JsonPairWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        try:
            data = json.loads(force_str(value))
        except:
            data = {}
        output = ''
        for k, v in data.items():
            output += self.render_pair(k, v, name)
        output += self.render_pair('', '', name)
        return mark_safe(output)

    def render_pair(self, key, value, name):
        ctx = {
            'key': key,
            'value': value,
            'fieldname': name,
            'key_attrs': flatatt(self.attrs['key_attrs']),
            'val_attrs': flatatt(self.attrs['val_attrs'])
        }
        return ' ' % ctx

    def value_from_datadict(self, data, files, name):
        jsontext = ""
        if f'json_key[{name}]' in data and f'json_value[{name}]' in data:
            keys = data.getlist(f"json_key[{name}]")
            values = data.getlist(f"json_value[{name}]")
            data_dict = {}
            for key, value in zip(keys, values):
                if len(key) > 0:
                    data_dict[key] = value
            jsontext = json.dumps(data_dict)
        return jsontext

class CKEditor(forms.Textarea):
    """A wrapper for the powerful CKEditor."""

    class Media:
        js = ('js/ckeditor/ckeditor.js',)

    def render(self, name, value, attrs={}):
        rendered = super(CKEditor, self).render(name, value, attrs)
        tokens = {
            'name': name,
            'toolbar': attrs.get('toolbar', 'Full'),
            'height': attrs.get('height', '220'),
            'width': attrs.get('width', '665'),
        }
        rendered += mark_safe(u'''
        <script type="text/javascript">
            CKEDITOR.replace('%(name)s', {
                toolbar: '%(toolbar)s',
                height: '%(height)s',
                width: '%(width)s'
            });
        </script>
        ''' % tokens)
        return rendered



class WidgetTemplateForm(forms.ModelForm):
    """Form for widget template data."""
    
    class Meta:
        model = WidgetTemplate
        widgets = {'context': JsonPairWidget(), 'source': forms.Select()}
        fields = '__all__'  # Ensure all fields are included

    def __init__(self, *args, **kwargs):
        super(WidgetTemplateForm, self).__init__(*args, **kwargs)
        self.fields['source'].widget.choices = registry.sources
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('context'),
            Field('source'),
            Submit('submit', 'Save')
        )

class WidgetForm(forms.ModelForm):
    """Form for widget data."""
    
    class Meta:
        model = Widget
        exclude = ['region', 'slug', 'show_title', 'editable', 'sort_order']
        widgets = {'context': JsonPairWidget()}

    def __init__(self, *args, **kwargs):
        super(WidgetForm, self).__init__(*args, **kwargs)
        self.fields['template'].queryset = WidgetTemplate.objects.filter(public=True)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('template'),
            Field('context'),
            Submit('submit', 'Save')
        )
