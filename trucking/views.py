
from finance.models import Party, TransactionMode
from trucking.models import Consignment, TripTransaction, Truck, Trip
from django.shortcuts import redirect, render
from trucking.services import create_consignment, create_trip

from datetime import date, timedelta


def consignment(request):
    if request.method == "POST":
        consignment = create_consignment(request.POST)
        return redirect('consignment_slip', consignment_id=consignment.id)

    context = {'trucks': Truck.objects.all(), 'consignors': Party.objects.filter(party_type='CONSIGNOR'), 'consignees': Party.objects.filter(party_type='CONSIGNEE'),
               'modes': TransactionMode.objects.all()}
    return render(request, 'bill_form.html', context)


def consignment_slip(request, consignment_id):
    consignment = Consignment.objects.get(id=consignment_id)
    context = {'consignment': consignment}
    return render(request, 'bill.html', context)


def consignment_history(request):
    consignments = Consignment.objects.all()
    current_date = date.today().isoformat() 
    days_before = (date.today()-timedelta(days=30)).isoformat()
    if request.method == 'POST':
        try:
            consignments = consignments.filter(date__lte=request.POST.get("to"))
        except:
            pass
        try:
            consignments = consignments.filter(date__gte=request.POST.get("from"))
        except:
            pass
    else : 
        consignments = consignments.filter(date__gte=days_before, date__lte=current_date).order_by('-date')
    context = {'consignments': consignments}
    return render(request, "consignment_history.html", context)


def trip(request, consignment_id):
    consignment = Consignment.objects.get(id=consignment_id)
    modes = TransactionMode.objects.all()
    if request.method == "POST":
        create_trip(request.POST)
        return redirect('consignment_info', consignment_id)
    context = {
        'trucks': Truck.objects.all(),
        'truckers': Party.objects.filter(party_type='TRUCKER'),
        'consignment': consignment,
        'modes': modes
    }
    return render(request, "trip.html", context)


def trip_slip(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    transactions = TripTransaction.objects.filter(trip=trip)
    context = {'trip': trip, 'transactions': transactions}
    return render(request, 'trip_slip.html', context)



def trip_history(request):
    trips = Trip.objects.all()
    current_date = date.today().isoformat() 
    days_before = (date.today()-timedelta(days=30)).isoformat()
    if request.method == 'POST':
        try:
            trips = trips.filter(date__lte=request.POST.get("to"))
        except:
            pass
        try:
            trips = trips.filter(date__gte=request.POST.get("from"))
        except:
            pass
    else : 
        trips = trips.filter(date__gte=days_before, date__lte=current_date).order_by('-date')
    context = {"trips": trips}
    return render(request, "trip_history.html", context)


def consignment_info(request, consignment_id):
    consignment = Consignment.objects.get(id=consignment_id)
    trips = Trip.objects.filter(consignment=consignment)
    context = {'consignment': consignment, 'trips': trips}
    return render(request, 'consignment_info.html', context)

def trip_info(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    transactions = TripTransaction.objects.filter(trip=trip)
    context = {'trips': trip, 'transactions': transactions}
    return render(request, 'trip_info.html', context)


def truck_history(request, truck_number):
    truck = Truck.objects.get(truck_number=truck_number)
    trips = Trip.objects.filter(truck=truck)
    consignments = Consignment.objects.filter(truck=truck)
    context = {'trips': trips, 'consignments': consignments, 'truck': truck}
    return render(request, 'truck_history.html', context)


def trip_end(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    consignment = trip.consignment
    if request.method == 'POST':
        date_end = request.POST['date_end']
        weight_received = request.POST['weight_received']
        freight = request.POST['freight']
        loss = float(trip.freight) - float(freight)

        trip.status = True
        trip.freight = freight
        trip.loss = loss
        trip.date_end = date_end
        trip.weight = weight_received
        trip.remaining_payment = float(trip.remaining_payment) -loss
        trip.save()

        trips = Trip.objects.filter(consignment=consignment)
        trips_status_true = trips.filter(status=True)

        if(trips.count() == trips_status_true.count()):
            consignment.status = True
            consignment.save()

    context = {
        'consignment': consignment,
        'trip': trip
    }
    return render(request, 'end_trip.html', context)