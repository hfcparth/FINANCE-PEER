from django.urls import path
from .views import (
registeration_view,
default_view,
signin_view,
signout_view,
home_view)

urlpatterns = [
    path('default/',default_view,name='default'),
    path('sign_up/',registeration_view,name='signup'),
    path('sign_in/',signin_view,name='signin'),
    path('sign_out/',signout_view,name='signout'),
    path('home/',home_view,name='home')

]
