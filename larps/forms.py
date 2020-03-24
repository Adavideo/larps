from django import forms
from .models import DietaryRestriction

def get_dietary_options():
    diets = DietaryRestriction.objects.all()
    diet_options = []
    for diet in diets:
        option = (diet.name, diet.name)
        diet_options.append(option)
    return diet_options

class PlayerForm(forms.Form):
    allergies = forms.CharField(max_length=100)
    food_allergies = forms.CharField(max_length=100)
    food_intolerances = forms.CharField(max_length=100)
    medical_conditions = forms.CharField(max_length=100)
    emergency_contact = forms.CharField(max_length=100)
    diets = get_dietary_options()
    dietary_restrictions = forms.ChoiceField(choices=diets)
    shoulder = forms.IntegerField()
    height = forms.IntegerField()
    chest = forms.IntegerField()
    waist = forms.IntegerField()
