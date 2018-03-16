from django.shortcuts import render_to_response
from django.template.context_processors import csrf

from WebApp.models import PurchaseMemo, SaleMemo, Customer, Supplier, Item


def purchase(request):
    objects= PurchaseMemo.objects.all()
    if request.POST.get('filterButton'):
        dateFrom = request.POST.get('dateFrom','')
        dateTo = request.POST.get('dateTo','')
        objects= PurchaseMemo.objects.filter(date__range=[dateFrom, dateTo])

    c = {'OBJECTS': objects, }
    c.update(csrf(request))
    return render_to_response('rpt_purchase.html', c)


def sale(request):
    objects= SaleMemo.objects.all()
    if request.POST.get('filterButton'):
        dateFrom = request.POST.get('dateFrom','')
        dateTo = request.POST.get('dateTo','')
        objects= SaleMemo.objects.filter(date__range=[dateFrom, dateTo])
    c = {'OBJECTS': objects, }
    c.update(csrf(request))
    return render_to_response('rpt_sale.html', c)


def salesReturn(request):
    objects= SaleMemo.objects.all()
    if request.POST.get('filterButton'):
        dateFrom = request.POST.get('dateFrom','')
        dateTo = request.POST.get('dateTo','')
        objects= SaleMemo.objects.filter(date__range=[dateFrom, dateTo])
    c = {'OBJECTS': objects, }
    c.update(csrf(request))
    return render_to_response('rpt_sale_return.html', c)


def listOfCustomers(request):
    objects = Customer.objects.all()
    c = {'OBJECTS': objects, }
    c.update(csrf(request))
    return render_to_response('report_list_of_customer.html', c)


def listOfSupplier(request):
    objects = Supplier.objects.all()
    c = {'OBJECTS': objects, }
    c.update(csrf(request))
    return render_to_response('report_list_of_supplier.html', c)


def listOfProduct(request):
    objects = Item.objects.all()
    c = {'OBJECTS': objects, }
    c.update(csrf(request))
    return render_to_response('report_list_of_product.html', c)