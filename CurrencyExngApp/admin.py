from django.contrib import admin
from django.contrib.auth.models import Group

from CurrencyExngApp.models import *

admin.site.register(Wallet)
admin.site.register(Transaction)
admin.site.register(User)


