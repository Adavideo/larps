from .models import BusStop, Accomodation


def process_options(options_list):
    processed_options = []
    try:
        len(options_list)
    except:
        options_list = []
    for option in options_list:
        processed_options.append((option.name, option.name))
    return processed_options

def get_bus_stops(larp):
    bus_stops = BusStop.objects.filter(larp=larp)
    bus_options = process_options(bus_stops)
    return bus_options

def get_accomodations(larp):
    accomodations = Accomodation.objects.filter(larp=larp)
    accomodation_options = process_options(accomodations)
    return accomodation_options

def boolean_choices():
    choices = [(True, "Yes"), (False, "No")]
    return choices

def gender_choices():
    choices = [("female", "female"), ("male", "male")]
    return choices
