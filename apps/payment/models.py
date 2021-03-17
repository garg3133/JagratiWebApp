from django.db import models


# Create your models here.

class Transaction(models.Model):
    name = models.CharField(max_length=80)
    email = models.CharField(max_length=127)
    order_id = models.CharField(max_length=80)
    currency = models.CharField(max_length=50)
    gateway_name = models.CharField(max_length=200)
    response_msg = models.TextField()
    bank_name = models.CharField(max_length=100)
    payment_mode = models.CharField(max_length=100)
    mid = models.CharField(max_length=100)
    response_code = models.CharField(max_length=50)
    txn_id = models.CharField(max_length=200)
    txn_amount = models.CharField(max_length=50)
    status = models.CharField(max_length=80)
    bank_txn_id = models.CharField(max_length=100)
    txn_date = models.CharField(max_length=80)
