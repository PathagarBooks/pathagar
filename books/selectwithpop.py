from django.template.loader import render_to_string
import django.forms as forms

class SelectWithPop(forms.Select):
    def render(self, name, *args, **kwargs):
        html = super(SelectWithPop, self).render(name, *args, **kwargs)
        popupplus = render_to_string("popupplus.html", {'field': name})

        return html+popupplus
