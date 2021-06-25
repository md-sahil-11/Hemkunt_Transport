from django.core.validators import EMPTY_VALUES
from finance.models import Party
from django.http.response import JsonResponse


def get_party(request):
    gstin = request.GET.get("gstin")
    party_type = request.GET.get("party_type")
    if gstin in EMPTY_VALUES or party_type in EMPTY_VALUES:
        # TODO -> return unsuccessful JsonResponse
        return JsonResponse({"success": False}, status=400)
    try:
        party_obj = Party.objects.get(
            gstin=gstin.upper(), party_type=party_type.upper()
        )
    except:
        return JsonResponse({"result": "Does not exist", "success": False}, status=404)

    party = {
        "id": party_obj.id,
        "name": party_obj.name,
        "gstin": party_obj.gstin,
        "address": party_obj.address,
        "party_type": party_obj.party_type,
        "balance": party_obj.balance,
    }
    response = {"result": party, "success": True}
    return JsonResponse(response, status=200)
