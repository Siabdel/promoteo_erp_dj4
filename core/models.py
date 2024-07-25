
import json
from datetime import datetime
from django.db import models
from django.db.models.signals import pre_delete
from django.core.exceptions import FieldDoesNotExist
from django_comments.models import Comment
from django_comments.moderation import CommentModerator, moderator, AlreadyModerated
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.dispatch import receiver

## VALIDATION RULES ##
        
def validate_json(value):
    try:
        json.loads(value)
    except:
        raise ValidationError(_('Ivalid JSON syntax'))

## MODELS ##

class CommentableModelModerator(CommentModerator):
    email_notification = False
    enable_field = 'allow_comments'

class CommentableModelBase(models.base.ModelBase):
    def __new__(cls, name, bases, attrs):
        model = super(CommentableModelBase, cls).__new__(cls, name, bases, attrs)

        try:
            moderator.register(model, CommentableModelModerator)
        except AlreadyModerated:
            pass
            
        return model


class Commentable(models.Model):
    """Mix-in for all commentable resources.
    """
    __metaclass__ = CommentableModelBase

    allow_comments = models.BooleanField(default=True, verbose_name=_('allow comments'))

    class Meta:
        abstract=True

@receiver(pre_delete)
def delete_comments(sender, **kwargs):
    """Deletes all associated comments.
    """
    comments = Comment.objects.for_model(sender)
    for c in comments:
        c.delete()
