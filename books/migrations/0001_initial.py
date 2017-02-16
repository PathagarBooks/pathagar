# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import taggit.managers
import books.uuidfield


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('book_file', models.FileField(upload_to=b'books')),
                ('file_sha256sum', models.CharField(unique=True, max_length=64)),
                ('mimetype', models.CharField(max_length=200, null=True)),
                ('time_added', models.DateTimeField(auto_now_add=True)),
                ('downloads', models.IntegerField(default=0)),
                ('a_id', books.uuidfield.UUIDField(verbose_name=b'atom:id', max_length=36, editable=False, blank=True)),
                ('a_title', models.CharField(max_length=200, verbose_name=b'atom:title')),
                ('a_author', models.CharField(max_length=200, verbose_name=b'atom:author')),
                ('a_updated', models.DateTimeField(auto_now=True, verbose_name=b'atom:updated')),
                ('a_summary', models.TextField(verbose_name=b'atom:summary', blank=True)),
                ('a_category', models.CharField(max_length=200, verbose_name=b'atom:category', blank=True)),
                ('a_rights', models.CharField(max_length=200, verbose_name=b'atom:rights', blank=True)),
                ('dc_publisher', models.CharField(max_length=200, verbose_name=b'dc:publisher', blank=True)),
                ('dc_issued', models.CharField(max_length=100, verbose_name=b'dc:issued', blank=True)),
                ('dc_identifier', models.CharField(help_text=b'Use ISBN for this', max_length=50, verbose_name=b'dc:identifier', blank=True)),
                ('cover_img', models.FileField(upload_to=b'covers', blank=True)),
            ],
            options={
                'ordering': ('-time_added',),
                'get_latest_by': 'time_added',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(unique=True, max_length=50, verbose_name=b'language name')),
                ('code', models.CharField(max_length=4, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name_plural': 'Status',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TagGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField(max_length=200)),
            ],
            options={
                'verbose_name': 'Tag group',
                'verbose_name_plural': 'Tag groups',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='book',
            name='a_status',
            field=models.ForeignKey(default=1, to='books.Status'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='book',
            name='dc_language',
            field=models.ForeignKey(blank=True, to='books.Language', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='book',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags'),
            preserve_default=True,
        ),
    ]
