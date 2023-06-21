# attendance-server YMCC 2023
The Website server used in Indonesian Mining & Energy Summit Event YMCC 2023 event. The server is used for registration and attendance via the API. The API is accessed using the [Presence Application](https://github.com/fakhrirofi/ymcc_presence).

## Workflow and features
Participants register via the web, then get a QR code directly (free) or via email. This depends on the type of event, which is free or paid. If the event is paid, the registration will be verified by the administrator and the QR code will be sent via email. The email contains a group link and QR code that that participants must bring when entering the event.

Presence is done by scanning the QR code using [Presence Application](https://github.com/fakhrirofi/ymcc_presence). After the QR scan success, the server will send the certificate to the participants automatically by email.
Database management is done using Django Admin, administrators can edit and download data.

## Setup
This server is configured to run on Linux and supports Python 3.8, 3.9, and 3.10.

```
# clone the repo
git clone https://github.com/fakhrirofi/attendance-server.git
cd attendance-server

# create environment (don't forget to add to .gitignore)
python -m venv venv
source venv/bin/activate

# installing requirements
pip install -r requirements.txt
```

Copy the `.envexample` and rename it to `.env`, then edit its contents. `API_KEY` is the key that will be used in API between the application and the server. `ENCRYPTION_KEY` is a key generated using [Fernet](https://cryptography.io/en/latest/fernet/#cryptography.fernet.Fernet). You can get recaptcha key using [google reCAPTCHA](https://www.google.com/recaptcha/admin/create).

For SMTP configuration, I suggest using gmail to minimize spam. The email host password can be obtained following [this tutorial](https://www.febooti.com/products/automation-workshop/tutorials/enable-google-app-passwords-for-smtp.html).

### Running on local
Set `DEBUG` to 1 in .env
```
# migrate database & testing
python manage.py makemigrations event
python manage.py migrate
python manage.py test event

# create super user
python manage.py createsuperuser

# run server
python manage.py runserver
```

Go to http://127.0.0.1:8000/admin to create new event. In debug mode, SMTP will not work, it uses dummy EmailBackend.