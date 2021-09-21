from django.db import models

# Create your models here.

class Stock(models.Model):
    share_id        =models.CharField(max_length=5,primary_key=True,unique=True)
    company_name    =models.CharField(max_length=30)
    face_value      =models.FloatField()
    current_value   =models.FloatField()
    quantity        =models.IntegerField(default=0)

class Auction(models.Model):
    seller              =models.ForeignKey('account.Account',on_delete=models.CASCADE)
    share_id            =models.ForeignKey('Stock',on_delete=models.CASCADE)
    quantity            =models.IntegerField()
    sell_value          =models.FloatField()
    timestamp           =models.DateTimeField(auto_now_add=True)
class Buyorder(models.Model):
    buyer               =models.ForeignKey('account.Account',on_delete=models.CASCADE,related_name='buyer')
    seller              =models.ForeignKey('account.Account',null=True,on_delete=models.SET_NULL,related_name='seller')
    quantity            =models.IntegerField()
    timestamp           =models.DateTimeField(auto_now_add=True)
    buy_value           =models.FloatField()
    share_id            =models.ForeignKey('Stock',on_delete=models.CASCADE,null=True)
