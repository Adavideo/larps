from django.urls import path

from . import views

app_name = 'larps'
urlpatterns = [
    path('player/<int:pk>/', views.PlayerView.as_view(), name='player'),
    path('players', views.PlayersListView.as_view(), name='playerslist'),
    path('character/<int:pk>/', views.CharacterView.as_view(), name='character'),
    path('characters', views.CharactersListView.as_view(), name='characterslist'),
    path('booking/<int:pk>/', views.BookingsView.as_view(), name='bookings'),
    path('bookings', views.BookingsListView.as_view(), name='bookingslist'),
    path('player_profile/', views.player_profile, name='player_profile'),
    path('logout/', views.logout_view, name='logout'),
]
