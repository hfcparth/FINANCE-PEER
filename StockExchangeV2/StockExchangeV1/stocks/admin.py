from django.contrib import admin
from stocks.models import Stock,Auction,Buyorder
# Register your models here.




admin.site.register(Stock)
admin.site.register(Auction)
admin.site.register(Buyorder)
