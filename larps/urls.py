from django.urls import path

from . import views

app_name = 'larps'
urlpatterns = [
    path('', views.home_view, name='home'),
    path('player/<int:pk>/', views.PlayerView.as_view(), name='player'),
    path('players', views.PlayersListView.as_view(), name='playerslist'),
    path('character/<int:pk>/', views.CharacterView.as_view(), name='character'),
    path('characters', views.CharactersListView.as_view(), name='characterslist'),
    path('bookings', views.BookingsListView.as_view(), name='bookingslist'),
    path('bookings/<int:pk>/', views.BookingsView.as_view(), name='bookings'),
    path('bookings/larp_<int:larp_id>', views.manage_bookings, name='manage_bookings'),
    path('player_profile/', views.player_profile, name='player_profile'),
    path('logout/', views.logout_view, name='logout'),
]
