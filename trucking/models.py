from datetime import datetime
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from finance.models import Party, Transaction, TransactionMode


class Truck(models.Model):
    truck_number = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.truck_number


class Consignment(models.Model):
    date = models.DateField(default=datetime.now)
    source = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    consignor = models.ForeignKey(
        Party,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="consignor",
    )
    consignee = models.ForeignKey(
        Party,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="consignee",
    )
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE, null=True, blank=True)
    goods = models.TextField(null=True, blank=True)
    e_way_bill = models.CharField(max_length=100, null=True, blank=True)
    weight = models.FloatField(default=0.0)
    rate = models.FloatField(default=0.0)
    freight = models.FloatField(default=0.0)
    advance_mode = models.CharField(max_length=100, null=True, blank=True)
    advance = models.FloatField(default=0.0)
    remaining_payment_type = models.CharField(max_length=100, default="TO PAY")
    remaining_payment = models.FloatField(default=0.0)
    gst_payer = models.CharField(max_length=100, default="CONSIGNEE")
    goods_value = models.FloatField(default=0.0)
    comment = models.TextField(null=True, blank=True)
    nhrt_no = models.CharField(max_length=50, null=True, blank=True)
    invoice_no = models.CharField(max_length=50, null=True, blank=True)
    discount = models.FloatField(default=0.0)
    consignor_pay = models.FloatField(default=0.0, null=True, blank=True)
    consignee_pay = models.FloatField(default=0.0, null=True, blank=True)


class Trip(models.Model):
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE)
    consignment = models.ForeignKey(
        Consignment, on_delete=models.CASCADE, null=True, blank=True
    )
    goods = models.CharField(max_length=200, null=True, blank=True)
    source = models.CharField(max_length=200, null=True, blank=True)
    destination = models.CharField(max_length=200, null=True, blank=True)
    rate = models.FloatField(default=0.0)
    weight = models.FloatField(default=0.0)
    freight = models.FloatField(default=0.0)
    driver_name = models.CharField(max_length=200, null=True, blank=True)
    contact_number = models.CharField(max_length=200, null=True, blank=True)
    owner_address = models.CharField(max_length=200, null=True, blank=True)
    remaining_payment_type = models.CharField(max_length=100, default="TO PAY")
    remaining_payment = models.FloatField(default=0.0)
    guarantee = models.TextField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    trucker = models.ForeignKey(
        Party, on_delete=models.CASCADE, null=True, blank=True
    )
    date = models.DateField(default=datetime.now)
    party = models.CharField(max_length=100, null=True, blank=True)
    completed = models.BooleanField(default=False)
    end_date = models.DateField(null=True, blank=True)


class TripTransaction(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)



@receiver(post_save, sender=Consignment)
def create_consignment_transactions(sender, instance, created, **kwargs):
    from trucking.services import ConsignmentWrapper
    if created:
        obj = ConsignmentWrapper()
        obj.add_transactions(instance)


@receiver(post_delete, sender=Consignment)
def delete_consignment_transactions(sender, instance, **kwargs):
    from trucking.services import ConsignmentWrapper
    obj = ConsignmentWrapper()
    obj.delete_transactions(instance.id)


@receiver(post_save, sender=Trip)
def create_trip_transaction(sender, instance, created, **kwargs):
    from trucking.services import TripWrapper
    if created:
        obj = TripWrapper()
        obj.add_transactions(instance)

@receiver(post_delete, sender=Trip)
def delete_trip_transaction(sender, instance, **kwargs):
    from trucking.services import TripWrapper
    obj = TripWrapper()
    obj.delete_transactions(instance)
