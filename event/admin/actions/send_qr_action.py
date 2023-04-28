from cryptography.fernet import Fernet
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def encrypt(data: str) -> str:
    data = data.encode("utf-8")
    f = Fernet(settings.API_KEY.encode("utf-8"))
    return f.encrypt(data).decode("utf-8")

def send_qr_to_mail(presence, domain):
    subject = f"YMCC {presence.event.name} Registration"
    html_message = render_to_string('event/no_reply.html', {
        'domain': domain, 'enc' : encrypt(str(presence.id))
    })
    message = strip_tags(html_message)
    from_email = "no-reply@ymcc.hmtaupnyk.com"
    to = presence.email
    send_mail(
        subject,
        message,
        from_email,
        [to],
        fail_silently=False,
        html_message=html_message
    )

def verify_registration(self, request, queryset):
    if not request.user.is_staff:
        raise PermissionDenied
    for presence in queryset:
        try:
            send_qr_to_mail(presence, settings.SITE_URL)
            presence.payment_check = True
            presence.save()
        except Exception as ex:
            print(ex)
            print("Sending Email Error:", presence.email)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

verify_registration.short_description = "Approve & send QR code"
