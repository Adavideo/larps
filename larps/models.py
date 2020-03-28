from django.db import models
from django.contrib.auth.models import User


# PLAYER PROFILES

class DietaryRestriction(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Player(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    allergies = models.CharField(max_length=200, blank=True)
    food_allergies = models.CharField(max_length=200, blank=True)
    food_intolerances = models.CharField(max_length=200, blank=True)
    medical_conditions = models.CharField(max_length=200, blank=True)
    emergency_contact = models.CharField(max_length=200, blank=True)
    dietary_restrictions = models.ForeignKey(DietaryRestriction, on_delete=models.SET_NULL, null=True, blank=True)
    comments = models.CharField(max_length=200, default="no", blank=True, null=True)
    shoulder = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    chest = models.IntegerField(default=0)
    waist = models.IntegerField(default=0)

    def __str__(self):
        if (self.user.first_name):
            name = self.user.first_name + " " + self.user.last_name
        else:
            name = self.user.username
        return name

    def get_data(self):
        if self.dietary_restrictions:
            diet = self.dietary_restrictions.name
        else:
            diet = "none"
        data = {
            'allergies': self.allergies,
            'food_allergies' : self.food_allergies,
            'food_intolerances': self.food_intolerances,
            'medical_conditions': self.medical_conditions,
            'emergency_contact': self.emergency_contact,
            'dietary_restrictions' : diet,
            'comments' : self.comments,
            'shoulder' : self.shoulder,
            'height' : self.height,
            'chest' : self.chest,
            'waist' : self.waist,
        }
        return data

    def save_profile(self, new_data):
        self.allergies = new_data['allergies']
        self.food_allergies = new_data['food_allergies']
        self.food_intolerances = new_data['food_intolerances']
        self.medical_conditions = new_data['medical_conditions']
        self.emergency_contact = new_data['emergency_contact']
        diet =  new_data['dietary_restrictions']
        self.dietary_restrictions = DietaryRestriction.objects.get(name=diet)
        self.comments = new_data['comments']
        self.shoulder = new_data['shoulder']
        self.height = new_data['height']
        self.chest = new_data['chest']
        self.waist = new_data['waist']
        self.save()


# LARPS AND CHARACTERS

class Larp(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Group(models.Model):
    larp = models.ForeignKey(Larp, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, default="", blank=True)
    weapon = models.CharField(max_length=50, blank=True)
    def __str__(self):
        if self.name:
            return self.larp.name + " - " + self.name
        else:
            return self.larp.name + " - " + "no group"

class Race(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Character(models.Model):
    name = models.CharField(max_length=50)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
    race = models.ForeignKey(Race, on_delete=models.SET_NULL, null=True, blank=True)
    short_concept = models.CharField(max_length=200, blank=True)
    def __str__(self):
        return self.name

class CharacterAssigment(models.Model):
    run = models.IntegerField(default=1)
    character =  models.ForeignKey(Character, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        assigment = ""
        if self.character.group:
            assigment = self.character.group.larp.name + " run " + str(self.run) + " - " + self.character.name
        if self.user:
            assigment += " assigned to " + self.user.first_name + " " + self.user.last_name
        return assigment

    def larp(self):
        return self.character.group.larp


# BOOKINGS

class Accomodation(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class BusStop(models.Model):
    name= models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Bookings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    larp = models.ForeignKey(Larp, on_delete=models.CASCADE)
    run = models.IntegerField(default=1)
    weapon = models.BooleanField(null=True, blank=True)
    bus = models.ForeignKey(BusStop, on_delete=models.SET_NULL, null=True, blank=True)
    accomodation = models.ForeignKey(Accomodation, on_delete=models.SET_NULL, null=True, blank=True)
    sleeping_bag = models.BooleanField(null=True, blank=True)
    comments = models.CharField(max_length=200, default="no", blank=True, null=True)

    def __str__(self):
        text = self.larp.name + " run " + str(self.run)
        text += " - " + self.user.first_name + " " + self.user.last_name
        return text

    def get_data(self):
        data = {
            'weapon': self.weapon,
            'bus' : self.bus,
            'accomodation': self.accomodation,
            'sleeping_bag' : self.sleeping_bag,
            'comments' : self.comments
        }
        return data

    def save_bookings(self, new_data):
        self.weapon = new_data['weapon']
        self.bus = BusStop.objects.get(name=new_data['bus'])
        self.accomodation = Accomodation.objects.get(name=new_data['accomodation'])
        self.sleeping_bag = new_data['sleeping_bag']
        self.comments = new_data['comments']
        self.save()


# UNIFORMS

class Uniform(models.Model):
    name = models.CharField(max_length=200)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
    color = models.CharField(max_length=50)

    def __str__(self):
        if self.group:
            text = self.group.name
        else:
            text = "Group not assigned"
        return text

    def add_size(self, size_information):
        size = UniformSize(uniform=self)
        size.set_values(size_information)
        size.save()
        return size

class UniformSize(models.Model):
    uniform  = models.ForeignKey(Uniform, on_delete=models.CASCADE)
    gender = models.CharField(max_length=50)
    american_size = models.CharField(max_length=10)
    european_size = models.CharField(max_length=10)
    chest_min = models.IntegerField()
    chest_max = models.IntegerField()
    waist_min = models.IntegerField()
    waist_max = models.IntegerField()

    def __str__(self):
        text = self.gender + ". "
        text += str(self.american_size) + "/" + str(self.european_size) +" "
        text += "chest(" + str(self.chest_min) + ","+ str(self.chest_max)+ ") "
        text += "waist(" + str(self.waist_min) + ","+ str(self.waist_max)+ ")"
        return text

    def set_values(self, size_information):
        self.gender = size_information["gender"]
        self.american_size = size_information["american_size"]
        self.european_size = size_information["european_size"]
        self.chest_min = size_information["chest_min"]
        self.chest_max = size_information["chest_max"]
        self.waist_min = size_information["waist_min"]
        self.waist_max = size_information["waist_max"]
