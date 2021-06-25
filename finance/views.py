from django.shortcuts import render
from finance.models import Party, Transaction

def ledger(request, party_id):
    party = Party.objects.get(id=party_id)
    transactions = Transaction.objects.filter(party=party).order_by('date')
    s = 0
    for t in transactions:
        s = s+t.value
        t.running_balance = s
    from_date = transactions[0].date
    to_date = transactions[transactions.count()-1].date
    context = {"party": party, "transactions": transactions, "from_date": from_date, "to_date": to_date}
    return render(request, "ledger.html", context)


def consignors(request):
    consignors = Party.objects.filter(party_type='CONSIGNOR')
    context = {"parties": consignors}
    return render(request, 'party_list.html', context)


def truckers(request):
    truckers = Party.objects.filter(party_type='TRUCKER')
    context = {"parties": truckers}
    return render(request, 'party_list.html', context)