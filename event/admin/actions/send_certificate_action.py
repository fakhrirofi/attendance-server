from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib import messages
from django.utils.safestring import mark_safe
from PIL import Image, ImageFont, ImageDraw
import os

import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

BASE_DIR = settings.BASE_DIR
get_dir = lambda dir: os.path.join(BASE_DIR, dir)

def write_text(draw: ImageDraw, rectang, text, position, size, align="left", fill="#000000", bold=False, align_right=100):
    """
    pos = (x, y)
    size = text size in pixel
    align = 'left', 'center', 'right
    """
    w, h = rectang

    # Text Font
    font =  lambda x: ImageFont.truetype(get_dir('assets/bookman_old_style_bold.ttf'), round(x * 4.1))
    font_bold = lambda x: ImageFont.truetype(get_dir('assets/BOOKOS.TTF'), round(x * 4.1))
    txt = text
    txtf = font_bold(size) if (bold == True) else font(size)

    # Text align
    x, y = position
    txt_posy = y
    txt_length = txtf.getlength(text)
    if align == "left":
        txt_posx = x
    elif align == "center":
        txt_posx = (w / 2) - (txt_length / 2)
    elif align == "right":
        txt_posx = align_right - txt_length

    draw.text(
        (txt_posx, txt_posy),
        txt, fill=fill, font=txtf
    )

def send_certificate_to_mail(presence, cert_url):
    subject = f"YMCC {presence.event.name} Certificate"
    html_message = render_to_string('event/no_reply_certificate.html', {
        'cert_url': cert_url, 'recipient_name' : presence.name, 'event_name' : presence.event.name,
    })
    message = strip_tags(html_message)
    from_email = settings.DEFAULT_FROM_EMAIL
    to = presence.email
    send_mail(
        subject,
        message,
        from_email,
        [to],
        fail_silently=False,
        html_message=html_message
    )

def send_certificate(presence):
    cert_link = get_dir('assets/participant_certificate.jpg')
    cert = Image.open(cert_link)
    width = cert.size[0]
    height = cert.size[1]

    img = Image.new("RGB", (width, height))
    img.paste(cert)
    draw = ImageDraw.Draw(img)
    # write participant name
    write_text(draw, (width, height), presence.name, (0, 830), size=16, align='center', bold=True)
    media_root = settings.MEDIA_ROOT
    if not os.path.exists(os.path.join(media_root, "certificate")):
        os.mkdir(os.path.join(media_root, "certificate"))
    img.save(os.path.join(media_root, f"certificate/{presence.id}_{presence.name}.pdf"))
    img.close()
    cert.close()
    # url that can be accessed by participant
    cert_url = settings.SITE_URL + f"/media/certificate/{presence.id}_{presence.name}.pdf"
    send_certificate_to_mail(presence, cert_url)

def send_certificate_act(self, request, queryset):
    if not request.user.is_staff:
        raise PermissionDenied
    success = []
    failed = []
    for i in range(len(queryset)):
        try:
            send_certificate(queryset[i])
            queryset[i].attendance = True
            queryset[i].save()
            success.append(i)
        except Exception as ex:
            failed.append(i)
            logger.warning(ex)
            logger.warning("Sending Email Error:", queryset[i].email)
    for i in success:
        queryset[i].payment_check = True
        queryset[i].save()

    if len(success) == len(queryset):
        messages.info(request, "Certificate delivery success!")
    else:
        msg = "Certificate Email sending failed for subsequent registrations:<br>"
        for i in failed:
            msg += "• " + queryset[i].name + " | " + queryset[i].institution + " | " + queryset[i].phone_number.as_e164 + " | " + queryset[i].email + "<br>"
        else:
            msg += "Check the user email!"
        messages.error(request, mark_safe(msg))

send_certificate_act.short_description = "Attend & send certificate"