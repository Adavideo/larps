import csv, io
from django.contrib.auth.models import User
from .models import *
from config import *

# CREATE ELEMENTS (USERS, CHARACTERS...) BASED ON CSV INFORMATION

# Checks if the string provided is empty or only blank spaces
def empty(name):
    return not name.strip()

def get_larp(larp_name):
    larp_search = Larp.objects.filter(name=larp_name)
    if larp_search:
        return larp_search[0]
    else:
        larp = Larp(name=larp_name)
        larp.save()
        return larp

def get_group(group_name, larp_name):
    if empty(larp_name) or empty(group_name):
        return None
    larp = get_larp(larp_name)
    search = Group.objects.filter(name=group_name, larp=larp)
    if search:
        return search[0]
    else:
        group = Group(name=group_name, larp=larp)
        group.save()
        return group

def create_user(player_name, email):
    if empty(player_name): return None

    name_parts = player_name.split(' ')
    username = "_".join(name_parts)
    first_name = name_parts[0]
    last_name = " ".join(name_parts[1:])

    user, created = User.objects.update_or_create(username=username)
    user.first_name = first_name
    user.last_name = last_name
    user.email = email
    user.save()
    return user


def create_character(larp_name, character_name, group, race, rank, type, concept, sheet, weapon):
    if empty(character_name) and empty(group) and empty(race):
        return None

    group = get_group(group, larp_name)
    race, created = Race.objects.update_or_create(name=race)
    type, created = CharacterType.objects.update_or_create(name=type)

    character, created = Character.objects.update_or_create(name=character_name)
    # TODO: When we include the field larp in the Character class, we should
    # search for a character in a concrete larp with that name.
    # This way we'll aloud to have characters with the same name in diferent larps.  
    # character, created = Character.objects.update_or_create(name=character_name, larp=larp)
    character.update(group=group, race=race, rank=rank, type=type, concept=concept, sheet=sheet, weapon=weapon)
    character.save()
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

def process_character_info(column):
    # larp;run;email;name;character;group;race;rank;type;concept;sheet;weapon
    larp = column[0]
    run = column[1]
    email = column[2]
    player_name = column[3]
    character_name = column[4]
    group = column[5]
    race = column[6]
    rank = column[7]
    type = column[8]
    concept = column[9]
    sheet = column[10]
    weapon = column[11]

    user = create_user(player_name, email)
    character = create_character(larp, character_name, group, race, rank,
                                type, concept, sheet, weapon)

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

def create_uniform(uniform_name):
    uniform, created = Uniform.objects.update_or_create(name=uniform_name)
    return uniform

def process_size_info(column):
    # uniform_name	gender	american_size	european_size	chest_min	chest_max	arm_min	arm_max	waist_min	waist_max	shoulder_ min	shoulder_max	torso_min	torso_max	body_min	body_max
    size_information = {}
    size_information["gender"] = column[1]
    size_information["american_size"] = column[2]
    size_information["european_size"] = column[3]
    size_information["chest_min"] = column[4]
    size_information["chest_max"] = column[5]
    size_information["arm_min"] = column[6]
    size_information["arm_max"] = column[7]
    size_information["waist_min"] = column[8]
    size_information["waist_max"] = column[9]
    return size_information

def process_uniform_info(column):
    # uniform_name;gender;american_size;european_size;chest_min;chest_max;arm_min;arm_max;waist_min;waist_max;shoulder_ min;shoulder_max;torso_min;torso_max;body_min;body_max
    uniform_name = column[0]
    uniform = create_uniform(uniform_name)
    if uniform:
        size_information = process_size_info(column)
        size = uniform.add_size(size_information)
        result = str(uniform) + " - " + str(size)
    else:
        result = "Uniform info NOT PROCESSED. " + str(column)
    return result

def process_csv_line(column, file_type):
    file_types_list = csv_file_types()
    if file_type == file_types_list[0][0]:
        result = process_character_info(column)
    elif file_type == file_types_list[1][0]:
        result = process_uniform_info(column)
    else:
        result = "File type "+ str(file_type) + " not recognised"
    return result

def get_file_type(header):
    file_type = "incorrect"
    file_headers = get_file_headers()
    for f in file_headers:
        if f["header"] in header:
            file_type = f["file_type"]
    return file_type

def process_data(data_set):
    io_string = io.StringIO(data_set)
    header = next(io_string)
    file_type = get_file_type(header)
    if file_type == "incorrect":
        return ["Incorrect file type"]

    result = []
    for column in csv.reader(io_string, delimiter=';', quotechar="|"):
        r = process_csv_line(column, file_type)
        result.append(r)
    return result

def read_csv_file(file):
    data_set = file.read().decode('UTF-8')
    return data_set

def process_csv(file):
    data_set = read_csv_file(file)
    result = process_data(data_set)
    return result
