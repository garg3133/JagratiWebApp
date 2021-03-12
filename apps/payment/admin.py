from django.contrib import admin
from .models import Transaction

# Register your models here.


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_id', 'gateway_name', 'bank_name',
                    'payment_mode', 'txn_id', 'txn_amount', 'status', 'txn_date')
    search_fields = ('order_id', 'txn_id', 'txn_date')
    ordering = ('-id',)
    list_filter = ('status', 'gateway_name', 'bank_name', 'payment_mode',)
