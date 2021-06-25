from django.contrib import admin

from trucking.models import *

admin.site.register([Consignment, Truck, Trip])
