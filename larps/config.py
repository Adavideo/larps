file_types = [("Characters","Characters"),
            ("Uniforms", "Uniforms")]

file_types_headers = {
    "Characters": "run,player,character,group,planet,rank",
    "Uniforms": "name,group,color,gender,american_size,european_size,chest_min,chest_max,waist_min,waist_max",
}



def login_required_enabled():
    login_required_enabled = True
    return login_required_enabled

# Name of the Larp. Used for importing characters and players with CSV files
def larp_name():
    larp = "Mission Together"
    return larp

def csv_file_types():
    return file_types

def correct_file_type(header, file_type):
    correct_header = file_types_headers[file_type]
    if correct_header in header:
        return True
    else:
        return False
