from django import forms
from .forms_util import get_bus_stops, get_accomodations, boolean_choices


class PlayerForm(forms.Form):
    gender = forms.CharField(max_length=100)
    shoulder = forms.IntegerField(help_text='in cm')
    height = forms.IntegerField(help_text='in cm')
    chest = forms.IntegerField(help_text='in cm')
    waist = forms.IntegerField(help_text='in cm')

class BookingsForm(forms.Form):
    weapon = forms.ChoiceField(choices=boolean_choices())
    bus = forms.ChoiceField(choices=get_bus_stops())
    accomodation = forms.ChoiceField(choices=get_accomodations())
    sleeping_bag = forms.ChoiceField(choices=boolean_choices(), help_text="price 23€")
    comments = forms.CharField(max_length=200, required=False)

class ImportCSVForm(forms.Form):
    file = forms.FileField()
