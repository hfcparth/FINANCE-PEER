from django.shortcuts import render, get_object_or_404,redirect
from .forms import BalanceForm,StockForm,BuyForm,SellForm
from account.models import Account
from .models import Auction,Stock,Buyorder
from django.contrib.admin.views.decorators import staff_member_required
# Create your views here.

def balance_view(request):
    context={}
    user=get_object_or_404(Account,email=request.user.email)
    if request.POST:
        form=BalanceForm(request.POST)
        if form.is_valid:
            print("ppp")
            data=form.clean_add_balance()
            user.user_balance=user.user_balance+data
            user.save()
            return redirect('home')
    else:
        form=BalanceForm()
        print(form)
        context['current_balance']=user.user_balance
        context['form']=form
    return render(request,'stocks/balance.html',context)

@staff_member_required
def add_stock(request):
    context={}

    if request.POST:
        form=StockForm(request.POST)
        if form.is_valid():
            obj=form.save(commit=False)
            print(form.cleaned_data)
            print(obj)
            obj.current_value=obj.face_value
            print(obj)
            print(form.cleaned_data)
            obj.save()

            auc=Auction.objects.create(seller=Account.objects.get(email=request.user.email),share_id=Stock.objects.get(share_id=obj.share_id),quantity=obj.quantity,sell_value=obj.face_value)
            auc.save()
            return redirect('home')
        else:
            context['stock_form']=form
    else:
        form=StockForm()
        context['stock_form']=form

    return render(request,'stocks/stock_add_form.html',context)



def list_auction(request):
    all_entries = Auction.objects.all()
    context = {'auction_list':all_entries}
    return render(request,'stocks/auction_list.html',context)


def buy_stock(request,id):
    context={}
    context['error']=[]
    auction=get_object_or_404(Auction,id=id)
    user=get_object_or_404(Account,email=request.user.email)
    if request.POST:
        form=BuyForm(request.POST)
        if form.is_valid:
            print("ppp")
            print(form)
            qty=form.cleaned_data['qty']
            if(qty<=auction.quantity):
                if(qty*auction.sell_value<user.user_balance):
                    buy=Buyorder.objects.create(buyer=Account.objects.get(email=request.user.email),seller=auction.seller,quantity=qty,buy_value=auction.sell_value,share_id=auction.share_id)
                    auction.quantity=auction.quantity-qty
                    auction.share_id.current_value=auction.sell_value
                    auction.share_id.save()
                    auction.save()
                    user.user_balance=user.user_balance-(qty*auction.sell_value)
                    auction.seller.user_balance=auction.seller.user_balance+(qty*auction.sell_value)
                    auction.seller.save()
                    user.save()
                    return redirect('home')
                else:
                    context['form']=form
                    context['error'].append('Not enough balance')
            else:
                context['form']=form
                context['error'].append('quantity not available')
        else:
            context['form']=form
            context['error'].append('form not valid')
    else:
        form=BuyForm()
        print(form)
        context['auction']=auction
        context['buyer']=user
        context['form']=form
    return render(request,'stocks/buy.html',context)


def view_portfolio(request):
    context={}
    info=(create_portfolio(request.user))
    context['info_buy']=info['buy']
    context['info_sell']=info['sell']
    context['info_net']=info['net']
    context['user_sell']=Buyorder.objects.filter(seller=request.user)
    context['user_buy']=Buyorder.objects.filter(buyer=request.user)
    context['buy_order']=Buyorder
    print(context['user_buy'])
    return render(request,'stocks/portfolio.html',context)


def sell_stock(request,id):
    context={}
    context['error']=[]
    data=create_portfolio(request.user)
    sdata=None
    for i in data['net']:
        if(id==i[0]):
            sdata=i
            break
    if request.POST:
        form=SellForm(request.POST)
        if form.is_valid():
            qty=form.cleaned_data['qty']
            sell_price=form.cleaned_data['sell_value']
            if(qty<=sdata[1]):
                auc=Auction.objects.create(seller=Account.objects.get(email=request.user.email),share_id=Stock.objects.get(share_id=sdata[0]),quantity=qty,sell_value=sell_price)
                auc.save()

                return redirect('portfolio')

            else:
                context['error'].append("The quantity you added is not owned by you")
        else:
            context['error'].append("Form not valid")

    else:
        form=SellForm()
        context['sell_form']=form
        context['share_info']=sdata
    return render(request,'stocks/sell_stocks.html',context)










def create_portfolio(userdata):
    portfolio={}
    bought=Buyorder.objects.filter(buyer=userdata)
    sold=Buyorder.objects.filter(seller=userdata)
    buy=[[],[],[]]
    sell=[[],[],[]]
    net=[[],[],[]]
    for b in bought:
        if(not (b.share_id.share_id in buy[0])):
            buy[0].append(b.share_id.share_id)
            buy[1].append(0)
            buy[2].append(0)

    print(buy)

    for i in range(len(buy[0])):
        for b in bought:
            if(buy[0][i]==b.share_id.share_id):
                buy[1][i]=buy[1][i]+b.quantity
                buy[2][i]=buy[1][i]*b.buy_value


    print(buy)
    for b in sold:
        if(not (b.share_id.share_id in sell[0])):
            sell[0].append(b.share_id.share_id)
            sell[1].append(0)
            sell[2].append(0)

    print(sell)
    for i in range(len(sell[0])):
        for b in sold:
            if(sell[0][i]==b.share_id.share_id):
                sell[1][i]=sell[1][i]+b.quantity
                sell[2][i]=sell[1][i]*b.buy_value

    print(sell)

    for i in range(len(buy[0])):
        f=False
        for j in range(len(sell[0])):

            if(sell[0][j]==buy[0][i]):
                net[0].append(buy[0][i])
                net[1].append(buy[1][i]-sell[1][j])
                net[2].append(buy[2][i]-sell[2][j])
                f=True
                break

        if(f==False):
            net[0].append(buy[0][i])
            net[1].append(buy[1][i])
            net[2].append(buy[2][i])


    print(net)
    b=[]
    s=[]
    n=[]
    for i in range(len(buy[0])):
        b.append([buy[0][i],buy[1][i],buy[2][i]])

    for i in range(len(sell[0])):
        s.append([sell[0][i],sell[1][i],sell[2][i]])

    for i in range(len(net[0])):
        n.append([net[0][i],net[1][i],net[2][i]])


    portfolio['buy']=b
    portfolio['sell']=s
    portfolio['net']=n
    print(portfolio)
    return portfolio
