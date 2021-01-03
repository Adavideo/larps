# Basic characters and players examples

example_groups = [ "Scientists", "Doctors", "Mecanics" ]

example_characters = [ "Marie Curie", "Ada Lovelace", "Mary Jane Watson", "May Parker", "Peter Parker", "Leopold Fitz" ]
example_characters1 = [ "Marie Curie", "Ada Lovelace", "Mary Jane Watson", "May Parker" ]
example_characters2 = [ "Peter Parker", "Leopold Fitz", "Tony Stark", "Gemma Simmons" ]

example_players_complete = [
    { "username": "Ana_Garcia", "first_name": "Ana", "last_name": "Garcia", "gender":"female", "chest":90, "waist":75 },
    { "username": "Pepa_Perez", "first_name": "Pepa", "last_name": "Perez", "gender":"female", "chest":95, "waist":78 },
    { "username": "Manolo_Garcia", "first_name": "Manolo", "last_name": "Garcia", "gender":"male", "chest":100, "waist":90 },
    { "username": "Paco_Garcia", "first_name": "Paco", "last_name": "Garcia", "gender":"male", "chest":102, "waist":86 },
]

example_players_incomplete = [
    { "username": "Maria_Gonzalez", "first_name": "Maria", "last_name": "Gonzalez", "gender":"", "chest":0, "waist":0 },
    { "username": "Andrea_Hernandez", "first_name": "Andrea", "last_name": "Hernandez", "gender":"", "chest":0, "waist":0 },
]


# BOOKINGS examples

example_bookings = [
    { "weapon": False, "bus": None, "accomodation": None, "sleeping_bag": False },
    { "weapon": False, "bus": "Madrid", "accomodation": "on site", "sleeping_bag": True },
]

# UNIFORMS AND SIZES EXAMPLES

example_sizes = [
         {  "gender":"female", "american_size":"S", "european_size":"38", "chest_min":"86", "chest_max":"90", "waist_min":"70", "waist_max":"74" },
         {  "gender":"female", "american_size":"M", "european_size":"40", "chest_min":"90", "chest_max":"94", "waist_min":"74", "waist_max":"78" },
         {  "gender":"female", "american_size":"M", "european_size":"42", "chest_min":"94", "chest_max":"98", "waist_min":"78", "waist_max":"82" },
         {  "gender":"male", "american_size":"M", "european_size":"46", "chest_min":"90", "chest_max":"94", "waist_min":"78", "waist_max":"82" },
         {  "gender":"male", "american_size":"M", "european_size":"48", "chest_min":"94", "chest_max":"98", "waist_min":"82", "waist_max":"86" },
         {  "gender":"male", "american_size":"L", "european_size":"50", "chest_min":"98", "chest_max":"102", "waist_min":"86", "waist_max":"90" },
     ]

example_sizes_info = [
    "female. S/38 chest(86,90) waist(70,74)",
    "female. M/40 chest(90,94) waist(74,78)",
    "female. M/42 chest(94,98) waist(78,82)",
    "male. M/46 chest(90,94) waist(78,82)",
    "male. M/48 chest(94,98) waist(82,86)",
    "male. L/50 chest(98,102) waist(86,90)"
]

correct_size_examples = [
    ["Pilots","female","S",38,86,90,70,74,70,74],
    ["Pilots","female","M",40,90,94,74,78,74,78],
    ["Pilots","female","M",42,94,98,78,82,78,82],
    ["Pilots","female","L",44,98,102,82,86,82,86],
    ["Pilots","female","L",46,102,107,86,91,86,91],
    ["Pilots","female","XL",48,107,113,91,97,91,97]
]
incorrect_size_examples = [
    ["Pilots","female","L",44,98,102,82,86,82,86],
    ["","female","L",44,98,102,82,86,82,86],
    ["","female","L",44,98,102,82,86,82,86],
    ["Pilots","","L",44,98,102,82,86,82,86],
    ["Pilots","female","",44,98,102,82,86,82,86],
    ["Pilots","female","L","",98,102,82,86,82,86],
    ["Pilots","female","","",98,102,82,86,82,86],
    ["Pilots","female","L",44,"","","","",82,86]
]

empty_size_info = { "gender":"", "american_size":"", "european_size":"", "chest_min":"", "chest_max":"", "waist_min":"", "waist_max" :"" }


# csv examples

uniforms_csv_example = '''uniform_name;gender;american_size;european_size;chest_min;chest_max;arm_min;arm_max;waist_min;waist_max;shoulder_ min;shoulder_max;torso_min;torso_max;body_min;body_max
Pilots;female;S;38;86;90;70;74;70;74
Pilots;female;M;40;90;94;74;78;74;78'''

# larp;run;email;name;character;group;race;rank;type;concept;sheet;weapon
characters_csv_example = '''larp;run;email;name;character;group;race;rank;type;concept;sheet;weapon
Mission Together;1;test1@email.com;Werner Mikolasch;Ono;agriculture teacher;Rhea;sargeant;secret NPC;https://docs.google.com/document/d/ynZA/edit?usp=sharing;this is a test;Your character owns a weapon, we will provide it
Mission Together;2;test2@email.com;Fabio;Fuertes;artist teacher;Kepler;;player;https://docs.google.com/document/d/1sICrVe/edit?usp=sharing;this is a test;'''

incorrect_csv = '''character;group;planet
1;Werner Mikolasch;Ono;agriculture teacher;Rhea
2;Fabio;Fuertes;artist teacher;Kepler'''

example_email = "test1@email.com"

example_character = {
    'larp': '',
    'run': '1',
    'email': '',
    'name': 'Kira',
    'character': 'Tatiana',
    'group': 'Doctors',
    'race': 'Kepler',
    'rank': 'capitain',
    'type': 'player',
    'concept': 'https://docs.google.com/document/d/ynZA/edit?usp=sharing',
    'sheet': 'https://docs.google.com/document/d/abcde/edit?usp=sharing',
    'weapon': 'Your character owns a weapon, we will provide it',
}
