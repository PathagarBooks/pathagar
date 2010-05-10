from django.forms import ModelForm
from models import *
from langlist import langs as LANG_CHOICES


class AddBookForm(ModelForm):
    class Meta:
        model = Book
        exclude = ('a_updated',)

