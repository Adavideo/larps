from django import forms
from .forms_util import get_diets, get_bus_stops, get_accomodations, boolean_choices


class PlayerForm(forms.Form):
    gender = forms.CharField(max_length=100)
    allergies = forms.CharField(max_length=100)
    food_allergies = forms.CharField(max_length=100)
    food_intolerances = forms.CharField(max_length=100)
    medical_conditions = forms.CharField(max_length=100)
    emergency_contact = forms.CharField(max_length=100)
    dietary_restrictions = forms.ChoiceField(choices=get_diets())
    comments = forms.CharField(max_length=200)
    shoulder = forms.IntegerField()
    height = forms.IntegerField()
    chest = forms.IntegerField()
    waist = forms.IntegerField()

class BookingsForm(forms.Form):
    weapon = forms.ChoiceField(choices=boolean_choices())
    bus = forms.ChoiceField(choices=get_bus_stops())
    accomodation = forms.ChoiceField(choices=get_accomodations())
    sleeping_bag = forms.ChoiceField(choices=boolean_choices())
    comments = forms.CharField(max_length=200)

class ImportCSVForm(forms.Form):
    file = forms.FileField()
