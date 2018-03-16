from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context_processors import csrf

from WebApp.models import Item, ReturnSaleMemo


def salesReturn(request):

    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')
    if request.POST.get('deleteButton'):
        memoNo = request.POST.get('memoNo', '')
        memoExist = ReturnSaleMemo.objects.filter(id=int(memoNo)).exists()
        print(memoNo)
        if memoNo is '' or not memoExist:
            c = {'ITEM': Item.objects.all()}
            c.update(csrf(request))
            return render_to_response('sales_return.html', c)

        else:
            ReturnSaleMemo.objects.filter(id=int(memoNo)).delete()

    elif request.POST.get('printButton'):
        memoNo = request.POST.get('memoNo','')
        memoExist = ReturnSaleMemo.objects.filter(id=memoNo).exists()
        print(memoNo)

        if memoNo is '' or not memoExist:
            c = {'ITEM': Item.objects.all()}
            c.update(csrf(request))
            return render_to_response('sales_return.html', c)

        else:
            saleMemoObject = ReturnSaleMemo.objects.filter(id=memoNo).get()
            c = {'OBJECT': saleMemoObject, }
            c.update(csrf(request))
            return render_to_response('rpt_invoice_return_sale.html', c)

    c={'ITEM': Item.objects.all()}
    c.update(csrf(request))
    return render_to_response('sales_return.html', c)