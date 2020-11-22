from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.conf import settings
from django.urls import reverse
from django.views import generic
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import *
from .models import *
from .csv_importer import process_csv
from config import csv_file_types



def not_allowed_view(request):
    template = "larps/not_allowed.html"
    context = {}
    return render(request, template, context)


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

def get_measurements(user):
    measurements_search = PlayerMeasurement.objects.filter(user=user)
    if len(measurements_search) == 0:
        measurements = PlayerMeasurement(user=user)
    else:
        measurements = measurements_search[0]
    return measurements

def measurements_form_view(request):
    template = 'larps/measurements_form.html'
    context = {'user': request.user}
    measurements = get_measurements(request.user)
    if request.method == 'POST':
        form = MeasurementsForm(request.POST)
        if form.is_valid():
            measurements.save_profile(form.cleaned_data)
            url = reverse('larps:home')
            return HttpResponseRedirect(url)
    else:
        data = measurements.get_data()
        context["form"] = MeasurementsForm(data)
    return render(request, template, context)


# BOOKINGS

def generate_bookings(user):
    assigments = CharacterAssigment.objects.filter(user=user)
    for assigment in assigments:
        booking = assigment.get_bookings()

class BookingsView(generic.DetailView):
    model = Bookings

class BookingsListView(generic.ListView):
    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            user_bookings = Bookings.objects.none()
        else:
            generate_bookings(user)
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
        url = reverse('larps:bookings_list')
        return HttpResponseRedirect(url)

    if request.method == 'POST':
        form = BookingsForm(request.POST, larp_id)
        if form.is_valid():
            bookings.save_bookings(form.cleaned_data)
            url = reverse('larps:bookings', args=[bookings.id])
            return HttpResponseRedirect(url)
    else:
        bookings_data = bookings.get_data()
        form = BookingsForm(bookings_data, larp_id)
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


def file_upload_view(request):
    if not request.user.is_staff:
        return not_allowed_view(request)
    template = "csv_import/file_upload.html"
    form = ImportCSVForm()
    context = {'form': form, 'user': request.user}

    if request.method == "POST":
        file = request.FILES['file']
        result = process_csv(file)
        context["result"] = result

    return render(request, template, context)



# UNIFORMS

def uniforms_view(request):
    if not request.user.is_staff:
        return not_allowed_view(request)
    template = "larps/uniforms.html"
    context = {"uniforms": Uniform.objects.all()}
    return render(request, template, context)


def uniform_sizes_view(request, uniform_id):
    if not request.user.is_staff:
        return not_allowed_view(request)
    template = "larps/uniforms.html"
    selected_uniform = Uniform.objects.get(id=uniform_id)
    players_with_sizes = selected_uniform.get_players_with_recommended_sizes()
    context = {}
    context["group"] = selected_uniform.group
    context["uniforms"] = Uniform.objects.all()
    context["players"] = players_with_sizes
    context["sizes"] = selected_uniform.get_sizes_with_quantities(players_with_sizes)
    return render(request, template, context)


# ADMINS VIEWS

def missing_info_index_view(request):
    if not request.user.is_staff:
        return not_allowed_view(request)
    template = "larps/missing_info_index.html"
    larps = Larp.objects.all()
    larps_info = []
    for larp in larps:
        number_of_runs = larp.get_number_of_runs()
        info = { "name": larp.name, "id": larp.id, "runs": range(1,number_of_runs+1) }
        larps_info.append(info)

    context = { "larps" : larps_info }
    return render(request, template, context)

def players_missing_info_view(request, larp_id):
    if not request.user.is_staff:
        return not_allowed_view(request)
    template = "larps/missing_info.html"
    larp = Larp.objects.get(id=larp_id)
    players_information = larp.get_players_information()
    context = { "larp" : larp.name, "larp_id": larp_id, "players_information": players_information }
    return render(request, template, context)


def players_missing_info_by_run_view(request, larp_id, run):
    if not request.user.is_staff:
        return not_allowed_view(request)
    template = "larps/missing_info.html"
    larp = Larp.objects.get(id=larp_id)
    players_information_all_runs = larp.get_players_information()
    if run <= len(players_information_all_runs):
        players_information = [ players_information_all_runs[run-1] ]
    else:
        players_information = [ ]
    context = { "larp" : larp.name, "run": run, "players_information": players_information }
    return render(request, template, context)
