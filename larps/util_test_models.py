from .models import *

def create_player(player_info):
    user = User(username=player_info["username"], first_name=player_info["first_name"], last_name=player_info["last_name"])
    user.save()
    player = Player(user=user, gender=player_info["gender"], chest=player_info["chest"], waist=player_info["waist"])
    player.save()
    return player
