import json

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
