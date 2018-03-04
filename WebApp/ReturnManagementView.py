from django.shortcuts import render_to_response
from django.template.context_processors import csrf


def salesReturn(request):
    c={}
    c.update(csrf(request))
    return render_to_response('sales_return.html', c)