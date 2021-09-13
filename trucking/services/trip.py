from finance.services.transaction import Receipt
from finance import TRUCKER
from finance.services import Payment
from finance.models import Party, Transaction

from trucking.models import Consignment, Trip, TripTransaction, Truck

from django.core.validators import EMPTY_VALUES


class TripWrapper:
    def __init__(self, data={}):
        if data in EMPTY_VALUES:
            return None
        self.truck_number = data["truck"].upper().strip()
        self.consignment_id = data["consignment"].upper().strip()
        self.trucker_gst = data["trucker_gstin"].upper().strip()
        self.trucker_name = data["trucker_name"].upper().strip()
        self.trucker_address = data["trucker_address"].upper().strip()
        self.trucker_phone = data["trucker_phone"].upper().strip()
        self.driver_name = data["driver_name"].upper().strip()
        self.contact_number = data["contact_number"].upper().strip()
        self.date = data["date"].strip()
        self.party = data["party"].strip()
        self.source = data["source"].upper().strip()
        self.destination = data["destination"].upper().strip()
        self.goods = data["goods"].upper().strip()
        self.guarantee = data["guarantee"].upper().strip()
        self.weight = data["weight"].strip().replace(",", "")
        self.rate = data["rate"].strip().replace(",", "")
        self.freight = data["freight"].strip().replace(",", "")
        self.comment = data["comment"].strip()
        self.remaining_payment_type = data["remaining_payment_type"].strip()
        self.remaining_payment = data["remaining_payment"].strip().replace(",", "")
        self.end_date = data.get("end_date", None)
        if self.end_date in EMPTY_VALUES:
            self.end_date = None
        self.mode_list = data.getlist("mode")
        self.value_list = data.getlist("value")
        # self.expense_comments_list = data.getlist("expense_comment")
        return None

    def get_party_instance(self, name, party_type):
        party, _ = Party.objects.get_or_create(name=name, party_type=party_type)
        return party

    def get_trucker_instance(self):
        trucker = self.get_party_instance(self.trucker_name, TRUCKER)
        trucker.gstin = self.trucker_gst
        trucker.address = self.trucker_address
        trucker.phone = self.trucker_phone
        trucker.save()
        return trucker

    def get_truck_instance(self):
        truck, _ = Truck.objects.get_or_create(truck_number=self.truck_number)
        return truck

    def get_consignment_instance(self):
        return Consignment.objects.get(id=self.consignment_id)

    def get_trip_instance(self, trip_id=None):
        if trip_id not in EMPTY_VALUES:
            return Trip.objects.get(id=trip_id)
        return Trip()

    def save_to_db(self, trip_instance):
        trip_instance.truck = self.get_truck_instance()
        trip_instance.consignment = self.get_consignment_instance()
        trip_instance.goods = self.goods
        trip_instance.source = self.source
        trip_instance.destination = self.destination
        trip_instance.rate = self.rate
        trip_instance.weight = self.weight
        trip_instance.freight = self.freight
        trip_instance.driver_name = self.driver_name
        trip_instance.contact_number = self.contact_number
        trip_instance.owner_address = self.trucker_address
        trip_instance.guarantee = self.guarantee
        trip_instance.comment = self.comment
        trip_instance.date = self.date
        trip_instance.trucker = self.get_trucker_instance()
        trip_instance.remaining_payment_type = self.remaining_payment_type
        trip_instance.remaining_payment = self.remaining_payment
        trip_instance.party = self.party
        if self.end_date not in EMPTY_VALUES:
            trip_instance.end_date = self.end_date
            trip_instance.completed = True
        trip_instance.save()
        return trip_instance

    def create(self):
        trip_instance = self.get_trip_instance()
        trip_instance = self.save_to_db(trip_instance)
        trip_instance = self.create_intermediate_transactions(trip_instance)
        return trip_instance

    def create_intermediate_transactions(self, trip_instance):
        mode_list = self.mode_list
        value_list = self.value_list
        # comment_list = self.expense_comments_list
        for i in range(len(mode_list)):
            data = {
                "mode": mode_list[i].upper().strip(),
                "value": float(value_list[i]),
                "date": self.date,
                "party": str(trip_instance.trucker.id),
                "comment": "Trip ID-{id} -- {comment}".format(id=str(trip_instance.id), comment=""),
            }
            transaction = Payment(data).create()
            tt = TripTransaction(trip=trip_instance, transaction=transaction)
            tt.save()
        return trip_instance

    def add_transactions(self, trip_instance, mode="TRIP FREIGHT COST"):
        data = {
            "mode": mode,
            "value": trip_instance.freight,
            "date": trip_instance.date,
            "party": str(trip_instance.trucker.id),
            "comment": "Trip ID-" + str(trip_instance.id),
        }
        return Receipt(data).create()

    def delete_transactions(self, trip):
        qs = Transaction.objects.filter(comment__contains="Trip ID-" + str(trip.id))
        for q in qs:
            q.delete()
        return True

    def update_transactions(self, trip_instance):
        self.delete_transactions(trip_instance)
        self.add_transactions(trip_instance)
        trip_instance = self.create_intermediate_transactions(trip_instance)
        return trip_instance

    def update(self, trip_id):
        trip_instance = self.get_trip_instance(trip_id)
        trip_instance = self.save_to_db(trip_instance)
        trip_instance = self.update_transactions(trip_instance)
        return trip_instance
