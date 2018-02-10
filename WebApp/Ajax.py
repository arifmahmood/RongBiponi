from time import strftime

from django.http import JsonResponse
from django.shortcuts import render_to_response
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt

from WebApp.models import Item, Customer, Supplier, SaleMemo, SalesRepresentative, SaleItem, PurchaseMemo, PurchaseItem


@csrf_exempt
def getItem(request):
    itemId = request.POST.get('itemId','')
    itemExist = Item.objects.filter(id=int(itemId)).exists()
    print(itemId)

    if(itemExist):
        item = Item.objects.get(id=int(itemId))
        data = {
            'isFound':True,
            'itemId':item.id,
            'itemName':item.itemName,
            'itemSize':item.itemSize,
            'stockRate':item.stockRate,
            'saleRate' :item.saleRate

        }
        return JsonResponse(data)
    else:
        data = {
            'isFound': False,
            'itemName': '',
            'itemSize': '',
            'stockRate': '',
            'saleRate': ''

        }
        return JsonResponse(data)


@csrf_exempt
def getSC(request):
    scId = request.POST.get('id', '')
    scType = request.POST.get('type','')
    print(scType)
    data = {
        'isFound': False,
    }
    if scType== 'customer':
        scExist = Customer.objects.filter(id=int(scId)).exists()
        if (scExist):
            sc = Customer.objects.get(id=int(scId))
            data = {
                'isFound': True,
                'scID': sc.id,
                'scName': sc.name,
                'scAddress': sc.address,
                'scMobileNo': sc.mobileNo,
                'scSR': sc.salesRepresentative.id
            }
            print(sc.salesRepresentative.name)
        return JsonResponse(data)
    if scType== 'supplier':
        scExist = Supplier.objects.filter(id=int(scId)).exists()
        if (scExist):
            sc = Supplier.objects.get(id=int(scId))
            data = {
                'isFound': True,
                'scID': sc.id,
                'scName': sc.name,
                'scAddress': sc.address,
                'scMobileNo': sc.mobileNo,
                'scSR': sc.salesRepresentative.id
            }
            print(sc.salesRepresentative.name)
        return JsonResponse(data)
    return JsonResponse(data)

@csrf_exempt
def getCustomerAddress(request):
    customerID = request.POST.get('id', '')

    itemExist = Customer.objects.filter(id=int(customerID)).exists()
    data = {
        'isFound': False,
    }
    if itemExist:
        sc = Customer.objects.get(id=int(customerID))
        data = {
            'isFound': True,
            'customerAddress': sc.address,
            'sr': sc.salesRepresentative.name,
        }

    return JsonResponse(data);

@csrf_exempt
def addNewDetails(request):
    memoNo= request.POST.get('memoNo', '')
    dataForTable=''
    if memoNo is '':
        date = request.POST.get('date', '')
        customerID = request.POST.get('customer', '')
        customer = Customer.objects.filter(id=int(customerID)).get()
        itemID = request.POST.get('itemID', '')
        item = Item.objects.filter(id=int(itemID)).get()
        quantity = request.POST.get('itemUnit','')
        free = request.POST.get('itemFree','')
        saleRate = request.POST.get('itemRate', '')
        saleItem = SaleItem(item=item, quantity=quantity,free=free,saleRate=saleRate)
        saleItem.save()
        saleItem.total = float((int(quantity) - int(free)) * float(saleRate))
        saleItem.save()
        saleMemoObject = SaleMemo(party=customer, date=date)
        saleMemoObject.save()
        saleMemoObject.saleItem.add(saleItem)
        saleMemoObject.save()

    else:
        saleMemoObject = SaleMemo.objects.filter(id=int(memoNo)).get()
        date = request.POST.get('date', '')
        saleMemoObject.date= date

        customerID = request.POST.get('customer', '')
        customer = Customer.objects.filter(id=int(customerID)).get()
        saleMemoObject.party = customer

        itemID = request.POST.get('itemID', '')
        item = Item.objects.filter(id=int(itemID)).get()
        quantity = request.POST.get('itemUnit', '')
        free = request.POST.get('itemFree', '')
        saleRate = request.POST.get('itemRate', '')
        saleItem = SaleItem(item=item, quantity=quantity, free=free, saleRate=saleRate)
        saleItem.save()
        saleItem.total= float((int(quantity) -int(free))*float(saleRate))
        saleItem.save()
        saleMemoObject.saleItem.filter(item=saleItem.item).delete()
        saleMemoObject.saleItem.add(saleItem)
        saleMemoObject.save()

    for i in saleMemoObject.saleItem.all():
        dataForTable+='<tr><td>'+str(i.item.itemName)+'</td>'+'<td>'+str(i.item.itemSize)+'</td>'+'<td>'+str(i.quantity)+'</td>'+'<td>'+str(i.free)+'</td>'+'<td>'+str(i.saleRate)+'</td>'+'<td>'+str(i.itemTotal())+'</td>'+'</tr>'

    data = {
        'isFound': True,
        'saleMemoObjectID':saleMemoObject.id,
        'dataForTable':dataForTable,
        'tempTotal':saleMemoObject.getTotal(),
    }
    return JsonResponse(data)

