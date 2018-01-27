from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from WebApp.models import Item


@csrf_exempt
def getItem(request):
    itemId = request.POST.get('itemId','')
    # itemExist = False
    # while itemExist is False:
    #     itemExist = Item.objects.filter(id = int(itemId)).exists()
    #     itemId= int(itemId)+1
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
