import csv, io
from django.contrib.auth.models import User
from .models import Character, Player, CharacterAssigment, Group, Larp, Race

def create_user(player_name):
    user = None
    name_parts = player_name.split(' ')
    username = "_".join(name_parts)
    if not username == "" or username == " ":
        first_name = name_parts[0]
        last_name = " ".join(name_parts[1:])
        user, created = User.objects.update_or_create(
            username=username,
            first_name=first_name,
            last_name=last_name
        )
    return user

def create_character(larp_name, character_name, character_group, character_race):
    larp, created = Larp.objects.update_or_create(name=larp_name)
    group, created = Group.objects.update_or_create(name=character_group, larp=larp)
    race, created = Race.objects.update_or_create(name=character_race)

    character, created = Character.objects.update_or_create(
        name=character_name,
        group=group,
        race=race
    )
    return character

def assign_character_to_user(user, character, run):
    _, created = CharacterAssigment.objects.update_or_create(
        run = run,
        character=character,
        user=user
    )
    if created:
        print("Character "+ character.name + " assigned to " + user.firstname + " " + user.last_name)


def process_csv_line(column):
    # run	player	character	group	planet	rank
    larp_name = "Mission Together"
    run = column[0]
    player_name = column[1]
    character_name = column[2]
    character_group = column[3]
    character_race = column[4]

    user = create_user(player_name)
    character = create_character(larp_name, character_name, character_group, character_race)

    if user:
        assign_character_to_user(user, character, run)


def process_csv(csv_file):
    # let's check if it is a csv file
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'THIS IS NOT A CSV FILE')
    data_set = csv_file.read().decode('UTF-8')

    # setup a stream which is when we loop through each line we are able to handle a data in a stream
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        process_csv_line(column)
