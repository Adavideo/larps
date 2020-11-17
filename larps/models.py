from django.db import models
from django.contrib.auth.models import User


# PLAYER PROFILES

class Player(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=200, blank=True)
    shoulder = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    chest = models.IntegerField(default=0)
    waist = models.IntegerField(default=0)
    sleeve_length = models.IntegerField(default=0)

    def __str__(self):
        if (self.user.first_name):
            name = self.user.first_name + " " + self.user.last_name
        else:
            name = self.user.username
        return name

    def get_data(self):
        data = {
            'gender' : self.gender,
            'shoulder' : self.shoulder,
            'height' : self.height,
            'chest' : self.chest,
            'waist' : self.waist,
            'sleeve_length' : self.sleeve_length,
        }
        return data

    def save_profile(self, new_data):
        self.gender = new_data['gender']
        self.shoulder = new_data['shoulder']
        self.height = new_data['height']
        self.chest = new_data['chest']
        self.waist = new_data['waist']
        self.sleeve_length = new_data['sleeve_length']
        self.save()


# LARPS AND CHARACTERS

class Larp(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

    def get_character_assigments(self):
        groups = Group.objects.filter(larp=self)
        character_assigments = []
        for group in groups:
            assigments = group.get_character_assigments()
            character_assigments.extend(assigments)
        return character_assigments

    def get_number_of_runs(self, assigments=None):
        if not assigments:
            assigments = self.get_character_assigments()
        number_of_runs = 0
        for assigment in assigments:
            if assigment.run > number_of_runs:
                number_of_runs = assigment.run
        return number_of_runs

    def initialize_players_info(self, number_of_runs):
        players_info = [ ]
        for i in range(0, number_of_runs):
            players_info.append([])
        return players_info

    def get_players_information(self):
        assigments = self.get_character_assigments()
        number_of_runs = self.get_number_of_runs(assigments)
        players_info = self.initialize_players_info(number_of_runs)
        for assigment in assigments:
            profile = assigment.get_player_profile()
            bookings = assigment.get_bookings()
            if assigment.user:
                if assigment.user.first_name or assigment.user.last_name:
                    user_name = assigment.user.first_name + " " + assigment.user.last_name
                else:
                    user_name = assigment.user.username
            else:
                user_name = "Not assigned"
            info = { "user": user_name, "profile": profile, "bookings": bookings, "run": assigment.run, "character": assigment.character.name }
            run_index = assigment.run -1
            players_info[run_index].append(info)
        return players_info


class Group(models.Model):
    larp = models.ForeignKey(Larp, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, default="", blank=True)
    weapon = models.CharField(max_length=50, blank=True)

    def __str__(self):
        if self.name:
            return self.larp.name + " - " + self.name
        else:
            return self.larp.name + " - " + "no group"

    # returns the profiles of the players assigned to this group.
    def get_player_profiles(self):
        players = []
        character_assigments = self.get_character_assigments()
        for assigment in character_assigments:
            player_profile = assigment.get_player_profile()
            if player_profile:
                # check that the profile is not already on the list.
                if player_profile not in players:
                    players.append(player_profile)
        return players

    def get_character_assigments(self):
        character_assigments = []
        characters_list = Character.objects.filter(group=self)
        for character in characters_list:
            assigments = CharacterAssigment.objects.filter(character=character)
            character_assigments.extend(assigments)
        return character_assigments

    def character_assigment_for_user(self, user):
        character_assigments = self.get_character_assigments()
        user_assigments = []
        for assigment in character_assigments:
            if assigment.user == user:
                user_assigments.append(assigment)
        return user_assigments


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

    def create_player_profile(self):
        player_profile = Player(user=self.user)
        player_profile.save()
        return player_profile

    def get_player_profile(self):
        if not self.user:
            return None
        player_profiles = Player.objects.filter(user=self.user)
        if player_profiles:
            return player_profiles[0]
        else:
            return self.create_player_profile()

    def get_bookings(self):
        larp = self.character.group.larp
        booking = None
        booking_search = Bookings.objects.filter(user=self.user, larp=larp, run=self.run)
        if booking_search:
            booking = booking_search[0]
        elif self.user:
            booking = Bookings(user=self.user, larp=larp, run=self.run)
            booking.save()
        return booking


# BOOKINGS

class Accomodation(models.Model):
    larp = models.ForeignKey(Larp, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class BusStop(models.Model):
    larp = models.ForeignKey(Larp, null=True, on_delete=models.SET_NULL)
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
        character = self.get_character()
        if character:
            text += ". " + character.name
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

    def get_character(self):
        assigments_search = CharacterAssigment.objects.filter(user=self.user, run=self.run)
        for assigment in assigments_search:
            if assigment.character.group.larp == self.larp:
                return assigment.character
        return None


# UNIFORMS

class Uniform(models.Model):
    name = models.CharField(max_length=200)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        if self.group:
            text = self.group.name
        else:
            text = "Group not assigned"
        return text

    def get_sizes(self):
        return UniformSize.objects.filter(uniform=self)

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

    def recommend_sizes(self, player):
        sizes = self.get_sizes().filter(gender=player.gender)
        if not sizes:
            return None
        perfect_fit = self.find_perfect_fit(sizes, player.chest, player.waist)
        if perfect_fit:
            return perfect_fit
        return self.find_valid_fit(sizes, player.chest, player.waist)

    def get_players_with_recommended_sizes(self):
        players_profiles = self.group.get_player_profiles()
        players_with_sizes = []
        for player in players_profiles:
            sizes = self.recommend_sizes(player=player)
            character_assigments = self.group.character_assigment_for_user(player.user)
            players_with_sizes.append( { "info": player, "sizes": sizes, "character_assigments": character_assigments } )
        return players_with_sizes

    def increment_quantity(self, sizes_with_quantities, size_to_increment):
        for size in sizes_with_quantities:
            if size["name"] == size_to_increment:
                size["quantity"] += 1

    def update_quantities(self, sizes_with_quantities, players_with_sizes):
        for player in players_with_sizes:
            if player["sizes"]:
                player_size = player["sizes"][0].get_name()
                self.increment_quantity(sizes_with_quantities, player_size)

    def initialize_sizes_with_quantities(self):
        sizes_with_quantities = []
        for size in self.get_sizes():
            sizes_with_quantities.append({ "name":size.get_name(), "info": size, "quantity": 0 })
        return sizes_with_quantities

    def get_sizes_with_quantities(self, players_with_sizes):
        sizes_with_quantities = self.initialize_sizes_with_quantities()
        self.update_quantities(sizes_with_quantities, players_with_sizes)
        return sizes_with_quantities


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

    def get_name(self):
        name = self.american_size
        if name and self.european_size:
            name += " / " + self.european_size
        else:
            name = self.european_size
        return name

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
