from django.urls import path
from .views import *

urlpatterns = [
    path('', consignment, name="consignment"),
    path('consignment/history/', consignment_history, name="consignment_history"),
    path('consignment/slip/<int:consignment_id>',
         consignment_slip, name='consignment_slip'),
    path('trip/slip/<int:trip_id>',
         trip_slip, name='trip_slip'),
    path('consignment/info/<int:consignment_id>',
         consignment_info, name='consignment_info'),
    path('trip/<int:consignment_id>', trip, name="trip"),
    path('trip/history/', trip_history, name="trip_history"),
    path('trip/info/<int:trip_id>', trip_info, name='trip_info'),
    path('truck/<str:truck_number>', truck_history, name="truck_history"),
    path('trip/end/<int:trip_id>/', trip_end, name='end_trip')
]
