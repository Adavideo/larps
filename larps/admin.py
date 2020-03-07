from django.contrib import admin
from .models import Larp, Group, Bookings, Player, Character, CharacterAssigment, DietaryRestriction, Accomodation, Race, BusStop

admin.site.register(Larp)
admin.site.register(Group)
admin.site.register(Player)
admin.site.register(Character)
admin.site.register(CharacterAssigment)
admin.site.register(Bookings)
admin.site.register(DietaryRestriction)
admin.site.register(Accomodation)
admin.site.register(Race)
admin.site.register(BusStop)
