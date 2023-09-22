from django.contrib import admin

from .models import Transaction, MpesaResponseBody

admin.site.register(Transaction)
admin.site.register(MpesaResponseBody)