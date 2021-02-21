from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'larps'

urlpatterns = [
    path('', login_required(views.home_view), name='home'),
    path('logout/', views.logout_view, name='logout'),
    # USERS
    path('uniform_measurements/', login_required(views.measurements_form_view), name='measurements_form'),
    path('bookings/larp_<int:larp_id>/run_<int:run>/', login_required(views.manage_bookings_view), name='manage_bookings'),
    path('characters/larp_<int:larp_id>/run_<int:run>/', login_required(views.characters_run_view), name='characters_run'),
    path('my_character/larp_<int:larp_id>/run_<int:run>/', login_required(views.my_character_view), name='my_character'),
    # ADMINS
    path('file_upload/', login_required(views.file_upload_view), name='file_upload'),
    path('uniforms', login_required(views.uniforms_view), name="uniforms"),
    path('uniform_sizes/<int:uniform_id>', login_required(views.uniform_sizes_view), name="uniform_sizes"),
    path('missing_info/', login_required(views.missing_info_index_view), name="missing_info_index"),
    path('missing_info/larp_<int:larp_id>/', login_required(views.players_missing_info_view), name="missing_info"),
    path('missing_info/larp_<int:larp_id>/run_<int:run>/', login_required(views.players_missing_info_by_run_view), name="missing_info_run"),
]
