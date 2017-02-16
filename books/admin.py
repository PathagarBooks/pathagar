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

from books.models import Book, Language, Status, TagGroup
from django.contrib import admin


class BookAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['book_file']}),
        ('Basic Information', {'fields': ['a_title', 'a_author', 'a_status', 'tags']}),
        ('Extended information', {'fields': ['a_summary', 'a_category', 'a_rights', 'dc_language', 'dc_publisher', 'dc_issued', 'dc_identifier', 'cover_img'], 'classes': ['collapse']}),
    ]


class LanguageAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields': ['label']})]


class TagGroupAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Book, BookAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(Status)
admin.site.register(TagGroup, TagGroupAdmin)
