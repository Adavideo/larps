from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.conf import settings
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required

from .forms import PlayerForm
from .models import Character, Player, CharacterAssigment, Bookings, Group, DietaryRestriction


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

class ProfileView(generic.DetailView):
    model = Player

class BookingsView(generic.DetailView):
    model = Bookings

class BookingsListView(generic.ListView):
    def get_queryset(self):
        return Bookings.objects.all()

def get_user_profile():
    player = Player.objects.all()[0]
    return player

@login_required
def player_profile(request):
    print("Autenticado")
    if request.method == 'POST':
        form = PlayerForm(request.POST)
        if form.is_valid():
            player = get_user_profile()
            player.save_profile(form.cleaned_data)
            return HttpResponseRedirect('/larps/players')
    else:
        player_data = get_user_profile().get_data()
        form = PlayerForm(player_data)
    return render(request, 'larps/player_profile.html', {'form': form})
