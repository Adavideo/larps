from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.conf import settings
from django.urls import reverse
from django.views import generic
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


from .forms import PlayerForm, BookingsForm
from .models import Character, Player, CharacterAssigment, Bookings, Group, DietaryRestriction, Larp


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

def get_player_profile(user):
    profiles = Player.objects.filter(user=user)
    if len(profiles) == 0:
        player = Player(user=user)
    else:
        player = profiles[0]
    return player

@login_required
def player_profile(request):
    player = get_player_profile(request.user)
    if request.method == 'POST':
        form = PlayerForm(request.POST)
        if form.is_valid():
            player.save_profile(form.cleaned_data)
            player_profile_url = '/larps/player/'+ str(player.id)
            return HttpResponseRedirect(player_profile_url)
    else:
        player_data = player.get_data()
        form = PlayerForm(player_data)
    return render(request, 'larps/player_profile.html', {'form': form, 'user': request.user})

def get_assigment_for_larp(user, larp):
    assigment_for_this_larp = None
    character_assigments = CharacterAssigment.objects.filter(user=user)
    for assigment in character_assigments:
        if assigment.larp() == larp:
            assigment_for_this_larp = assigment
    return assigment_for_this_larp

def get_bookings(user, larp):
    assigment_for_this_larp = get_assigment_for_larp(user, larp)
    if not assigment_for_this_larp:
        return None

    bookings_assigned = Bookings.objects.filter(character_assigment=assigment_for_this_larp)
    if len(bookings_assigned) == 0:
        bookings = Bookings(character_assigment=assigment_for_this_larp)
    else:
        bookings = bookings_assigned[0]
    return bookings

@login_required
def manage_bookings(request, larp_id):
    larp = Larp.objects.get(id=larp_id)
    bookings = get_bookings(request.user, larp)
    if not bookings:
        text = "The player doesn't have a character assigned in this larp. <br>"
        user_bookings = Bookings.objects.all()
        larps = []
        for b in user_bookings:
            if b.user() == request.user:
                larp = b.larp()
                larps.append(larp)
                text += larp.name + " - " + str(larp.id)
        return HttpResponse(text)
    if request.method == 'POST':
        form = BookingsForm(request.POST)
        if form.is_valid():
            bookings.save_bookings(form.cleaned_data)
            return HttpResponseRedirect('/larps/bookings')
    else:
        bookings_data = bookings.get_data()
        form = BookingsForm(bookings_data)
    return render(request, 'larps/bookings_form.html', {'form': form, 'user': request.user, 'larp': larp })

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/accounts/login/')

@login_required
def home_view(request):
    return render(request, 'larps/home.html', {'user': request.user})
