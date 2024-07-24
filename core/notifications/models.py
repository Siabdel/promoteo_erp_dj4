
import hashlib
from datetime import datetime
import json
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.validators import validate_slug

User = get_user_model()

def validate_json(value):
    try:
        json.loads(value)
    except ValueError:
        raise ValidationError(_('Invalid JSON'))

class Observable(models.Model):
    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__changes = {}
        self.__field_cache = {f.name: f for f in self._meta.fields}

    def __setattr__(self, name, value):
        if self.pk and name in self.__field_cache:
            field = self.__field_cache[name]
            label = str(field.verbose_name)
            if not hasattr(self, '_change_exclude') or name not in self._change_exclude:
                old_value = field.value_from_object(self)
                super().__setattr__(name, value)
                new_value = field.value_from_object(self)
                if new_value != old_value:
                    self.__changes[label] = (str(old_value), str(new_value))
                return
        super().__setattr__(name, value)

class Signature(models.Model):
    title = models.CharField(_('title'), max_length=100)
    slug = models.SlugField(_('slug'), max_length=100, unique=True, validators=[validate_slug])
    subscribers = models.ManyToManyField(User, through='Subscription', related_name='signatures', verbose_name=_('subscribers'))

    class Meta:
        verbose_name = _('signature')
        verbose_name_plural = _('signatures')

    def __str__(self):
        return self.title

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    signature = models.ForeignKey(Signature, on_delete=models.CASCADE)
    send_email = models.BooleanField(default=True, verbose_name=_('send email'))

    class Meta:
        verbose_name = _('subscription')
        verbose_name_plural = _('subscriptions')

class Stream(models.Model):
    slug = models.SlugField(_('slug'), max_length=100, unique=True, validators=[validate_slug])
    linked_streams = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='linked_to', verbose_name=_('linked streams'))
    followers = models.ManyToManyField(User, related_name='followed_streams', verbose_name=_('followers'))

    class Meta:
        verbose_name = _('stream')
        verbose_name_plural = _('streams')

    def __str__(self):
        return self.slug

class Activity(models.Model):
    title = models.CharField(_('title'), max_length=200)
    signature = models.CharField(_('signature'), max_length=50)
    template = models.CharField(_('template'), blank=True, null=True, max_length=200)
    context = models.JSONField(_('context'), blank=True, null=True, validators=[validate_json], help_text=_('Use the JSON syntax.'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created'))
    streams = models.ManyToManyField(Stream, related_name='activities', verbose_name=_('streams'))
    backlink = models.URLField(_('backlink'), blank=True, null=True, max_length=200)

    class Meta:
        verbose_name = _('activity')
        verbose_name_plural = _('activities')
        ordering = ('-created',)

    def __str__(self):
        try:
            return self.title % self.context
        except:
            return self.title

    def get_content(self):
        template_name = f"notifications/activities/{self.signature}.html"
        if self.template:
            template_name = self.template
        return render_to_string(template_name, self.context or {})

    def get_absolute_url(self):
        return self.backlink or ""

class Notification(models.Model):
    title = models.CharField(max_length=100, verbose_name=_('title'))
    description = models.TextField(blank=True, null=True, verbose_name=_('description'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications', verbose_name=_('user'))
    signature = models.ForeignKey(Signature, on_delete=models.CASCADE, related_name='notifications', verbose_name=_('signature'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created on'))
    read = models.DateTimeField(blank=True, null=True, verbose_name=_('read on'))
    dispatch_uid = models.CharField(max_length=32, verbose_name=_('dispatch UID'))

    class Meta:
        verbose_name = _('notification')
        verbose_name_plural = _('notifications')
        ordering = ('-created', 'id')
        get_latest_by = '-created'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('notification_detail', kwargs={'username': self.user.username, 'id': self.pk})

    def get_delete_url(self):
        return reverse('notification_delete', kwargs={'username': self.user.username, 'id': self.pk})

    def clean(self):
        if not self.user.subscription_set.filter(signature=self.signature).exists():
            raise ValidationError(_('The user is not subscribed for this kind of notification.'))
        super().clean()

    def save(self, *args, **kwargs):
        if not self.dispatch_uid:
            self.dispatch_uid = hashlib.md5(f"{self.title}{self.description}{datetime.now()}".encode()).hexdigest()
        super().save(*args, **kwargs)