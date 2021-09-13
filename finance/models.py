from datetime import datetime

from django.db import models
from django.db.models import Sum
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

PARTY_CHOICES = (
    ("CONSIGNOR", "CONSIGNOR"),
    ("CONSIGNEE", "CONSIGNEE"),
    ("TRUCKER", "TRUCKER"),
)


class TransactionMode(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Party(models.Model):
    name = models.CharField(max_length=100)
    gstin = models.CharField(max_length=100, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    state = models.CharField(max_length=30, default="ODISHA")
    state_code = models.IntegerField(default=21)
    party_type = models.CharField(max_length=30, choices=PARTY_CHOICES, default="CONSIGNOR")
    balance = models.FloatField(default=0.0)
    phone = models.CharField(max_length=30, null=True, blank=True)
    pan = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    party = models.ForeignKey(Party, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(default=datetime.now)
    time = models.TimeField(default=datetime.now)
    mode = models.ForeignKey(
        TransactionMode, on_delete=models.DO_NOTHING, null=True, blank=True
    )
    value = models.FloatField(default=0.0)
    comment = models.TextField(null=True, blank=True)


def calculate_balance(party):
    transactions = Transaction.objects.filter(party=party)
    if not transactions:
        return 0
    return transactions.aggregate(Sum("value"))["value__sum"]


@receiver(post_save, sender=Transaction)
def increase_balance(sender, instance, created, **kwargs):
    if created:
        try:
            instance.party.balance = calculate_balance(instance.party)
            instance.party.save()
        except:
            # ! Incase of party does not exist
            pass


@receiver(post_delete, sender=Transaction)
def decrease_balance(sender, instance, **kwargs):
    try:
        instance.party.balance = calculate_balance(instance.party)
        instance.party.save()
    except:
        # ! Incase of party does not exist
        pass
