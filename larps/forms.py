from django import forms
from .models import DietaryRestriction, BusStop, Accomodation

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
    comments = forms.CharField(max_length=200)
    shoulder = forms.IntegerField()
    height = forms.IntegerField()
    chest = forms.IntegerField()
    waist = forms.IntegerField()

def boolean_choices():
    choices = [(True, "Yes"), (False, "No")]
    return choices

class BookingsForm(forms.Form):
    weapon = forms.ChoiceField(choices=boolean_choices())
    bus_options = process_options(BusStop.objects.all())
    bus = forms.ChoiceField(choices=bus_options)
    accomodation_options = process_options(Accomodation.objects.all())
    accomodation = forms.ChoiceField(choices=accomodation_options)
    sleeping_bag = forms.ChoiceField(choices=boolean_choices())
    comments = forms.CharField(max_length=200)