@csrf_exempt
def saveMemo(request):
    memoNo = request.POST.get('memoNo', '')
    discount = request.POST.get('discount', '')
    paid = request.POST.get('paid', '')
    if memoNo is '':
        data = {
            'isSuccessful': False,

        }
    else:
        saleMemoObject = SaleMemo.objects.filter(id=int(memoNo)).get()
        saleMemoObject.discount = float(discount)
        saleMemoObject.paid = float(paid)
        saleMemoObject.save()
        data = {
            'isSuccessful': True,
            'memoNo': memoNo,
        }

    return JsonResponse(data)

@csrf_exempt
def loadMemoObject(request):
    memoNo = request.POST.get('memoNo', '')
    memoExist = SaleMemo.objects.filter(id=int(memoNo)).exists()

    if memoNo is '' or not memoExist:
        data = {
            'isSuccessful': False,


        }
    else:
        saleMemoObject = SaleMemo.objects.filter(id=int(memoNo)).get()
        dataForTable=''
        for i in saleMemoObject.saleItem.all():
            dataForTable += '<tr><td>' + str(i.item.itemName) + '</td>' + '<td>' + str(
                i.item.itemSize) + '</td>' + '<td>' + str(i.quantity) + '</td>' + '<td>' + str(
                i.free) + '</td>' + '<td>' + str(i.saleRate) + '</td>' + '<td>' + str(i.itemTotal()) + '</td>' + '</tr>'
        date= saleMemoObject.date

        data = {
            'isFound': True,
            'saleMemoObjectID': saleMemoObject.id,
            'date': date,
            'customer': saleMemoObject.party.name,
            'address': saleMemoObject.party.address,
            'sr': saleMemoObject.party.salesRepresentative.name,
            'dataForTable': dataForTable,
            'tempTotal': saleMemoObject.getTotal(),
            'discount': saleMemoObject.discount,
            'paid': saleMemoObject.paid,
        }


    return JsonResponse(data)


@csrf_exempt
def getCustomerAddressPurchase(request):
    customerID = request.POST.get('id', '')

    itemExist = Supplier.objects.filter(id=int(customerID)).exists()
    data = {
        'isFound': False,
    }
    if itemExist:
        sc = Supplier.objects.get(id=int(customerID))
        data = {
            'isFound': True,
            'customerAddress': sc.address,
            'sr': sc.salesRepresentative.name,
        }

    return JsonResponse(data);


@csrf_exempt
def saveMemoPurchase(request):
    memoNo = request.POST.get('memoNo', '')
    discount = request.POST.get('discount', '')
    paid = request.POST.get('paid', '')
    if memoNo is '':
        data = {
            'isSuccessful': False,

        }
    else:
        saleMemoObject = PurchaseMemo.objects.filter(id=int(memoNo)).get()
        saleMemoObject.discount = float(discount)
        saleMemoObject.paid = float(paid)
        saleMemoObject.save()
        data = {
            'isSuccessful': True,
            'memoNo': memoNo,
        }

    return JsonResponse(data)

