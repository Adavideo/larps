from django import forms
from .models import DietaryRestriction, BusStop

def process_options(options_list):
    processed_options = []
    for option in options_list:
        processed_options.append((option.name, option.name))
    return processed_options

class PlayerForm(forms.Form):
    allergies = forms.CharField(max_length=100)
    food_allergies = forms.CharField(max_length=100)
    food_intolerances = forms.CharField(max_length=100)
    medical_conditions = forms.CharField(max_length=100)
    emergency_contact = forms.CharField(max_length=100)
    diets = process_options(DietaryRestriction.objects.all())
    dietary_restrictions = forms.ChoiceField(choices=diets)
    shoulder = forms.IntegerField()
    height = forms.IntegerField()
    chest = forms.IntegerField()
    waist = forms.IntegerField()

def get_weapon_choices():
    choices = [(True, "Yes"), (False, "No")]
    return choices

class BookingsForm(forms.Form):
    weapon = forms.ChoiceField(choices=get_weapon_choices())
    bus_options = process_options(BusStop.objects.all())
    bus = forms.ChoiceField(choices=bus_options)
    #accomodation
