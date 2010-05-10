from pathagar.books.models import Book
from django.contrib import admin

class BookAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['file']}),
        ('Basic Information', {'fields': ['a_title', 'a_author']}),
        ('Extended information', {'fields': ['a_summary', 'a_category', 'a_rights', 'dc_language', 'dc_publisher', 'dc_issued', 'dc_identifier'], 'classes': ['collapse']}),
    ]

admin.site.register(Book, BookAdmin)
