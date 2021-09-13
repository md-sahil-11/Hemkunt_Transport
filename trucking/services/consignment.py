from finance import CONSIGNOR, CONSIGNEE
from finance.models import Party, Transaction
from finance.services import Payment

from trucking.models import Consignment, Truck

from django.core.validators import EMPTY_VALUES


class ConsignmentWrapper:
    def __init__(self, data={}):
        if data in EMPTY_VALUES:
            return None
        self.truck_number = data["truck"].upper().strip()
        self.consignor_gst = data["consignor_gst"].upper().strip()
        self.consignee_gst = data["consignee_gst"].upper().strip()
        self.consignor_name = data["consignor_name"].upper().strip()
        self.consignee_name = data["consignee_name"].upper().strip()
        self.consignor_address = data["consignor_address"].upper().strip()
        self.consignee_address = data["consignee_address"].upper().strip()
        self.invoice_no = data["invoice_no"].strip()
        self.date = data["date"].strip()
        self.nhrt_no = data["nhrt_no"].strip()
        self.source = data["source"].upper().strip()
        self.destination = data["destination"].upper().strip()
        self.goods = data["description"].upper().strip()
        self.e_way_bill = data["ewaybill"].strip()
        self.goods_value = data["value"].strip()
        self.weight = data["weight"].strip()
        self.rate = data["rate"].strip()
        self.freight = data["freight"].strip()
        self.advance = data["advance"].strip()
        self.comment = data["comment"].strip()
        self.remaining_payment_type = data["remaining_payment_type"].strip()
        self.remaining_payment = data["remaining_payment"].strip()
        self.consignor_pay = data["consignor_pay"].strip()
        self.consignee_pay = data["consignee_pay"].strip()
        return None

    def get_party_instance(self, gst_number, party_type):
        party, _ = Party.objects.get_or_create(gstin=gst_number, party_type=party_type)
        return party

    def get_consignor_instance(self):
        consignor = self.get_party_instance(self.consignor_gst, CONSIGNOR)
        consignor.name = self.consignor_name
        consignor.address = self.consignor_address
        consignor.save()
        return consignor

    def get_consignee_instance(self):
        consignee = self.get_party_instance(self.consignee_gst, CONSIGNEE)
        consignee.name = self.consignee_name
        consignee.address = self.consignee_address
        consignee.save()
        return consignee

    def get_truck_instance(self):
        truck, _ = Truck.objects.get_or_create(truck_number=self.truck_number)
        return truck

    def get_consignment_instance(self, consignment_id=None):
        if consignment_id not in EMPTY_VALUES:
            return Consignment.objects.get(id=consignment_id)
        return Consignment()

    def save_to_db(self, consignment_instance):
        consignment_instance.date = self.date
        consignment_instance.nhrt_no = self.nhrt_no
        consignment_instance.source = self.source
        consignment_instance.destination = self.destination
        consignment_instance.truck = self.get_truck_instance()
        consignment_instance.consignor = self.get_consignor_instance()
        consignment_instance.consignee = self.get_consignee_instance()
        consignment_instance.goods = self.goods
        consignment_instance.e_way_bill = self.e_way_bill
        consignment_instance.goods_value = self.goods_value
        consignment_instance.weight = self.weight
        consignment_instance.rate = self.rate
        consignment_instance.freight = self.freight
        consignment_instance.advance = self.advance
        consignment_instance.comment = self.comment
        consignment_instance.remaining_payment_type = self.remaining_payment_type
        consignment_instance.remaining_payment = self.remaining_payment
        consignment_instance.consignor_pay = self.consignor_pay
        consignment_instance.consignee_pay = self.consignee_pay
        consignment_instance.invoice_no = self.invoice_no
        consignment_instance.save()
        self.consignment_id = consignment_instance.id
        return consignment_instance

    def create(self):
        consignment_instance = self.get_consignment_instance()
        self.save_to_db(consignment_instance)
        return consignment_instance

    def delete_transactions(self, consignment_id):
        qs = Transaction.objects.filter(
            comment__contains="Consignment ID-" + str(consignment_id)
        )
        for q in qs:
            q.delete()
        return True

    def add_transactions(self, consignment_instance, mode="CONSIGNMENT FREIGHT COST"):
        data = {
            "mode": mode,
            "value": consignment_instance.consignor_pay,
            "date": consignment_instance.date,
            "party": str(consignment_instance.consignor.id),
            "comment": "Consignment ID-" + str(consignment_instance.id),
        }
        Payment(data).create()

        data["value"] = consignment_instance.consignee_pay
        data["party"] = str(consignment_instance.consignee.id)
        Payment(data).create()
        return True

    def update_transactions(self, consignment_instance):
        self.delete_transactions(consignment_instance.id)
        self.add_transactions(consignment_instance)
        return True

    def update(self, consignment_id):
        consignment_instance = self.get_consignment_instance(consignment_id)
        self.save_to_db(consignment_instance)
        self.update_transactions(consignment_instance)
        return consignment_instance
