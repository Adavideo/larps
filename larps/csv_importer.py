import csv, io
from django.contrib.auth.models import User
from .models import Character, Player, CharacterAssigment, Group, Larp, Race


# CREATE ELEMENTS (USERS, CHARACTERS...) BASED ON CSV INFORMATION

# Checks if the string provided is empty or only blank spaces
def empty(name):
    return not name.strip()


def create_user(player_name):
    if empty(player_name):
        return None

    name_parts = player_name.split(' ')
    username = "_".join(name_parts)
    first_name = name_parts[0]
    last_name = " ".join(name_parts[1:])

    user, created = User.objects.update_or_create(
        username=username,
        first_name=first_name,
        last_name=last_name
    )
    return user


def create_character(larp_name, character_name, character_group, character_race):
    if empty(character_name) and empty(character_group) and empty(character_race):
        return None

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
        result = "Character "+ character.name + " assigned to " + user.first_name + " " + user.last_name
    else:
        result = "Not assigned."
    return result


# PROCESS CSV FILE

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

    if user and character:
        result = assign_character_to_user(user, character, run)
    else:
        if not user:
            result = "User invalid"
        else:
            result = "Created user " + user.first_name + " " + user.last_name
        if not character:
            result += ". Character invalid"
    return result

def process_data(data_set):
    result = []
    # setup a stream which is when we loop through each line we are able to handle a data in a stream
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        r = process_csv_line(column)
        result.append(r)
    return result

def read_csv_file(file):
    data_set = file.read().decode('UTF-8')
    return data_set

def process_csv(file):
    data_set = read_csv_file(file)
    process_data(data_set)
