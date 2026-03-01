from django import forms
from .models import Alternativa

class AlternativaForm(forms.ModelForm):
    class Meta:
        model = Alternativa
        fields = ['texto_alternativa']
        labels = {
            'texto_alternativa': 'Descrição da Alternativa'
        }
        widgets = {
            'texto_alternativa': forms.TextInput(attrs={'class': 'form-control'})
        }