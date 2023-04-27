from django import forms
from .models import Presence
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Presence
        fields = ["name", "email", "institution", "phone_number", "proof_payment"]
    
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self ).__init__(*args, **kwargs)
        self.fields['captcha'] = ReCaptchaField(widget=ReCaptchaV2Checkbox)

# STATES = (
#     ('', 'Choose...'),
#     ('MG', 'Minas Gerais'),
#     ('SP', 'Sao Paulo'),
#     ('RJ', 'Rio de Janeiro')
# )

# class RegistrationForm(forms.Form):
#     name = forms.CharField(max_length=50)
#     institution = forms.CharField(max_length=50)
#     email = forms.EmailField()
#     phone_number = PhoneNumberField(label="Phone number (WhatsApp)")
#     proof_payment = forms.FileField(label="Proof of payment")
    # address_1 = forms.CharField(
    #     label='Address',
    #     widget=forms.TextInput(attrs={'placeholder': '1234 Main St'})
    # )
    # address_2 = forms.CharField(
    #     widget=forms.TextInput(attrs={'placeholder': 'Apartment, studio, or floor'})
    # )
    # city = forms.CharField()
    # state = forms.ChoiceField(choices=STATES)
    # zip_code = forms.CharField(label='Zip')
    # check_me_out = forms.BooleanField(required=False)