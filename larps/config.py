file_types = [("Characters","Characters"),
            ("Uniforms", "Uniforms")]

file_headers = [ {"file_type":"Characters", "header": "run,player,character,group,planet,rank"},
                {"file_type":"Uniforms", "header": "name,group,color,gender,american_size,european_size,chest_min,chest_max,waist_min,waist_max"}
                ]


# Name of the Larp. Used for importing characters and players with CSV files
def larp_name():
    larp = "Mission Together"
    return larp

def csv_file_types():
    return file_types

def get_file_headers():
    return file_headers
