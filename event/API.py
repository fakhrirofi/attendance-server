from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .user_qr_code import decrypt
from .models import Presence, attend, get_events, get_event_presence

def is_valid(request):
    api_key = request.POST.get("API_KEY", "")
    return settings.API_KEY == api_key

def authentication_error(request):
    return JsonResponse({
        "status_code"    : 401,
        "message"   : "authentication error"
    }, status=401)

def api_attend(request):
    # this will return 404 if the presence_id not found
    if not is_valid(request):
        return authentication_error(request)

    enc = request.POST.get("enc", "")
    presence_id = decrypt(enc)
    event_id = int(request.POST.get("event_id", "0"))

    # check qr code validation
    if presence_id == "invalid":
        return JsonResponse({
            "status_code"    : 400,
            "message"   : "qr_code"
        }, status=400)

    # check qr code for the selected event
    presence = get_object_or_404(Presence, pk=int(presence_id))
    if presence.event.id != event_id:
        return JsonResponse({
            "status_code"    : 400,
            "message"   : "different_event"
        }, status=400)

    # check payment of the registration
    attend_data = attend(int(presence_id))
    if attend_data["status"] != "success":
        return JsonResponse({
            "status_code"    : 400,
            "message"   : "payment_check"
        }, status=400)
    
    return JsonResponse(attend_data, status=200)

def api_get_events(request):
    if not is_valid(request):
        return authentication_error(request)
    data = get_events()
    return JsonResponse(data, safe=False)

def api_get_event_presence(request):
    # return 404 if event_id not found
    if not is_valid(request):
        return authentication_error(request)
    
    event_id = int(request.POST.get("event_id", "0"))
    data = get_event_presence(event_id)
    return JsonResponse(data, safe=False)

@csrf_exempt
def api_handler(request, api_type):
    if api_type == "attend":
        return api_attend(request)
    elif api_type == "get_events":
        return api_get_events(request)
    # disable access for security purposes. not used in production
    # elif api_type == "get_event_presence":
    #     return api_get_event_presence(request)
    else:
        return JsonResponse({
            "status_code"      : 404,
            "message"   : "not found"
        }, status=404)