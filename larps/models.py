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

    def find_perfect_fit(self, sizes, chest, waist):
        perfect_fit = []
        for size in sizes:
            if size.perfect_fit(chest, waist):
                perfect_fit.append(size)
        return perfect_fit

    def find_valid_fit(self, sizes, chest, waist):
        valid_fit = []
        for size in sizes:
            if (size.chest_fit(chest) and size.waist_minimum_fit(waist)):
                valid_fit.append(size)
            elif (size.chest_minimum_fit(chest) and size.waist_fit(waist)):
                valid_fit.append(size)
        if valid_fit:
            return valid_fit
        else:
            return None

    def recommend_sizes(self, chest, waist):
        sizes = UniformSize.objects.filter(uniform=self)
        if not sizes:
            return None

        perfect_fit = self.find_perfect_fit(sizes, chest, waist)
        if perfect_fit:
            return perfect_fit

        return self.find_valid_fit(sizes, chest, waist)

class UniformSize(models.Model):
    uniform = models.ForeignKey(Uniform, on_delete=models.CASCADE)
    gender = models.CharField(max_length=50)
    american_size = models.CharField(max_length=10)
    european_size = models.CharField(max_length=10)
    chest_min = models.IntegerField()
    chest_max = models.IntegerField()
    waist_min = models.IntegerField()
    waist_max = models.IntegerField()

    def __str__(self):
        text = ""
        if self.gender:
            text = self.gender + ". "
        if self.american_size:
            text += str(self.american_size)
            if self.european_size:
                text += "/" + str(self.european_size) +" "
        elif self.european_size:
            str(self.european_size) +" "
        text += "chest(" + str(self.chest_min) + ","+ str(self.chest_max)+ ") "
        text += "waist(" + str(self.waist_min) + ","+ str(self.waist_max)+ ")"
        return text

    def get_measurement(self, size_info, index):
        measurement = size_info[index]
        if not measurement:
            return 0
        return int(measurement)

    def set_values(self, size_info):
        self.gender = size_info["gender"]
        self.american_size = size_info["american_size"]
        self.european_size = size_info["european_size"]
        self.chest_min = self.get_measurement(size_info, "chest_min")
        self.chest_max = self.get_measurement(size_info, "chest_max")
        self.waist_min = self.get_measurement(size_info, "waist_min")
        self.waist_max = self.get_measurement(size_info, "waist_max")

    def perfect_fit(self, chest, waist):
        return self.chest_fit(chest) and self.waist_fit(waist)

    def chest_fit(self, chest):
        return (self.chest_min <= chest and self.chest_max >= chest)

    def chest_minimum_fit(self, chest):
        return self.chest_fit(chest) or self.chest_min >= chest

    def waist_fit(self, waist):
        return (self.waist_min <= waist and self.waist_max >= waist)

    def waist_minimum_fit(self, waist):
        return self.waist_fit(waist) or self.waist_min >= waist
