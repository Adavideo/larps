
example_players_incomplete = [
    { "username": "Maria_Gonzalez", "first_name": "Maria", "last_name": "Gonzalez", "gender":"", "chest":0, "waist":0, "diet":"" },
    { "username": "Andrea_Hernandez", "first_name": "Andrea", "last_name": "Hernandez", "gender":"", "chest":0, "waist":0, "diet":"" },
]

def initialize_diets_amounts(diets_types, run_number):
    all_diets_amounts = []
    for diet in diets_types:
        diet_amount = { "diet_name": diet.name, "amount": 0, "run": run_number }
        all_diets_amounts.append(diet_amount)
    return all_diets_amounts

def increment_diet_ammount(diets_amounts, diet_name):
    for diet in diets_amounts:
        if diet["diet_name"] == diet_name:
            diet["amount"] += 1


def get_diets_amounts(diets_all_runs, number_of_runs, diets_types):
    diets_amounts_all_runs = []
    count = 1
    for diets_for_this_run in diets_all_runs:
        diets_amounts = initialize_diets_amounts(diets_types, run_number=count)
        for player_diet in diets_for_this_run:
            increment_diet_ammount(diets_amounts, player_diet["diet"])
        diets_amounts_all_runs.append(diets_amounts)
        count += 1
    return diets_amounts_all_runs

def get_runs_number(assigments):
    runs = 0
    for assigment in assigments:
        if assigment.run > runs:
            runs = assigment.run
    return runs

# Create an empty list for each run
def get_empty_run_list(number_of_runs):
    runs_list = []
    for i in range(0, number_of_runs):
        runs_list.append([])
    return runs_list

def get_player_diet_info(assigment):
    player_diet = { "character": assigment.character.name, "run": assigment.run }

    if assigment.user:
        player_diet["player"] = assigment.user.first_name + " " + assigment.user.last_name
    else:
        player_diet["player"] = ""

    profile = assigment.get_player_profile()
    if profile and profile.dietary_restrictions:
        player_diet["diet"] = profile.dietary_restrictions.name
        player_diet["comments"] = profile.get_diet_comments()
    else:
        player_diet["diet"] = "Not provided yet"
        player_diet["comments"] = ""
        
    return player_diet


def get_players_diets(assigments, number_of_runs):
    diets_list = get_empty_run_list(number_of_runs)
    # populate the lists with the information of the players diets
    for assigment in assigments:
        player_diet = get_player_diet_info(assigment)
        run_index = assigment.run-1
        diets_list[run_index].append(player_diet)
    return diets_list


def get_food_information(assigments, diets_types):
    number_of_runs = get_runs_number(assigments)
    players_diets = get_players_diets(assigments, number_of_runs)
    diets_amounts = get_diets_amounts(players_diets, number_of_runs, diets_types)
    food_information = { "players_diets": players_diets, "diets_amounts": diets_amounts }
    return food_information
