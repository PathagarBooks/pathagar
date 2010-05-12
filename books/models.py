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

import datetime
from uuidfield import UUIDField
from langlist import langs as LANG_CHOICES

class Book(models.Model):
    file = models.FileField(blank=False, upload_to='books')
    a_id = UUIDField('atom:id')
    a_title = models.CharField('atom:title', max_length=200, blank=False)
    a_author = models.CharField('atom:author', max_length=200, blank=False)
    a_updated = models.DateTimeField('atom:updated', default=datetime.datetime.now())
    a_summary = models.TextField('atom:summary', blank=True)
    a_category = models.CharField('atom:category', max_length=200, blank=True)
    a_rights = models.CharField('atom:rights', max_length=200, blank=True)
    dc_language = models.CharField('dc:language', max_length=10, blank=True, choices=LANG_CHOICES)
    dc_publisher = models.CharField('dc:publisher', max_length=200, blank=True)
    dc_issued = models.CharField('dc:issued', max_length=100, blank=True)
    dc_identifier = models.CharField('dc:identifier', max_length=50, \
        help_text='Use ISBN for this', blank=True)

    def __unicode__(self):
        return self.a_title

