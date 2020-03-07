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
    height = models.IntegerField(default=0)
    chest = models.IntegerField(default=0)
    waist = models.IntegerField(default=0)
    def __str__(self):
        if (self.user.first_name):
            name = self.user.first_name + " " + self.user.last_name
        else:
            name = self.user.username
        return name


# LARPS AND CHARACTERS

class Larp(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Group(models.Model):
    larp = models.ForeignKey(Larp, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, default="", blank=True)
    uniform = models.CharField(max_length=50, blank=True)
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
    character_assigment = models.ForeignKey(CharacterAssigment, on_delete=models.CASCADE)
    weapon = models.CharField(max_length=50, blank=True)
    uniform = models.CharField(max_length=50, blank=True)
    bus = models.ForeignKey(BusStop, on_delete=models.SET_NULL, null=True, blank=True)
    accomodation = models.ForeignKey(Accomodation, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return str(self.character_assigment)
