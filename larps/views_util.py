from .models import *

def find_character(user, larp, run):
    assigments = larp.get_character_assigments()
    for a in assigments:
        if (a.user == user) and (a.run == run):
            return a.character

def build_context(request, larp_id, run):
    larp = Larp.objects.get(id=larp_id)
    character = find_character(request.user, larp, run)
    context = {
        'user': request.user,
        'larp': larp, 'run':run,
        'character': character }
    return context


def get_measurements(user):
    measurements_search = PlayerMeasurement.objects.filter(user=user)
    if len(measurements_search) == 0:
        measurements = PlayerMeasurement(user=user)
    else:
        measurements = measurements_search[0]
    return measurements

# BOOKINGS

def generate_bookings(user):
    assigments = CharacterAssigment.objects.filter(user=user)
    for assigment in assigments:
        booking = assigment.get_bookings()

def get_bookings(user, larp, run):
    bookings_list = Bookings.objects.filter(user=user, larp=larp, run=run)
    if len(bookings_list) == 0: return None
    return bookings_list[0]


# CHARACTERS

def get_characters(larp):
    larp_characters = []
    for character in Character.objects.all():
        if character.group.larp == larp:
            larp_characters.append(character)
    return larp_characters
