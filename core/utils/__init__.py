"""
___ utils
    compatbilite Django v4
"""
    
    
from django.db import models
from django.db.models import Q, query
from django.db.models import fields as django_fields
from collections import OrderedDict
from django.utils.encoding import force_str
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.utils.formats import localize
from django.template.defaultfilters import date, time, striptags, truncatewords
from django.conf import settings

class DependencyError(Exception):
    def __init__(self, app_name):
        self._app_name = app_name

    def __str__(self):
        return f"A dependency is not satisfied: {self._app_name}"

def check_dependency(app_name):
    if app_name not in settings.INSTALLED_APPS:
        raise DependencyError(app_name)

def clean_referer(request, default_referer='/'):
    referer = request.META.get('HTTP_REFERER', default_referer)
    return referer.replace("http://", "").replace("https://", "").replace(request.META['HTTP_HOST'], "")

def value_to_string(value):
    output = localize(value)
    if isinstance(value, (list, tuple)):
        output = ', '.join(str(v) for v in value)
    elif isinstance(value, bool):
        output = f"<span class='{'yes' if value else 'no'}'>{_('Yes') if value else _('No')}</span>"
    elif isinstance(value, float):
        output = f'{value:.2f}'
    elif isinstance(value, int):
        output = f'{value}'
    if not value and not output:
        output = f"<span class='disabled'>{_('empty')}</span>"
    return mark_safe(output)

def field_to_value(field, instance):
    value = getattr(instance, field.name)
    if field.primary_key or isinstance(field, models.SlugField):
        return f'#{value}' if value else None
    elif isinstance(field, models.PositiveIntegerField):
        return f'#{value}'
    elif isinstance(field, (models.ForeignKey, models.OneToOneField)):
        try:
            return mark_safe(f"<a href='{value.get_absolute_url()}'>{value}</a>")
        except AttributeError:
            return value
    elif isinstance(field, models.ManyToManyField):
        items = []
        for item in value.all():
            try:
                items.append(mark_safe(f"<a href='{item.get_absolute_url()}'>{item}</a>"))
            except AttributeError:
                items.append(str(item))
        return items
    elif isinstance(field, models.DateTimeField):
        return date(value, settings.DATETIME_FORMAT)
    elif isinstance(field, models.DateField):
        return date(value, settings.DATE_FORMAT)
    elif isinstance(field, models.TimeField):
        return time(value, settings.TIME_FORMAT)
    elif isinstance(field, models.URLField) and value:
        return mark_safe(f'<a href="{value}">{value}</a>')
    elif isinstance(field, models.EmailField) and value:
        return mark_safe(f'<a href="mailto:{value}">{value}</a>')
    elif field.choices:
        return getattr(instance, f'get_{field.name}_display')()
    elif isinstance(field, models.BooleanField):
        return bool(value)
    return value

def field_to_string(field, instance):
    return value_to_string(field_to_value(field, instance))

def is_visible(field_name, fields=[], exclude=[]):
    return (len(fields) == 0 or field_name in fields) and field_name not in exclude

def filter_field_value(request, field):
    name = field.name
    if f"sub_{name}" in request.POST:
        return None
    elif name in request.POST:
        return request.POST[name]
    elif 'filter_field' in request.POST and request.POST['filter_field'] == name:
        return request.POST['filter_query']
    return None
    
def get_filter_fields(request, model, fields, exclude):
    return [(f, filter_field_value(request, f)) for f in model._meta.fields if is_visible(f.name, fields, exclude)]

def filter_objects(request, model_or_queryset=None, fields=[], exclude=[]):
    matches = []
    model = None
    object_list = None
    queryset = None

    if isinstance(model_or_queryset, query.QuerySet):
        model = model_or_queryset.model
        object_list = model_or_queryset
    elif issubclass(model_or_queryset, models.Model):
        model = model_or_queryset
        object_list = model.objects.all()

    if not object_list.query.can_filter():
        pks = [instance.pk for instance in object_list]
        object_list = model.objects.filter(pk__in=pks)
    
    filter_fields = get_filter_fields(request, model, fields, exclude)
    
    if request.method == 'POST':
        queryset = []
        for f, value in filter_fields:
            if value is not None:
                if isinstance(f, django_fields.related.RelatedField):
                    pass  # Fail silently.
                else:
                    queryset.append(Q(**{f"{f.name}__startswith": value}) | Q(**{f"{f.name}__endswith": value}))

    if queryset:
        matches = object_list.filter(*queryset)
    else:
        matches = object_list

    try:
        order_by = request.GET['order_by']
        matches = matches.order_by(order_by)
    except KeyError:
        pass
        
    return [f.name for f, value in filter_fields], OrderedDict(filter_fields), matches

def assign_code(instance, queryset=None, code_field_name='code', order_field_name='created'):
    from datetime import date

    if not isinstance(queryset, query.QuerySet):
        queryset = instance.__class__.objects.all()

    if not getattr(instance, code_field_name):
        year = date.today().year
        uid = 1
        try:
            last_obj = queryset.filter(**{f'{code_field_name}__endswith': f'-{year}'}).latest(order_field_name)
            uid = int(getattr(last_obj, code_field_name).partition('-')[0]) + 1
        except queryset.model.DoesNotExist:
            pass
        setattr(instance, code_field_name, f'{uid}-{year}')
