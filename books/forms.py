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

from django.forms import ModelForm, ModelChoiceField
from models import *
from langlist import langs as LANG_CHOICES
from selectwithpop import SelectWithPop

class BookForm(ModelForm):
    # dc_language = ModelChoiceField(Language.objects, widget=SelectWithPop)

    class Meta:
        model = Book
        exclude = ('mimetype', 'file_sha256sum', )

    def save(self, commit=True):
        """
        Store the MIME type of the uploaded book in the database.

        This is given by the browser in the POST request.

        """
        instance = super(BookForm, self).save(commit=False)
        book_file = self.cleaned_data['book_file']
        instance.mimetype = book_file.content_type
        if commit:
            instance.save()
        return instance

class AddLanguageForm(ModelForm):
    class Meta:
        model = Language
        exclude = ('code',)
