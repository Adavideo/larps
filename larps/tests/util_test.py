from django.contrib.auth.models import User
from larps.models import *
from .examples import example_players_complete, example_characters


# Initialize testing - basic functions

def create_user(player_info=example_players_complete[0]):
    user_search = User.objects.filter(username=player_info["username"])
    if user_search:
        return user_search[0]
    user = User(username=player_info["username"], first_name=player_info["first_name"], last_name=player_info["last_name"])
    user.save()
    return user

def create_player(player_info=example_players_complete[0]):
    user = create_user(player_info)
    player_search = PlayerMeasurement.objects.filter(user=user)
    if player_search:
        return player_search[0]
    player = PlayerMeasurement(user=user, chest=player_info["chest"], waist=player_info["waist"])
    player.save()
    return player

def create_group(group_name="", larp_name = "Mission Together"):
    group_search = Group.objects.filter(name=group_name)
    if group_search:
        return group_search[0]
    larp = Larp(name = larp_name)
    larp.save()
    group = Group(larp=larp, name=group_name)
    group.save()
    return group

def create_character(character_name=example_characters[0], group=None, group_name=""):
    character_search = Character.objects.filter(name=character_name)
    if character_search:
        return character_search[0]
    if not group and group_name:
        group = Group(name=group_name)
    character = Character(name=character_name, group=group)
    character.save()
    return character

def contains_profile_info(player_info):
    return player_info["chest"] or player_info["waist"]

def create_character_assigment(group="", player_info=example_players_complete[0], character_name=example_characters[0], run=1):
    if contains_profile_info(player_info):
        player = create_player(player_info )
        user=player.user
    else:
        user = create_user(player_info)
        user.save()
    character = create_character(character_name, group)
    assigment = CharacterAssigment(user=user, character=character, run=run)
    assigment.save()
    return assigment

def create_characters_assigments(group="", players=example_players_complete, characters=example_characters, run=1):
    assigments = []
    if len(players) > len(characters):
        n = len(characters)
    else:
        n = len(players)
    for i in range(0, n):
        player_info = players[i]
        character_name = characters[i]
        assigment = create_character_assigment(group=group, player_info=player_info, character_name=character_name, run=run)
        assigment.save()
        assigments.append(assigment)
    return assigments


# OTHER util functions

def set_bookings(assigment, booking_info):
    user = assigment.user
    larp = assigment.character.group.larp
    run = assigment.run
    sleeping_bag = booking_info["sleeping_bag"]

    bus = None
    if booking_info["bus"]:
        bus, created = BusStop.objects.update_or_create(name=booking_info["bus"])

    accomodation = None
    if booking_info["accomodation"]:
        accomodation, created = Accomodation.objects.update_or_create(name=booking_info["accomodation"])

    bookings = Bookings( user=user, larp=larp, run=run, bus=bus,
                         sleeping_bag=sleeping_bag, accomodation=accomodation )
    bookings.save()
