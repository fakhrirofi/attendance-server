from cryptography.fernet import Fernet
from django.conf import settings
from django.core.mail import send_mail, send_mass_mail, get_connection, EmailMultiAlternatives
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib import messages
from django.utils.safestring import mark_safe

import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

# not used, maybe in future
def send_mass_html_mail(datatuple, fail_silently=False, user=None, password=None, 
                        connection=None):
    """
    Given a datatuple of (subject, text_content, html_content, from_email,
    recipient_list), sends each message to each recipient list. Returns the
    number of emails sent.

    If from_email is None, the DEFAULT_FROM_EMAIL setting is used.
    If auth_user and auth_password are set, they're used to log in.
    If auth_user is None, the EMAIL_HOST_USER setting is used.
    If auth_password is None, the EMAIL_HOST_PASSWORD setting is used.

    """
    connection = connection or get_connection(
        username=user, password=password, fail_silently=fail_silently)
    messages = []
    for subject, text, html, from_email, recipient in datatuple:
        message = EmailMultiAlternatives(subject, text, from_email, recipient)
        message.attach_alternative(html, 'text/html')
        messages.append(message)
    return connection.send_messages(messages)

def encrypt(data: str) -> str:
    data = data.encode("utf-8")
    f = Fernet(settings.ENCRYPTION_KEY.encode("utf-8"))
    return f.encrypt(data).decode("utf-8")

def send_qr_to_mail(presence, domain):
    subject = f"YMCC {presence.event.name} Registration"
    html_message = render_to_string('event/no_reply.html', {
        'domain': domain, 'enc' : encrypt(str(presence.id)), 'recipient_name' : presence.name,
    })
    message = strip_tags(html_message)
    from_email = f"YMCC {presence.event.name} Registration"
    to = presence.email
    send_mail(
        subject,
        message,
        from_email,
        [to],
        fail_silently=False,
        html_message=html_message
    )
    # return (subject, message, html_message, from_email, [to])
    # print(send_mass_html_mail(((subject, message, html_message, from_email, [to]), (subject, message, html_message, from_email, ["hello@localhosta"])), fail_silently=False))

def verify_registration(self, request, queryset):
    if not request.user.is_staff:
        raise PermissionDenied
    success = []
    failed = []
    for i in range(len(queryset)):
        try:
            send_qr_to_mail(queryset[i], settings.SITE_URL)
            success.append(i)
        except Exception as ex:
            failed.append(i)
            logger.warning(ex)
            logger.warning("Sending Email Error:", queryset[i].email)
    for i in success:
        queryset[i].payment_check = True
        queryset[i].save()

    if len(success) == len(queryset):
        messages.info(request, "Email delivery success!")
    else:
        msg = "Email sending failed for subsequent registrations:<br>"
        for i in failed:
            msg += "• " + queryset[i].name + " | " + queryset[i].institution + " | " + queryset[i].phone_number.as_e164 + " | " + queryset[i].email + "<br>"
        else:
            msg += "Check the user email!"
        messages.error(request, mark_safe(msg))

verify_registration.short_description = "Approve & send QR code"
