from django.urls import path
from .views import *
from finance import api

urlpatterns = [
    path('ledger/<str:party_id>/', ledger, name='ledger'),
    path('consignors', consignors, name="consignors"),
    path('party', api.get_party, name='party'),
    path('truckers', truckers, name="truckers"),
    path('consignees', consignees, name="consignees"),
    path('payment', payment_view, name='payment'),
    path('receipt', receipt_view, name='receipt')
]