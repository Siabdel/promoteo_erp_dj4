#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This file is part of the prometeo project.

This program is free software: you can redistribute it and/or modify it 
under the terms of the GNU Lesser General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
more details.

You should have received a copy of the GNU Lesser General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>
"""

__author__ = 'Emanuele Bertoldi <emanuele.bertoldi@gmail.com>'
__copyright__ = 'Copyright (c) 2011 Emanuele Bertoldi'
__version__ = '0.0.5'

import datetime

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.template.defaultfilters import truncatewords
from django.urls import reverse
from django.conf import settings

from .core.utils import value_to_string
from .models import Commentable

from .managers import **

class WikiPage(Commentable):
    """Wiki page model.
    """
    slug = models.SlugField(verbose_name=_('slug'))
    body = models.TextField(help_text=_('Use <a href="http://daringfireball.net/projects/markdown/syntax">MarkDown syntax</a>.'), verbose_name=_('body'))
    language = models.CharField(max_length=5, null=True, blank=True, choices=settings.LANGUAGES, default=settings.LANGUAGE_CODE, verbose_name=_('language'))
    author = models.ForeignKey('auth.User', verbose_name=_('created by'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created on'))
    categories = models.ManyToManyField('taxonomy.Category', null=True, blank=True, verbose_name=_('categories'))
    tags = models.ManyToManyField('taxonomy.Tag', null=True, blank=True, verbose_name=_('tags'))
    stream = models.OneToOneField('notifications.Stream', null=True, verbose_name=_('stream'))

    class Meta:
        ordering  = ('-created',)
        get_latest_by = 'created'
        verbose_name = _('wiki page')
        verbose_name_plural = _('wiki pages')     

    def __unicode__(self):
        return u'%s' % self.slug

    def get_absolute_url(self):
        return reverse('wikipage_detail', kwargs={'slug': self.slug})

    def get_edit_url(self):
        return reverse('wikipage_edit', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('wikipage_delete', kwargs={'slug': self.slug})

    
class WikiRevision(models.Model):
    """Revision of a wiki page.
    """
    page = models.ForeignKey(WikiPage, related_name='revisions', verbose_name=_('page'))
    slug = models.SlugField(verbose_name=_('slug'))
    body = models.TextField(verbose_name=_('body'))
    author = models.ForeignKey(User, verbose_name=_('created by'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created on'))

    objects = WikiRevisionManager()

    class Meta:
        ordering  = ('-created',)
        get_latest_by = 'created'
        verbose_name = _('wiki page revision')
        verbose_name_plural = _('wiki page revisions')     

    def __str__(self):
        return _('Rev # %(created)s') % {'created': self.created.strftime('%Y-%m-%d %H:%M:%S')}

    def get_absolute_url(self):
        return reverse('wikipage_revision_detail', kwargs={'slug': self.page.slug, 'created': self.created.strftime('%Y-%m-%d %H:%M:%S')})

    def _stream(self):
        return self.page.stream
    stream = property(_stream)

class Faq(Commentable):
    """Frequently Asked Question model.
    """
    title = models.CharField(max_length=200, unique=True, verbose_name=_('title'))
    question = models.TextField(verbose_name=_('question'))
    language = models.CharField(max_length=5, null=True, blank=True, choices=settings.LANGUAGES, default=settings.LANGUAGE_CODE, verbose_name=_('language'))
    author = models.ForeignKey('auth.User', verbose_name=_('created by'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created on'))
    categories = models.ManyToManyField('taxonomy.Category', null=True, blank=True, verbose_name=_('categories'))
    tags = models.ManyToManyField('taxonomy.Tag', null=True, blank=True, verbose_name=_('tags'))
    stream = models.OneToOneField('notifications.Stream', null=True, verbose_name=_('stream'))
    votes = generic.GenericRelation('taxonomy.Vote')

    class Meta:
        ordering  = ('-created',)
        get_latest_by = 'created'
        verbose_name = _('FAQ')
        verbose_name_plural = _('FAQs')

    def get_absolute_url(self):
        return reverse('faq_detail', kwargs={'id': self.pk})

    def get_edit_url(self):
        return reverse('faq_edit', kwargs={'id': self.pk})

    def get_delete_url(self):
        return reverse('faq_delete', kwargs={'id': self.pk})

    def __unicode__(self):
        return u'%s' % self.title

class Answer(Commentable):
    """Answer model.
    """
    question = models.ForeignKey(Faq, verbose_name=_('question'))
    answer = models.TextField(verbose_name=_('answer'))
    author = models.ForeignKey('auth.User', verbose_name=_('created by'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created on'))
    votes = generic.GenericRelation('taxonomy.Vote')

    class Meta:
        ordering  = ('created',)
        get_latest_by = 'created'
        verbose_name = _('answer')
        verbose_name_plural = _('answers')

    def __unicode__(self):
        return truncatewords(u'%s' % self.answer, 15)

class Poll(Commentable):
    """Poll model.
    """    
    title = models.CharField(unique=True, max_length=100, verbose_name=_('title'))
    description = models.TextField(blank=True, null=True, verbose_name=_('description'))
    language = models.CharField(max_length=5, null=True, blank=True, choices=settings.LANGUAGES, default=settings.LANGUAGE_CODE, verbose_name=_('language'))
    author = models.ForeignKey(User, verbose_name=_('created by'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created on'))
    due_date = models.DateTimeField(null=True, blank=True, verbose_name=_('due date'))
    categories = models.ManyToManyField('taxonomy.Category', null=True, blank=True, verbose_name=_('categories'))
    tags = models.ManyToManyField('taxonomy.Tag', null=True, blank=True, verbose_name=_('tags'))
    stream = models.OneToOneField('notifications.Stream', null=True, verbose_name=_('stream'))

    class Meta:
        ordering  = ('-created',)
        get_latest_by = 'created'
        verbose_name = _('poll')
        verbose_name_plural = _('polls')

    def __unicode__(self):
        return u'%s' % self.title

    def get_absolute_url(self):
        return reverse('poll_detail', kwargs={'id': self.pk})

    def get_edit_url(self):
        return reverse('poll_edit', kwargs={'id': self.pk})

    def get_delete_url(self):
        return reverse('poll_delete', kwargs={'id': self.pk})
    
    def _vote_count(self):
        count = 0
        for choice in self.choices.all():
            count += choice.votes.count()
        return count
    _vote_count.short_description = _('vote count')
    vote_count = property(_vote_count)
   
class Choice(models.Model):
    """Choice model.
    """    
    poll = models.ForeignKey(Poll, related_name='choices', verbose_name=_('poll'))
    description = models.CharField(max_length=255, verbose_name=_('description'))
    votes = generic.GenericRelation('taxonomy.Vote')

    class Meta:
        ordering  = ('poll', 'id',)
        verbose_name = _('choice')
        verbose_name_plural = _('choices')

    def __unicode__(self):
        return u'%s' % self.description

    def get_absolute_url(self):
        return reverse("poll_vote", kwargs={"id": self.poll.pk, "choice": self.index})

    def _stream(self):
        return self.poll.stream
    stream = property(_stream)

    def _index(self):
        for i, choice in enumerate(self.poll.choices.all()):
            if choice == self:
                return i
        return self.poll.choices.count()
    _index.short_description = _('index')
    index = property(_index)