@csrf_exempt
def addNewDetailsPurchase(request):
    memoNo= request.POST.get('memoNo', '')
    dataForTable=''
    if memoNo is '':
        date = request.POST.get('date', '')
        supplierID = request.POST.get('customer', '')
        supplier = Supplier.objects.filter(id=int(supplierID)).get()
        itemID = request.POST.get('itemID', '')
        item = Item.objects.filter(id=int(itemID)).get()
        quantity = request.POST.get('itemUnit','')
        free = request.POST.get('itemFree','')
        purchaseRate = request.POST.get('itemRate', '')
        purchaseItem = PurchaseItem(item=item, quantity=quantity,free=free,purchaseRate=purchaseRate)
        purchaseItem.save()
        purchaseItem.total = float((int(quantity) - int(free)) * float(purchaseRate))
        purchaseItem.save()
        purchaseMemoObject = PurchaseMemo(party=supplier, date=date)
        purchaseMemoObject.save()
        purchaseMemoObject.purchaseItem.add(purchaseItem)
        purchaseMemoObject.save()

    else:
        purchaseMemoObject = PurchaseMemo.objects.filter(id=int(memoNo)).get()
        date = request.POST.get('date', '')
        purchaseMemoObject.date= date

        customerID = request.POST.get('customer', '')
        customer = Supplier.objects.filter(id=int(customerID)).get()
        purchaseMemoObject.party = customer

        itemID = request.POST.get('itemID', '')
        item = Item.objects.filter(id=int(itemID)).get()
        quantity = request.POST.get('itemUnit', '')
        free = request.POST.get('itemFree', '')
        saleRate = request.POST.get('itemRate', '')
        saleItem = PurchaseItem(item=item, quantity=quantity, free=free, purchaseRate=saleRate)
        saleItem.save()
        saleItem.total= float((int(quantity) -int(free))*float(saleRate))
        saleItem.save()
        purchaseMemoObject.purchaseItem.filter(item=saleItem.item).delete()
        purchaseMemoObject.purchaseItem.add(saleItem)
        purchaseMemoObject.save()

    for i in purchaseMemoObject.purchaseItem.all():
        dataForTable+='<tr><td>'+str(i.item.itemName)+'</td>'+'<td>'+str(i.item.itemSize)+'</td>'+'<td>'+str(i.quantity)+'</td>'+'<td>'+str(i.free)+'</td>'+'<td>'+str(i.purchaseRate)+'</td>'+'<td>'+str(i.itemTotal())+'</td>'+'</tr>'

    data = {
        'isFound': True,
        'saleMemoObjectID':purchaseMemoObject.id,
        'dataForTable':dataForTable,
        'tempTotal':purchaseMemoObject.getTotal(),
    }
    return JsonResponse(data)

@csrf_exempt
def loadMemoObjectPurchase(request):
    memoNo = request.POST.get('memoNo', '')
    memoExist = PurchaseMemo.objects.filter(id=int(memoNo)).exists()

    if memoNo is '' or not memoExist:
        data = {
            'isSuccessful': False,


        }
    else:
        saleMemoObject = PurchaseMemo.objects.filter(id=int(memoNo)).get()
        dataForTable=''
        for i in saleMemoObject.purchaseItem.all():
            dataForTable += '<tr><td>' + str(i.item.itemName) + '</td>' + '<td>' + str(
                i.item.itemSize) + '</td>' + '<td>' + str(i.quantity) + '</td>' + '<td>' + str(
                i.free) + '</td>' + '<td>' + str(i.purchaseRate) + '</td>' + '<td>' + str(i.itemTotal()) + '</td>' + '</tr>'
        date= saleMemoObject.date

        data = {
            'isFound': True,
            'saleMemoObjectID': saleMemoObject.id,
            'date': date,
            'customer': saleMemoObject.party.name,
            'address': saleMemoObject.party.address,
            'sr': saleMemoObject.party.salesRepresentative.name,
            'dataForTable': dataForTable,
            'tempTotal': saleMemoObject.getTotal(),
            'discount': saleMemoObject.discount,
            'paid': saleMemoObject.paid,
        }


    return JsonResponse(data)
