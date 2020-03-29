from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.conf import settings
from django.urls import reverse
from django.views import generic
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages


from .forms import *
from .models import *
from .csv_importer import process_csv
from .config import csv_file_types


# HOME AND LOGOUT

def home_view(request):
    return render(request, 'larps/home.html', {'user': request.user})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/accounts/login/')


# CHARACTERS

class CharacterView(generic.DetailView):
    model = Character

class CharactersListView(generic.ListView):
    def get_queryset(self):
        return Character.objects.all()


# PLAYERS

class PlayersListView(generic.ListView):
    def get_queryset(self):
        return Player.objects.all()

def get_player_profile(user):
    profiles = Player.objects.filter(user=user)
    if len(profiles) == 0:
        player = Player(user=user)
    else:
        player = profiles[0]
    return player

def player_profile_view(request):
    player = get_player_profile(request.user)
    if request.method == 'POST':
        form = PlayerForm(request.POST)
        if form.is_valid():
            player.save_profile(form.cleaned_data)
            url = '/larps/'
            return HttpResponseRedirect(url)
    else:
        player_data = player.get_data()
        form = PlayerForm(player_data)
    return render(request, 'larps/player_profile.html', {'form': form, 'user': request.user})


# BOOKINGS

class BookingsView(generic.DetailView):
    model = Bookings

class BookingsListView(generic.ListView):
    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            user_bookings = Bookings.objects.none()
        else:
            user_bookings = Bookings.objects.filter(user=user)
        return user_bookings

def get_bookings(user, larp, run):
    bookings_list = Bookings.objects.filter(user=user, larp=larp, run=run)
    if len(bookings_list) == 0:
        return None
    else:
        bookings = bookings_list[0]
    return bookings

def manage_bookings_view(request, larp_id, run):
    larp = Larp.objects.get(id=larp_id)

    bookings = get_bookings(request.user, larp, run)
    if not bookings:
        return HttpResponseRedirect('/larps/bookings')

    if request.method == 'POST':
        form = BookingsForm(request.POST)
        if form.is_valid():
            bookings.save_bookings(form.cleaned_data)
            url = '/larps/bookings/'+ str(bookings.id)
            return HttpResponseRedirect(url)
    else:
        bookings_data = bookings.get_data()
        form = BookingsForm(bookings_data)
    return render(request, 'larps/bookings_form.html', {'form': form, 'user': request.user, 'larp': larp, 'run': run })


# CSV IMPORTER

def get_context_info():
    characters = Character.objects.all()
    players = User.objects.all()
    assigments = CharacterAssigment.objects.all()
    context = {
                'characters': characters,
                'players': players,
                'assigments' : assigments
              }
    return context


def file_upload_index_view(request):
    template = "csv_import/csv_index.html"
    file_types = csv_file_types()
    context = {'user': request.user, 'file_types': file_types}
    return render(request, template, context)


def file_upload_view(request, file_type_number):
    template = "csv_import/file_upload.html"
    file_type = csv_file_types()[file_type_number][0]
    form = ImportCSVForm()
    context = {'form': form, 'user': request.user, 'file_type':file_type}

    if request.method == "POST":
        file = request.FILES['file']
        result = process_csv(file, file_type)
        context["result"] = result

    return render(request, template, context)



# UNIFORMS

def uniforms_view(request):
    template = "larps/uniforms.html"
    uniforms = Uniform.objects.all()
    context = {"uniforms": uniforms}
    return render(request, template, context)

def uniform_sizes_view(request, uniform_id):
    template = "larps/uniforms.html"
    uniforms = Uniform.objects.all()
    group = Uniform.objects.get(id=uniform_id).group
    players_profiles = group.get_player_profiles()
    sizes = UniformSize.objects.filter(uniform=uniform_id)
    context = {"uniforms": uniforms, "sizes": sizes, "players": players_profiles}
    return render(request, template, context)
