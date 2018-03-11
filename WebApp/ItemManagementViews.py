from itertools import chain

from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context_processors import csrf

from WebApp.models import Item


def showItemPage(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')

    c = {}
    c.update(csrf(request))
    return render_to_response('item.html', c)


def showItemAddPage(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')
    c = {}

    print(request)

    if request.POST.get('addButton'):
        name = request.POST.get('itemName', '')
        size = request.POST.get('itemSize', '')
        stockRate = request.POST.get('stockRate','0')
        saleRate = request.POST.get('saleRate','0')

        if stockRate=='':
            stockRate=0.0
        if saleRate=='':
            saleRate=0.0

        itemAddObject = Item(itemName=name, itemSize=size, stockRate=float(stockRate), saleRate=float(saleRate))
        itemAddObject.save();

    elif request.POST.get('searchButton'):
        searchItemName = request.POST.get('searchItemName','')
        searchItemId =request.POST.get('searchItemId','')
        searchItemSize =request.POST.get('searchItemSize','')
        if searchItemId == '':
            searchItemId=-1

        if searchItemName =='' and searchItemSize == '':
            filteredItems= Item.objects.all()
            c.update({'SEARCHED_ITEMS': filteredItems})
        elif searchItemName =='':
            filteredItems= Item.objects.filter(Q(id=int(searchItemId)) |  Q(itemSize__icontains=searchItemSize))
            c.update({'SEARCHED_ITEMS': filteredItems})
        elif searchItemSize == '':
            filteredItems= Item.objects.filter(Q(id=int(searchItemId)) | Q(itemName__icontains=searchItemName))
            c.update({'SEARCHED_ITEMS': filteredItems})
        else:
            filteredItems= Item.objects.filter(Q(id=int(searchItemId)) | Q(itemName__icontains=searchItemName) | Q(itemSize__icontains=searchItemSize))
            c.update({'SEARCHED_ITEMS': filteredItems})

    c.update(csrf(request))
    return render_to_response('item_add.html', c)


def showItemDeletePage(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')

    c={}
    if request.POST.get('searchButton'):
        searchItemName = request.POST.get('searchItemName','')
        searchItemId =request.POST.get('searchItemId','')
        searchItemSize =request.POST.get('searchItemSize','')
        if searchItemId == '':
            searchItemId=-1

        if searchItemName =='' and searchItemSize == '':
            filteredItems= Item.objects.all()
            c.update({'SEARCHED_ITEMS': filteredItems})
        elif searchItemName =='':
            filteredItems= Item.objects.filter(Q(id=int(searchItemId)) |  Q(itemSize__icontains=searchItemSize))
            c.update({'SEARCHED_ITEMS': filteredItems})
        elif searchItemSize == '':
            filteredItems= Item.objects.filter(Q(id=int(searchItemId)) | Q(itemName__icontains=searchItemName))
            c.update({'SEARCHED_ITEMS': filteredItems})
        else:
            filteredItems= Item.objects.filter(Q(id=int(searchItemId)) | Q(itemName__icontains=searchItemName) | Q(itemSize__icontains=searchItemSize))
            c.update({'SEARCHED_ITEMS': filteredItems})

    elif request.POST.get('deleteButton'):
        id = request.POST.get('itemId', '')

        if id == '':
            print('invalid')
        else:
            Item.objects.filter(id=id).delete()

    c.update(csrf(request))
    return render_to_response('item_delete.html', c)

def showItemEditPage(request):
    c={}

    if request.POST.get('searchButton'):
        searchItemName = request.POST.get('searchItemName','')
        searchItemId =request.POST.get('searchItemId','')
        searchItemSize =request.POST.get('searchItemSize','')
        if searchItemId == '':
            searchItemId=-1

        if searchItemName =='' and searchItemSize == '':
            filteredItems= Item.objects.all()
            c.update({'SEARCHED_ITEMS': filteredItems})
        elif searchItemName =='':
            filteredItems= Item.objects.filter(Q(id=int(searchItemId)) |  Q(itemSize__icontains=searchItemSize))
            c.update({'SEARCHED_ITEMS': filteredItems})
        elif searchItemSize == '':
            filteredItems= Item.objects.filter(Q(id=int(searchItemId)) | Q(itemName__icontains=searchItemName))
            c.update({'SEARCHED_ITEMS': filteredItems})
        else:
            filteredItems= Item.objects.filter(Q(id=int(searchItemId)) | Q(itemName__icontains=searchItemName) | Q(itemSize__icontains=searchItemSize))
            c.update({'SEARCHED_ITEMS': filteredItems})

    elif request.POST.get('saveButton'):
        id = request.POST.get('itemId', '-1')
        item = Item.objects.filter(id=int(id)).get()
        item.itemName = request.POST.get('itemName', '')
        item.itemSize = request.POST.get('itemSize', '')
        item.stockRate = float(request.POST.get('stockRate', ''))
        item.saleRate = float(request.POST.get('saleRate', ''))
        item.save()
        print("here")

    c.update(csrf(request))
    return render_to_response('item_edit.html', c)
