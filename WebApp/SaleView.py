from django.contrib.auth import login
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context_processors import csrf

from WebApp.models import Customer, SalesRepresentative, Item, SaleMemo, PurchaseMemo, Supplier


def salePageLoad(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')

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
            return render_to_response('rpt_invoice.html', c)

    print(request)
    c = {'CUSTOMER':Customer.objects.all(), "SR":SalesRepresentative.objects.all(), "ITEM":Item.objects.all()}
    c.update(csrf(request))
    return render_to_response('sale_add.html', c)


def purchasePageLoad(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')
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
            return render_to_response('rpt_invoice_purchase.html', c)

    print(request)
    c = {'CUSTOMER':Supplier.objects.all(), "SR":SalesRepresentative.objects.all(), "ITEM":Item.objects.all()}
    c.update(csrf(request))
    return render_to_response('purchase_add.html', c)


def showSrPage(request):
    c={}

    if request.POST.get('addButton'):
        srName = request.POST.get('srName', '')
        srMobileNo = request.POST.get('srMobileNo', '')
        srAddress = request.POST.get('srAddress','')


        sr = SalesRepresentative(name=srName, mobileNo=srMobileNo, address=srAddress)
        sr.save()

    elif request.POST.get('searchButton'):

        srName = request.POST.get('srNameSearch', '')
        srMobileNo = request.POST.get('srMobileNoSearch', '')
        filteredSr = None
        if srName is not '' and srMobileNo is not '':
            filteredSr = SalesRepresentative.objects.filter(Q(name__icontains=srName) | Q(mobileNo__icontains=srMobileNo))
        elif srMobileNo is not '':
            filteredSr = SalesRepresentative.objects.filter(Q(mobileNo__icontains=srMobileNo))
        elif srName is not '':
            filteredSr = SalesRepresentative.objects.filter(Q(name__icontains=srName))

        c = { 'FILTERED_SR': filteredSr}
        c.update(csrf(request))
        return render_to_response('sr_add.html', c)

    c.update(csrf(request))
    return render_to_response('sr_add.html', c)

