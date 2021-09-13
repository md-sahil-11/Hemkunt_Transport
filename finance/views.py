from finance.services import Payment, Receipt
from finance.models import Party, Transaction, TransactionMode
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def ledger(request, party_id):
    party = Party.objects.get(id=party_id)
    transactions = Transaction.objects.filter(party=party).order_by("date")
    from_date = None
    to_date = None
    s = 0
    for t in transactions:
        s += t.value
        t.running_balance = s
    context = {
        "party": party,
        "transactions": transactions,
        "from_date": from_date,
        "to_date": to_date,
    }
    return render(request, "ledger.html", context)


def render_party_html(request, party_type):
    parties = Party.objects.filter(party_type=party_type.upper())
    context = {"parties": parties}
    return render(request, "party_list.html", context)


@login_required
def consignors(request):
    return render_party_html(request, "CONSIGNOR")


@login_required
def truckers(request):
    return render_party_html(request, "TRUCKER")


@login_required
def consignees(request):
    return render_party_html(request, "CONSIGNEE")


def render_transaction_html(request, template_name):
    parties = Party.objects.all()
    modes = TransactionMode.objects.all()
    context = {"parties": parties, "modes": modes}
    return render(request, template_name, context=context)


@login_required
def payment_view(request):
    if request.method == "POST":
        payment = Payment(request.POST)
        payment.create()
    return render_transaction_html(request, "payment.html")


@login_required
def receipt_view(request):
    if request.method == "POST":
        receipt = Receipt(request.POST)
        receipt.create()
    return render_transaction_html(request, "receipt.html")
