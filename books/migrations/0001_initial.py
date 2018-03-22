# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import books.uuidfield
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


def status_insert_status(apps, schema_editor):
    Status = apps.get_model("books", "Status")
    db_alias = schema_editor.connection.alias
    Status.objects.using(db_alias).bulk_create([
        Status(pk=1, status="Published"),
        Status(pk=2, status="Draft"),
    ])


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('a_author', models.CharField(max_length=200, unique=True, verbose_name='atom:author')),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_file', models.FileField(upload_to='books')),
                ('file_sha256sum', models.CharField(max_length=64, unique=True)),
                ('mimetype', models.CharField(max_length=200, null=True)),
                ('time_added', models.DateTimeField(auto_now_add=True)),
                ('downloads', models.IntegerField(default=0)),
                ('a_id', books.uuidfield.UUIDField(blank=True, editable=False, max_length=36, verbose_name='atom:id')),
                ('a_title', models.CharField(max_length=200, verbose_name='atom:title')),
                ('a_updated', models.DateTimeField(auto_now=True, verbose_name='atom:updated')),
                ('a_summary', models.TextField(blank=True, verbose_name='atom:summary')),
                ('a_category', models.CharField(blank=True, max_length=200, verbose_name='atom:category')),
                ('a_rights', models.CharField(blank=True, max_length=200, verbose_name='atom:rights')),
                ('dc_publisher', models.CharField(blank=True, max_length=200, verbose_name='dc:publisher')),
                ('dc_issued', models.CharField(blank=True, max_length=100, verbose_name='dc:issued')),
                ('dc_identifier', models.CharField(blank=True, help_text='Use ISBN for this', max_length=50, verbose_name='dc:identifier')),
                ('cover_img', models.FileField(blank=True, upload_to='covers')),
                ('a_author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.Author')),
            ],
            options={
                'ordering': ('-time_added',),
                'get_latest_by': 'time_added',
            },
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=50, unique=True, verbose_name='language name')),
                ('code', models.CharField(blank=True, max_length=4)),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=200, blank=False)),
            ],
            options={
                'verbose_name_plural': 'Status',
            },
        ),
        migrations.RunPython(status_insert_status),
        migrations.CreateModel(
            name='TagGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField(max_length=200)),
            ],
            options={
                'verbose_name': 'Tag group',
                'verbose_name_plural': 'Tag groups',
            },
        ),
        migrations.AddField(
            model_name='book',
            name='a_status',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='books.Status'),
        ),
        migrations.AddField(
            model_name='book',
            name='dc_language',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='books.Language'),
        ),
        migrations.AddField(
            model_name='book',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
