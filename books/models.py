# Copyright (C) 2010, One Laptop Per Child
# Copyright (C) 2010, Kushal Das
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

from django.db import models

from hashlib import sha256

from tagging.fields import TagField #OLD

from taggit.managers import TaggableManager #NEW

from uuidfield import UUIDField
from langlist import langs

def sha256_sum(_file): # used to generate sha256 sum of book files
    s = sha256()
    for chunk in _file:
        s.update(chunk)
    return s.hexdigest()

class Language(models.Model):
    label = models.CharField('language name', max_length=50, blank=False, unique=True)
    code = models.CharField(max_length=4, blank=True)

    def __unicode__(self):
        return self.label

    def save(self, *args, **kwargs):
        '''
        This method automatically tries to assign the right language code
        to the specified language. If a code cannot be found, it assigns
        'xx'
        '''
        code = 'xx'
        for lang in langs:
            if self.label.lower() == lang[1].lower():
                code = lang[0]
                break
        self.code = code
        super(Language, self).save(*args, **kwargs)


class TagGroup(models.Model):
    name = models.CharField(max_length=200, blank=False)
    slug = models.SlugField(max_length=200, blank=False)
    #tags = TagableManager()

    class Meta:
        verbose_name = "Tag group"
        verbose_name_plural = "Tag groups"

    def __unicode__(self):
        return self.name


class Status(models.Model):
    status = models.CharField(max_length=200, blank=False)

    class Meta:
        verbose_name_plural = "Status"

    def __unicode__(self):
        return self.status


class Book(models.Model):
    """
    This model stores the book file, and all the metadata that is
    needed to publish it in a OPDS atom feed.

    It also stores other information, like tags and downloads, so the
    book can be listed in OPDS catalogs.

    """
    book_file = models.FileField(upload_to='books')
    file_sha256sum = models.CharField(max_length=64, unique=True)
    mimetype = models.CharField(max_length=200, null=True)
    time_added = models.DateTimeField(auto_now_add=True)
    tags = TaggableManager(blank=True)
    downloads = models.IntegerField(default=0)
    a_id = UUIDField('atom:id')
    a_status = models.ForeignKey(Status, blank=False, null=False)
    a_title = models.CharField('atom:title', max_length=200)
    a_author = models.CharField('atom:author', max_length=200)
    a_updated = models.DateTimeField('atom:updated', auto_now=True)
    a_summary = models.TextField('atom:summary', blank=True)
    a_category = models.CharField('atom:category', max_length=200, blank=True)
    a_rights = models.CharField('atom:rights', max_length=200, blank=True)
    dc_language = models.ForeignKey(Language, blank=True, null=True)
    dc_publisher = models.CharField('dc:publisher', max_length=200, blank=True)
    dc_issued = models.CharField('dc:issued', max_length=100, blank=True)
    dc_identifier = models.CharField('dc:identifier', max_length=50, \
    help_text='Use ISBN for this', blank=True)
    cover_img = models.FileField(blank=True, upload_to='covers')

    def save(self, *args, **kwargs):
        if not self.file_sha256sum:
            self.file_sha256sum = sha256_sum(self.book_file)
        super(Book, self).save(*args, **kwargs)

    class Meta:
        ordering = ('-time_added',)
        get_latest_by = "time_added"

    def __unicode__(self):
        return self.a_title

    @models.permalink
    def get_absolute_url(self):
        return ('pathagar.books.views.book_detail', [self.pk])
