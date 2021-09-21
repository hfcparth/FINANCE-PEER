from django import forms
from account.models import Account
from .models import Stock


class BalanceForm(forms.Form):
    add_balance=forms.FloatField(help_text='Enter the balance to be added',required=True)

    def clean_add_balance(self):

        print(self)
        data=self.cleaned_data['add_balance']
        print(data)
        if data<0:
            raise forms.ValidationError('The balance to add must be positive')

        return data

class StockForm(forms.ModelForm):
    share_id=forms.CharField(min_length=5,max_length=5)
    class Meta:
        model = Stock
        fields = ['share_id','company_name','face_value','quantity']

    def clean_face_value(self):
        data=self.cleaned_data['face_value']
        if(data <= 0):
            raise forms.ValidationError('face value must be positive')

        return data

    def clean_quantity(self):
        data=self.cleaned_data['quantity']
        if(data <= 0):
            raise forms.ValidationError('quantity must be positive')

        return data


class BuyForm(forms.Form):
    qty=forms.IntegerField(help_text='Enter the quantity you want to buy',required=True)

    def clean_qty(self):

        print(self)
        data=self.cleaned_data['qty']

        if data<=0:
            raise forms.ValidationError('The quantity to add must be positive')

        return data


class SellForm(forms.Form):
    qty=forms.IntegerField(help_text='Enter the quantity you want to sell',required=True)
    sell_value=forms.FloatField(help_text='Enter the price at which you wanna sell the stock',required=True)

    def clean_qty(self):

        print(self)
        data=self.cleaned_data['qty']

        if data<=0:
            raise forms.ValidationError('The quantity to add must be positive')

        return data

    def clean_sell_value(self):

        print(self)
        data=self.cleaned_data['sell_value']

        if data<=0:
            raise forms.ValidationError('The sell price must be positive must be positive')

        return data
