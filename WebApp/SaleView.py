from django.shortcuts import render_to_response
from django.template.context_processors import csrf

from WebApp.models import Customer, SalesRepresentative, Item, SaleMemo, PurchaseMemo, Supplier


def salePageLoad(request):
    if request.POST.get('deleteButton'):
        memoNo = request.POST.get('memoNo', '')
        memoExist = SaleMemo.objects.filter(id=int(memoNo)).exists()
        print(memoNo)
        if memoNo is '' or not memoExist:
            c = {'CUSTOMER': Customer.objects.all(), "SR": SalesRepresentative.objects.all(),
                 "ITEM": Item.objects.all()}
            c.update(csrf(request))
            return render_to_response('sale_add.html', c)

        else:
            SaleMemo.objects.filter(id=int(memoNo)).delete()

    elif request.POST.get('printButton'):
        memoNo = request.POST.get('memoNo','')
        memoExist = SaleMemo.objects.filter(id=int(memoNo)).exists()
        print(memoNo)

        if memoNo is '' or not memoExist:
            c = {'CUSTOMER': Customer.objects.all(), "SR": SalesRepresentative.objects.all(),
                 "ITEM": Item.objects.all()}
            c.update(csrf(request))
            return render_to_response('sale_add.html', c)

        else:
            saleMemoObject = SaleMemo.objects.filter(id=int(memoNo)).get()
            c = {'OBJECT': saleMemoObject, }
            c.update(csrf(request))
            return render_to_response('rptInvoice.html', c)

    print(request)
    c = {'CUSTOMER':Customer.objects.all(), "SR":SalesRepresentative.objects.all(), "ITEM":Item.objects.all()}
    c.update(csrf(request))
    return render_to_response('sale_add.html', c)


def purchasePageLoad(request):
    if request.POST.get('deleteButton'):
        memoNo = request.POST.get('memoNo', '')
        memoExist = PurchaseMemo.objects.filter(id=int(memoNo)).exists()
        print(memoNo)
        if memoNo is '' or not memoExist:
            c = {'CUSTOMER': Supplier.objects.all(), "SR": SalesRepresentative.objects.all(),
                 "ITEM": Item.objects.all()}
            c.update(csrf(request))
            return render_to_response('purchase_add.html', c)

        else:
            PurchaseMemo.objects.filter(id=int(memoNo)).delete()

    elif request.POST.get('printButton'):
        memoNo = request.POST.get('memoNo','')
        memoExist = PurchaseMemo.objects.filter(id=int(memoNo)).exists()
        print(memoNo)

        if memoNo is '' or not memoExist:
            c = {'CUSTOMER': Supplier.objects.all(), "SR": SalesRepresentative.objects.all(),
                 "ITEM": Item.objects.all()}
            c.update(csrf(request))
            return render_to_response('purchase_add.html', c)

        else:
            saleMemoObject = PurchaseMemo.objects.filter(id=int(memoNo)).get()
            c = {'OBJECT': saleMemoObject, }
            c.update(csrf(request))
            return render_to_response('rptInvoicePurchase.html', c)

    print(request)
    c = {'CUSTOMER':Supplier.objects.all(), "SR":SalesRepresentative.objects.all(), "ITEM":Item.objects.all()}
    c.update(csrf(request))
    return render_to_response('purchase_add.html', c)

