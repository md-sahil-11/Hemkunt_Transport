from finance.models import Party, Transaction, TransactionMode
from trucking.models import Consignment, TripTransaction, Truck, Trip


def create_consignment(data):
    truck, _ = Truck.objects.get_or_create(truck_number=data["truck"].upper())
    consignor, _ = Party.objects.get_or_create(
        gstin=data["consignor_gst"].upper(), party_type="CONSIGNOR"
    )
    consignor.name = data["consignor_name"].upper()
    consignor.address = data["consignor_address"].upper()
    consignor.save()
    consignee, _ = Party.objects.get_or_create(
        gstin=data["consignee_gst"].upper(), party_type="CONSIGNEE"
    )
    consignee.name = data["consignee_name"].upper()
    consignee.address = data["consignee_address"].upper()
    consignee.save()
    # TODO: gst_payer (should ideally go in comments)
    consignment = Consignment(
        date=data["date"],
        nhrt_no=data["nhrt_no"],
        source=data["source"].upper(),
        destination=data["destination"].upper(),
        truck=truck,
        consignor=consignor,
        consignee=consignee,
        goods=data["description"].upper(),
        e_way_bill=data["ewaybill"],
        goods_value=data["value"],
        weight=data["weight"],
        rate=data["rate"],
        freight=data["freight"],
        advance=data["advance"],
        comment=data["comment"],
        advance_mode=data["advance_mode"],
        remaining_payment_type=data["remaining_payment_type"],
        remaining_payment=data["remaining_payment"],
    )
    consignment.save()
    return consignment


def create_trip(data):
    truck, _ = Truck.objects.get_or_create(truck_number=data["truck"].upper())
    consignment = Consignment.objects.get(id=data["consignment"])
    trucker, _ = Party.objects.get_or_create(
        gstin=data["trucker_gstin"].upper(), party_type="TRUCKER"
    )
    trucker.name = data["trucker_name"].upper()
    trucker.address = data["trucker_address"].upper()
    trucker.save()
    trip = Trip(
        truck=truck,
        consignment=consignment,
        goods=data["goods"].upper(),
        source=data["source"].upper(),
        destination=data["destination"].upper(),
        rate=data["rate"],
        weight=data["weight"],
        freight=data["freight"],
        driver_name=data["driver_name"].upper(),
        contact_number=data["contact_number"],
        owner_address=data["trucker_address"].upper(),
        guarantee=data["guarantee"].upper(),
        comment=data["comment"],
        date=data["date"],
        trucker=trucker,
        remaining_payment_type=data["remaining_payment_type"],
        remaining_payment=data["remaining_payment"],
    )
    trip.save()
    mode_list = data.getlist("mode")
    value_list = data.getlist("value")
    for i in range(0, len(mode_list)):
        mode, _ = TransactionMode.objects.get_or_create(name=mode_list[i].upper())
        transaction = Transaction(
            party=trucker,
            date=data["date"],
            mode=mode,
            value=-1 * float(value_list[i]),
            comment=str(value_list[i] + "spent on" + mode_list[i]).upper(),
        )
        transaction.save()
        tt = TripTransaction(trip=trip, transaction=transaction)
        tt.save()
    return trip
