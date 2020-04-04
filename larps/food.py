

def get_food_count(diets_list, runs_number):
    return []
    food_count = []
    for run in range(1,runs):
        for player_diet in diets_list:
            run_diets = []
            if player_diet["run"] == run:
                run_diets.append(player_diet)

def get_runs_number(assigments):
    runs = 0
    for assigment in assigments:
        if assigment.run > runs:
            runs = assigment.run
    return runs

def get_players_diets(assigments, number_of_runs):
    diets_list = []
    # Create empty list for each run
    for i in range(0, number_of_runs):
        diets_list.append([])
    # populate the lists with the information of the players diets
    for assigment in assigments:
        profile = assigment.get_player_profile()
        player_name = assigment.user.first_name + " " + assigment.user.last_name
        player_diet = { "character": assigment.character.name, "run": assigment.run, "player": player_name, "diet": profile.dietary_restrictions }
        run_index = assigment.run-1
        diets_list[run_index].append(player_diet)
    return diets_list


def get_food_information(assigments):
    number_of_runs = get_runs_number(assigments)
    players_diets = get_players_diets(assigments, number_of_runs)
    food_count = get_food_count(players_diets, number_of_runs)
    food_information = { "players_diets": players_diets, "food_count": food_count }
    return food_information
