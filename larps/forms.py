from django import forms

class PlayerForm(forms.Form):
    allergies = forms.CharField(max_length=100)
    food_allergies = forms.CharField(max_length=100)
    food_intolerances = forms.CharField(max_length=100)
    medical_conditions = forms.CharField(max_length=100)
    emergency_contact = forms.CharField(max_length=100)
    shoulder = forms.IntegerField()
    height = forms.IntegerField()
    chest = forms.IntegerField()
    waist = forms.IntegerField()
