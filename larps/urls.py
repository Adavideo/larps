from django.urls import path
from django.contrib.auth.decorators import login_required
from .config import login_required_enabled, csv_file_types
from . import views

app_name = 'larps'
csv_file_types = csv_file_types()

if login_required_enabled():
    urlpatterns = [
        path('', views.home_view, name='home'),
        path('logout/', views.logout_view, name='logout'),
        path('player_profile/', login_required(views.player_profile_view), name='player_profile'),
        path('players', login_required(views.PlayersListView.as_view()), name='players_list'),
        path('character/<int:pk>/', login_required(views.CharacterView.as_view()), name='character'),
        path('characters', login_required(views.CharactersListView.as_view()), name='characters_list'),
        path('bookings', login_required(views.BookingsListView.as_view()), name='bookings_list'),
        path('bookings/<int:pk>/', login_required(views.BookingsView.as_view()), name='bookings'),
        path('bookings/larp_<int:larp_id>/run_<int:run>/', login_required(views.manage_bookings_view), name='manage_bookings'),
        path('file_upload/', login_required(views.file_upload_index_view), name='file_upload'),
        path('file_upload/<int:file_type_number>/', login_required(views.file_upload_view), name='file_upload'),
        path('uniforms', login_required(views.uniforms_view), name="uniforms"),
        path('uniform_sizes/<int:uniform_id>', login_required(views.uniform_sizes_view), name="uniform_sizes"),
    ]
else:
    urlpatterns = [
        path('', views.home_view, name='home'),
        path('logout/', views.logout_view, name='logout'),
        path('player_profile/', views.player_profile_view, name='player_profile'),
        path('players', views.PlayersListView.as_view(), name='players_list'),
        path('character/<int:pk>/', views.CharacterView.as_view(), name='character'),
        path('characters', views.CharactersListView.as_view(), name='characters_list'),
        path('bookings', views.BookingsListView.as_view(), name='bookings_list'),
        path('bookings/<int:pk>/', views.BookingsView.as_view(), name='bookings'),
        path('bookings/larp_<int:larp_id>/run_<int:run>/', views.manage_bookings_view, name='manage_bookings'),
        path('file_upload/', views.file_upload_index_view, name='file_upload'),
        path('file_upload/<int:file_type_number>/', views.file_upload_view, name='file_upload'),
        path('uniforms', views.uniforms_view, name="uniforms"),
        path('uniform_sizes/<int:uniform_id>/', views.uniform_sizes_view, name="uniform_sizes"),
    ]
