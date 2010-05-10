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

