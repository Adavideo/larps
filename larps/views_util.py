from .models import *

def build_context(request, larp_id, run):
    larp = Larp.objects.get(id=larp_id)
    context = {'user': request.user, 'larp': larp, 'run':run}
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
