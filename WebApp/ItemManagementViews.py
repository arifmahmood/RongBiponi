from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context_processors import csrf


def showItemPage(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')

    c = {}
    c.update(csrf(request))
    return render_to_response('item.html', c)


def showItemAddPage(request):
    return None