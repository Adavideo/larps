from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Character, Player, CharacterAssigment, Bookings, Group


class CharacterView(generic.DetailView):
    model = Character

class CharactersListView(generic.ListView):
    def get_queryset(self):
        return Character.objects.all()

class PlayerView(generic.DetailView):
    model = Player

class PlayersListView(generic.ListView):
    def get_queryset(self):
        return Player.objects.all()

class BookingsView(generic.DetailView):
    model = Bookings

class BookingsListView(generic.ListView):
    def get_queryset(self):
        return Bookings.objects.all()
