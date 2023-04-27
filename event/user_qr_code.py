import qrcode
from cryptography.fernet import Fernet
from django.conf import settings
from io import BytesIO
from PIL import Image
from .models import Presence


def get_encryption(presence: Presence) -> str:
    data = f"{presence.event.id}|{presence.id}"
    key = settings.API_KEY.encode("utf-8")
    f = Fernet(key)
    return f.encrypt(str(data).encode("utf-8"))

def get_qr_code(text: str) -> bytes: 
    # https://www.geeksforgeeks.org/how-to-generate-qr-codes-with-a-custom-logo-using-python/
    Logo_link = 'assets/logo-ymcc.png'
    logo = Image.open(Logo_link)
    basewidth = 100
    # adjust image size
    wpercent = (basewidth/float(logo.size[0]))
    hsize = int((float(logo.size[1])*float(wpercent)))
    logo = logo.resize((basewidth, hsize), Image.LANCZOS)
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

if __name__ == "__main__":
    a = get_qr_code("hello world")
    print(a)