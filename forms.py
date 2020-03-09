from django import forms

class skladka01(forms.Form):
    idSkladkaRoczna = forms.IntegerField(widget=forms.HiddenInput())
    email = forms.EmailField(label='Email')
    kwota = forms.DecimalField(label='Kwota', min_value=0.01,decimal_places=2)
    class NewMeta:
        readonly = ('idSkladkaRoczna',)

