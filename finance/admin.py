from django.contrib import admin

from finance.models import *

admin.site.register([Transaction, TransactionMode, Party])