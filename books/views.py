from django.http import HttpResponse
from opds import get_catalog

def catalogs(request):
    return HttpResponse(get_catalog(request), mimetype='application/atom+xml')
