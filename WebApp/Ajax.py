from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from WebApp.models import Item, Customer, Supplier


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
