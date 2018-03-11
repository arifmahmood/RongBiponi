from django.shortcuts import render_to_response
from django.template.context_processors import csrf

from WebApp.models import Item


def salesReturn(request):
    c={'ITEM': Item.objects.all()}
    c.update(csrf(request))
    return render_to_response('sales_return.html', c)