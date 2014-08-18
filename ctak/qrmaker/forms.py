from django.forms import ModelForm
from .models import QR

class QRForm(ModelForm):
    class Meta:
        model = QR
        exclude = ['qrmaked', 'thumb']
