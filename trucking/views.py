from finance import CONSIGNOR, CONSIGNEE, TRUCKER
from trucking.services import ConsignmentWrapper, TripWrapper
from django.http.response import JsonResponse
from finance.models import Party, TransactionMode
from trucking.models import Consignment, TripTransaction, Truck, Trip
from django.shortcuts import redirect, render
from trucking.services import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.core import serializers

from datetime import date, timedelta


def login_user(request):
    if request.method == "POST":
        user = authenticate(
            username=request.POST.get("username"), password=request.POST.get("password")
        )
        if user is not None:
            login(request, user)
            return redirect("consignment")
        else:
            context = {"message": "Wrong password or username."}
            return render(request, "registration/login.html", context)
    return render(request, "registration/login.html")


@login_required
def consignment_view(request):
    if request.method == "POST":
        consignment = ConsignmentWrapper(request.POST).create()
        return redirect("consignment_slip", consignment_id=consignment.id)

    context = {
        "trucks": Truck.objects.all(),
        "consignors": Party.objects.filter(party_type=CONSIGNOR),
        "consignees": Party.objects.filter(party_type=CONSIGNEE),
        "modes": TransactionMode.objects.all(),
    }
    return render(request, "bill_form.html", context)


@login_required
def consignment_slip(request, consignment_id):
    consignment = Consignment.objects.get(id=consignment_id)
    context = {"consignment": consignment}
    return render(request, "bill.html", context)


@login_required
def consignment_history(request):
    consignments = Consignment.objects.all()
    current_date = date.today().isoformat()
    days_before = (date.today() - timedelta(days=365)).isoformat()
    if request.method == "POST":
        try:
            consignments = consignments.filter(date__lte=request.POST.get("to"))
        except:
            pass
        try:
            consignments = consignments.filter(date__gte=request.POST.get("from"))
        except:
            pass
    else:
        consignments = consignments.filter(
            date__gte=days_before, date__lte=current_date
        ).order_by("-id")
    for consignment in consignments:
        trips = Trip.objects.filter(consignment=consignment)
        if (
            trips.exists()
            and trips.filter(completed=False).exists()
            or not trips.exists()
        ):
            consignment.status = False
        else:
            consignment.status = True
    context = {"consignments": consignments}
    return render(request, "consignment_history.html", context)


@login_required
def consignment_update(request, consignment_id):
    if request.method == "POST":
        ConsignmentWrapper(request.POST).update(consignment_id=consignment_id)
        return redirect("consignment_slip", consignment_id=consignment_id)

    context = {
        "trucks": Truck.objects.all(),
        "consignors": Party.objects.filter(party_type=CONSIGNOR),
        "consignees": Party.objects.filter(party_type=CONSIGNEE),
        "c": Consignment.objects.get(id=consignment_id),
        "modes": TransactionMode.objects.all(),
    }
    return render(request, "update.html", context)


@login_required
def trip(request, consignment_id):
    consignment = Consignment.objects.get(id=consignment_id)
    modes = TransactionMode.objects.all()
    if request.method == "POST":
        trip = TripWrapper(request.POST).create()
        return redirect("trip_slip", trip.id)
    context = {
        "trucks": Truck.objects.all(),
        "truckers": Party.objects.filter(party_type=TRUCKER),
        "consignment": consignment,
        "modes": modes,
    }
    return render(request, "trip.html", context)


@login_required
def trip_update(request, id):
    trip = Trip.objects.get(id=id)
    consignment = trip.consignment
    if request.method == "POST":
        trip = TripWrapper(request.POST).update(id)
        return redirect("trip_slip", trip.id)

    context = {
        "trip": trip,
        "consignment": consignment,
        "modes": TransactionMode.objects.all(),
    }
    return render(request, "trip_update.html", context)


@login_required
def trip_slip(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    transactions = TripTransaction.objects.filter(trip=trip)
    context = {"trip": trip, "transactions": transactions}
    return render(request, "trip_slip.html", context)


@login_required
def trip_history(request):
    trips = Trip.objects.all()
    current_date = date.today().isoformat()
    days_before = (date.today() - timedelta(days=365)).isoformat()
    if request.method == "POST":
        try:
            trips = trips.filter(date__lte=request.POST.get("to"))
        except:
            pass
        try:
            trips = trips.filter(date__gte=request.POST.get("from"))
        except:
            pass
    else:
        trips = trips.filter(date__gte=days_before, date__lte=current_date).order_by(
            "-date"
        )

    context = {"trips": trips}
    return render(request, "trip_history.html", context)


@login_required
def consignment_info(request, consignment_id):
    consignment = Consignment.objects.get(id=consignment_id)
    trips = Trip.objects.filter(consignment=consignment)
    context = {"consignment": consignment, "trips": trips}
    return render(request, "consignment_info.html", context)


@login_required
def consignment_delete(request, consignment_id):
    try:
        consignment = Consignment.objects.get(id=consignment_id)
        consignment.delete()
    except:
        pass
    return render(request, "consignment_history.html")


@login_required
def trip_info(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    transactions = TripTransaction.objects.filter(trip=trip)
    context = {
        "trips": trip,
        "transactions": transactions,
    }
    for t in transactions:
        t.transaction.comment = t.transaction.comment.replace("Trip ID-{} -- ".format(str(t.trip.id)), "")
    return render(request, "trip_info.html", context)


@login_required
def trip_delete(request, trip_id):
    try:
        trip = Trip.objects.get(id=trip_id)
        trip.delete()
    except:
        pass
    return render(request, "trip_history.html")


@login_required
def truck_history(request, truck_number):
    truck = Truck.objects.get(truck_number=truck_number.upper())
    trips = Trip.objects.filter(truck=truck)
    consignments = Consignment.objects.filter(truck=truck)
    context = {"trips": trips, "consignments": consignments, "truck": truck}
    return render(request, "truck_history.html", context)


# @login_required
# def fuel_history(request):
#     diesels = Diesel.objects.all()
#     context = {"fuels": diesels}
#     return render(request, "fuel_history.html", context)


# # @login_required
# def fuel_status(request, fuel_id):
#     d = Diesel.objects.get(id=fuel_id)
#     d.status = True
#     d.save()
#     return JsonResponse({"success": True}, status=200)


def consignment_details(request):
    id = request.GET.get("id")
    c = Consignment.objects.filter(id=id)
    consignor = c[0].consignor.gstin
    consignee = c[0].consignee.gstin
    data = serializers.serialize("json", c)
    return JsonResponse(
        {"data": data, "consignor_gstin": consignor, "consignee_gstin": consignee},
        status=200,
    )


def trip_details(request):
    trip_id = request.GET.get("id")
    trips = Trip.objects.filter(id=trip_id)
    t = trips[0]

    trucker = t.trucker.name
    data = serializers.serialize("json", trips)
    transactions = TripTransaction.objects.filter(trip=t)
    expenses = [
        {
            "mode": t.transaction.mode.name,
            "value": -1 * float(t.transaction.value),
            "comment": t.transaction.comment.replace("Trip ID-{} -- ".format(str(t.trip.id)), "")
        }
        for t in transactions
    ]
    return JsonResponse(
        {"data": data, "trucker_name": trucker, "expenses": expenses},
        status=200,
    )

