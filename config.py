characters_header = "larp;run;email;name;character;group;race;rank;type;concept;sheet;weapon"
uniforms_header = "uniform_name;gender;american_size;european_size;chest_min;chest_max;arm_min;arm_max;waist_min;waist_max;shoulder_ min;shoulder_max;torso_min;torso_max;body_min;body_max"

file_types = [("Characters","Characters"),
            ("Uniforms", "Uniforms")]

file_headers = [ {"file_type":"Characters", "header": characters_header},
                 {"file_type":"Uniforms", "header": uniforms_header},
               ]


def csv_file_types():
    return file_types

def get_file_headers():
    return file_headers
