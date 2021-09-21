from django.urls import path
from .views import(
balance_view,
add_stock,
list_auction,
buy_stock,
view_portfolio,
sell_stock
)


urlpatterns = [
    path('balance/',balance_view,name='balance'),
    path('add_stock/',add_stock,name='add stock'),
    path('sell_stock/<str:id>/',sell_stock,name='sell stock'),
    path('list_auction/',list_auction,name='list auction'),
    path('buy_stock/<int:id>/',buy_stock,name='buy stock'),
    path('portfolio/',view_portfolio,name='portfolio')
]
