
from larps.models import Uniform, UniformSize
from .examples import example_players_complete, example_characters, example_groups
from .util_test import create_group, create_characters_assigments, create_character_assigment


# Initialize for uniforms and sizes testing

def create_uniform(group_name="", group=None):
    if not group:
        group = create_group(group_name)
    uniform = Uniform(group=group, name=group_name)
    uniform.save()
    return uniform

def create_uniform_size(size_information, group_name=""):
    uniform = create_uniform(group_name)
    size = UniformSize(uniform=uniform)
    size.set_values(size_information)
    size.save()
    return size

def create_uniform_with_sizes(sizes, group_name="", group=None):
    uniform = create_uniform(group_name=group_name, group=group)
    for size_information in sizes:
        size = UniformSize(uniform=uniform)
        size.set_values(size_information)
        size.save()
    return uniform

def create_uniform_with_players_and_sizes(sizes, players_info=example_players_complete, characters_names=example_characters, group_name="", run=1):
    group = create_group(group_name=group_name)
    uniform = create_uniform_with_sizes(sizes, group_name=group_name)
    assigments = create_characters_assigments(group, players_info, characters_names, run)
    return uniform

def create_uniform_with_player_in_several_runs(sizes, players_info, characters_names, player_in_several_runs, group_name="", runs=2):
    uniform = create_uniform_with_players_and_sizes(sizes, players_info, characters_names, group_name=group_name, run=1)
    for i in range(2,runs+1):
        create_character_assigment(uniform.group, player_in_several_runs, characters_names[1], run=i)
    return uniform
