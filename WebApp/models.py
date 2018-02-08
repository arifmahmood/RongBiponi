from django.db import models


# Create your models here.


class Item(models.Model):
    itemName = models.CharField(max_length=50)
    itemSize = models.CharField(max_length=50)
    stockRate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    saleRate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    itemAvailable= models.IntegerField(default=0)
    itemFree= models.IntegerField(default=0)

    def __str__(self):
        return self.itemName


class SalesRepresentative(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Supplier(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=150)
    mobileNo = models.CharField(max_length=20)
    salesRepresentative = models.ForeignKey(SalesRepresentative)

    def __str__(self):
        return self.name


class Customer(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=150)
    mobileNo = models.CharField(max_length=20)
    salesRepresentative = models.ForeignKey(SalesRepresentative)


    def __str__(self):
        return self.name


class SaleItem(models.Model):
    quantity = models.IntegerField(default=0)
    free = models.IntegerField(default=0)
    item = models.ForeignKey(Item)


    def itemTotal(self):
        return (self.quantity - self.free) * self.item.sale_rate


class SaleMemo(models.Model):
    date = models.DateField()
    party = models.ForeignKey(Customer)
    saleItem = models.ManyToManyField(SaleItem)
    discount = models.DecimalField(max_digits=10, decimal_places=2,default=0, blank=True, null=True)
    paid = models.DecimalField(max_digits=10, decimal_places=2,default=0, blank=True, null=True)

    def getTotal(self):
        # type: () -> object
        return sum(i.itemTotal() for i in self.saleItem.all())


class PurchaseItem(models.Model):
    quantity = models.IntegerField(default=0)
    free = models.IntegerField(default=0)
    item = models.ForeignKey(Item)


    def itemTotal(self):
        return (self.quantity - self.free) * self.item.saleRate


class PurchaseMemo(models.Model):
    givenMemoNo = models.IntegerField(default=0)
    date = models.DateField()
    party = models.ForeignKey(Supplier)
    purchaseItem = models.ManyToManyField(PurchaseItem)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    paid = models.DecimalField(max_digits=10, decimal_places=2,default=0, blank=True, null=True)




    def getTotal(self):
        return sum(i.itemTotal() for i in self.purchaseItem.all())






