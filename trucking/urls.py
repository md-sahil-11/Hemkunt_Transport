from django.urls import path
from .views import *

urlpatterns = [
    path('', consignment_view, name="consignment"),
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
#     path('trip/end/<int:trip_id>/', trip_end, name='end_trip'),
#     path('trip/fuel', fuel_history, name="fuel_history"),
#     path('fuel/status/<int:fuel_id>', fuel_status, name="fuel_status"),
    path('consignment/delete/<int:consignment_id>', consignment_delete, name="consignment_delete"),
    path('trip/delete/<int:trip_id>', trip_delete, name="trip_delete"),
    path('login/user', login_user, name='login'),
    path('consignment/update/<int:consignment_id>', consignment_update, name="consignment_update"),
    path('consignment/details/', consignment_details, name="consignment_details"),
    path('trip/update/<int:id>', trip_update, name="trip_update"),
    path('trip/details/', trip_details, name="trip_details")
]
