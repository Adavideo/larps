from django.urls import path

from . import views

app_name = 'larps'
urlpatterns = [
    path('', views.home_view, name='home'),
    path('player_profile/', views.player_profile, name='player_profile'),
    path('players', views.PlayersListView.as_view(), name='players_list'),
    path('character/<int:pk>/', views.CharacterView.as_view(), name='character'),
    path('characters', views.CharactersListView.as_view(), name='characters_list'),
    path('bookings', views.BookingsListView.as_view(), name='bookings_list'),
    path('bookings/<int:pk>/', views.BookingsView.as_view(), name='bookings'),
    path('bookings/larp_<int:larp_id>/', views.manage_bookings, name='manage_bookings'),
    path('logout/', views.logout_view, name='logout'),
]
