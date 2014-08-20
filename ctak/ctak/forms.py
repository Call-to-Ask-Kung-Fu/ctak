from django.forms import ModelForm
from .models import Index

class IndexForm(ModelForm):
    class Meta:
        model = Index
        exclude = ['owner', 'type']
