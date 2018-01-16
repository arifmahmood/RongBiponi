from django.contrib import admin

# Register your models here.
from WebApp import models

admin.site.register(models.Item)
admin.site.register(models.SalesRepresentative)
admin.site.register(models.Customer)
admin.site.register(models.Supplier)
admin.site.register(models.SaleItem)
admin.site.register(models.SaleMemo)
admin.site.register(models.PurchaseItem)
admin.site.register(models.PurchaseMemo)