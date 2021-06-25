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
    consignor = models.ForeignKey(Party, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='consignor')
    consignee = models.ForeignKey(Party, on_delete=models.DO_NOTHING,  null=True, blank=True, related_name='consignee')
    truck = models.ForeignKey(Truck, on_delete=models.DO_NOTHING, null=True, blank=True)
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
    discount = models.FloatField(default=0.0)
    status = models.BooleanField(default=False)


class Trip(models.Model):
    truck = models.ForeignKey(Truck, on_delete=models.DO_NOTHING)
    consignment = models.ForeignKey(Consignment, on_delete=models.DO_NOTHING, null=True, blank=True)
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
    trucker = models.ForeignKey(Party, on_delete=models.DO_NOTHING, null=True, blank=True)
    date = models.DateField(default=datetime.now)
    date_end = models.DateField(default=datetime.now)
    status = models.BooleanField(default=False)
    loss = models.FloatField(default=0.0)


class TripTransaction(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)


class Diesel(models.Model):
    company = models.CharField(max_length=100, null=True, blank=True)
    value = models.FloatField(default=0.0, null=True, blank=True)
    status = models.BooleanField(default=False)


@receiver(post_save, sender=Consignment)
def create_transactions(sender, instance, created, **kwargs):
    if created:
        mode, _ = TransactionMode.objects.get_or_create(name="CONSIGNMENT FREIGHT COST")
        t = Transaction(
            mode=mode,
            value=(-1) * float(instance.freight),
            date=instance.date,
            party=instance.consignor,
            comment="Consignment ID-" + str(instance.id),
        )
        t.save()

        if float(instance.advance) > 0:
            mode, _ = TransactionMode.objects.get_or_create(name=instance.advance_mode)
            t = Transaction(
                mode=mode,
                value=float(instance.advance),
                date=instance.date,
                party=instance.consignor,
                comment="Consignment ID-" + str(instance.id),
            )
            t.save()


@receiver(post_delete, sender=Consignment)
def delete_transaction(sender, instance, **kwargs):
    mode, _ = TransactionMode.objects.get_or_create(name="CONSIGNMENT")
    Transaction.objects.filter(
        mode=mode,
        value=(-1) * float(instance.freight),
        date=instance.date,
        party=instance.consignor,
        comment="Consignment ID-" + str(instance.id),
    ).delete()

    mode, _ = TransactionMode.objects.get_or_create(name="CONSIGNMENT ADVANCE")
    Transaction.objects.filter(
        mode=mode,
        value=float(instance.advance),
        date=instance.date,
        party=instance.consignor,
        comment="Consignment ID-" + str(instance.id),
    ).delete()


@receiver(post_save, sender=Trip)
def create_trip_transaction(sender, instance, created, **kwargs):
    if created:
        mode, _ = TransactionMode.objects.get_or_create(name="TRIP FREIGHT COST")
        t = Transaction(
            mode=mode,
            value=float(instance.freight),
            date=instance.date,
            party=instance.trucker,
            comment="Trip ID-" + str(instance.id),
        )
        t.save()


@receiver(post_delete, sender=Trip)
def delete_trip_transaction(sender, instance, **kwargs):
    mode, _ = TransactionMode.objects.get_or_create(name="TRIP FREIGHT COST")
    Transaction.objects.filter(
        mode=mode,
        value=float(instance.freight),
        date=instance.date,
        party=instance.trucker,
        comment="Trip ID-" + str(instance.id),
    ).delete()