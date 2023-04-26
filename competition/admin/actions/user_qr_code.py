import os
import qrcode
import tempfile
import zipfile
from io import BytesIO
from PIL import Image
from django.http import HttpResponse


def get_qr_code(text) -> bytes: 
    # https://www.geeksforgeeks.org/how-to-generate-qr-codes-with-a-custom-logo-using-python/
    Logo_link = 'assets/logo.jpg'
    logo = Image.open(Logo_link)
    basewidth = 100
    # adjust image size
    wpercent = (basewidth/float(logo.size[0]))
    hsize = int((float(logo.size[1])*float(wpercent)))
    logo = logo.resize((basewidth, hsize), Image.ANTIALIAS)
    QRcode = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H
    )
    # generating QR code
    QRcode.add_data(text)
    QRcode.make()
    QRcolor = 'Black'
    QRimg = QRcode.make_image(
        fill_color=QRcolor, back_color="white").convert('RGB')
    # set size of QR code
    pos = ((QRimg.size[0] - logo.size[0]) // 2,
        (QRimg.size[1] - logo.size[1]) // 2)
    QRimg.paste(logo, pos)
    # save the QR code generated
    s = BytesIO()
    QRimg.save(s, "jpeg")
    QRimg.close()
    return s.getvalue()

def download_qr_code(self, request, queryset):
    with tempfile.SpooledTemporaryFile() as tmp:
        with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as archive:
            for user in queryset:
                text = f"{str(user.id).zfill(3)}|{user.name}"
                qr_bytes = get_qr_code(text)
                archive.writestr(text + ".jpg", qr_bytes)
        tmp.seek(0)
        response = HttpResponse(content=tmp.read(), content_type='application/x-zip-compressed')
        response['Content-Disposition'] = 'attachment; filename="USER QRCODE.zip"'
        return response
download_qr_code.short_description = "Download QR code"
