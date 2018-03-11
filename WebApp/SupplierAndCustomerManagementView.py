from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context_processors import csrf

from WebApp.models import SalesRepresentative, Customer, Supplier

def showScPage(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')

    c = {}
    c.update(csrf(request))
    return render_to_response('sc.html', c)

def showScAddPage(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')

    if request.POST.get('addButton'):
        srId = request.POST.get('scSR', '')
        print(srId)

        name = request.POST.get('scName', '')
        address = request.POST.get('scAddress', '')
        mobileNo = request.POST.get('scMobileNo', '')
        sr = SalesRepresentative.objects.get(id=int(srId))
        type = request.POST.get('scType', '')

        if type == 'customer':
            scObject = Customer(name=name, address=address, mobileNo=mobileNo, salesRepresentative=sr)
            scObject.save()

        elif type == 'supplier':
            scObject = Supplier(name=name, address=address, mobileNo=mobileNo, salesRepresentative=sr)
            scObject.save()

    if request.POST.get('searchButton'):
        name = request.POST.get('scNameSearch', '')
        mobileNo = request.POST.get('scMobileNoSearch', '')
        filteredC= None
        filteredS =None
        if name is not '' and mobileNo is not '' :
            filteredC = Customer.objects.filter(Q(name__icontains=name) | Q(mobileNo__icontains=mobileNo))
            filteredS = Supplier.objects.filter(Q(name__icontains=name) | Q(mobileNo__icontains=mobileNo))
        elif mobileNo is not '':
            filteredC = Customer.objects.filter(Q(mobileNo__icontains=mobileNo))
            filteredS = Supplier.objects.filter(Q(mobileNo__icontains=mobileNo))
        elif name is not '':
            filteredC = Customer.objects.filter(Q(name__icontains=name))
            filteredS = Supplier.objects.filter(Q(name__icontains=name))
        else:
            filteredC = Customer.objects.all()
            filteredS = Supplier.objects.all()

        c = {'SR': SalesRepresentative.objects.all(), 'FILTERED_C': filteredC, 'FILTERED_S': filteredS}
        c.update(csrf(request))
        return render_to_response('sc_add.html', c)

    c={'SR': SalesRepresentative.objects.all()}
    c.update(csrf(request))
    return render_to_response('sc_add.html', c)

def showScDeletePage(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')

    if request.POST.get('deleteButton'):
        id = request.POST.get('scID', '')
        type = request.POST.get('scType','')
        if type == 'supplier':
            Supplier.objects.filter(id=int(id)).delete()
        if type == 'customer':
            Customer.objects.filter(id=int(id)).delete()


    if request.POST.get('searchButton'):
        name = request.POST.get('scNameSearch', '')
        mobileNo = request.POST.get('scMobileNoSearch', '')
        filteredC= None
        filteredS =None
        if name is not '' and mobileNo is not '' :
            filteredC = Customer.objects.filter(Q(name__icontains=name) | Q(mobileNo__icontains=mobileNo))
            filteredS = Supplier.objects.filter(Q(name__icontains=name) | Q(mobileNo__icontains=mobileNo))
        elif mobileNo is not '':
            filteredC = Customer.objects.filter(Q(mobileNo__icontains=mobileNo))
            filteredS = Supplier.objects.filter(Q(mobileNo__icontains=mobileNo))
        elif name is not '':
            filteredC = Customer.objects.filter(Q(name__icontains=name))
            filteredS = Supplier.objects.filter(Q(name__icontains=name))
        else:
            filteredC = Customer.objects.all()
            filteredS = Supplier.objects.all()


        c = {'SR': SalesRepresentative.objects.all(), 'FILTERED_C': filteredC, 'FILTERED_S': filteredS}
        c.update(csrf(request))
        return render_to_response('sc_delete.html', c)

    c={'SR': SalesRepresentative.objects.all()}
    c.update(csrf(request))
    return render_to_response('sc_delete.html', c)

def showScEditPage(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')

    if request.POST.get('saveButton'):
        id = request.POST.get('scID', '')
        type = request.POST.get('scType','')
        if type == 'supplier':
            object = Supplier.objects.filter(id=int(id)).get()
            srId = request.POST.get('scSR', '')
            print(srId)

            name = request.POST.get('scName', '')
            object.name = name
            address = request.POST.get('scAddress', '')
            object.address=address
            mobileNo = request.POST.get('scMobileNo', '')
            object.mobileNo = mobileNo
            if int(srId) is not -1:
                sr = SalesRepresentative.objects.get(id=int(srId))
                object.salesRepresentative = sr
            object.save()

        if type == 'customer':
            object = Customer.objects.filter(id=int(id)).get()
            srId = request.POST.get('scSR', '')
            print(srId)

            name = request.POST.get('scName', '')
            object.name = name
            address = request.POST.get('scAddress', '')
            object.address = address
            mobileNo = request.POST.get('scMobileNo', '')
            object.mobileNo = mobileNo
            if int(srId) is not -1:
                sr = SalesRepresentative.objects.get(id=int(srId))
                object.salesRepresentative=sr
            object.save()

    if request.POST.get('searchButton'):
        name = request.POST.get('scNameSearch', '')
        mobileNo = request.POST.get('scMobileNoSearch', '')
        filteredC= None
        filteredS =None
        if name is not '' and mobileNo is not '' :
            filteredC = Customer.objects.filter(Q(name__icontains=name) | Q(mobileNo__icontains=mobileNo))
            filteredS = Supplier.objects.filter(Q(name__icontains=name) | Q(mobileNo__icontains=mobileNo))
        elif mobileNo is not '':
            filteredC = Customer.objects.filter(Q(mobileNo__icontains=mobileNo))
            filteredS = Supplier.objects.filter(Q(mobileNo__icontains=mobileNo))
        elif name is not '':
            filteredC = Customer.objects.filter(Q(name__icontains=name))
            filteredS = Supplier.objects.filter(Q(name__icontains=name))
        else:
            filteredC = Customer.objects.all()
            filteredS = Supplier.objects.all()

        c = {'SR': SalesRepresentative.objects.all(), 'FILTERED_C': filteredC, 'FILTERED_S': filteredS}
        c.update(csrf(request))
        return render_to_response('sc_edit.html', c)

    c={'SR': SalesRepresentative.objects.all()}
    c.update(csrf(request))
    return render_to_response('sc_edit.html', c)
