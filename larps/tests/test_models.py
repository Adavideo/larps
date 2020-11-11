from django.test import TestCase
from django.contrib.auth.models import User
from larps.config import larp_name
from larps.models import Player, Character, CharacterAssigment, Larp, Group, Bookings
from .util_test import create_player, create_group, create_characters_assigments, create_character_assigment
from .util_test_uniforms import create_uniform_with_player_in_several_runs
from .examples import example_players_complete, example_players_incomplete, example_characters, example_groups, example_sizes


# PLAYER PROFILES

class PlayerModelTests(TestCase):

    def test_create_player_profile(self):
        """
        create_player_profile() creates a Player object asociated to a test User account.
        """
        player_info = example_players_complete[0]
        player = create_player(player_info)
        self.assertEqual(player.user.username, player_info["username"])
        self.assertEqual(str(player), player_info["first_name"] + " " + player_info["last_name"])
        self.assertEqual(player.gender, player_info["gender"])

    def test_create_player_profile_with_size_information(self):
        """
        create_player_profile_with_size_information() creates a Player object asociated to a test User account
        and adds information about the size of the player.
        """
        test_user = User(username="ana")
        test_player = Player(user=test_user, shoulder= 40, height = 160, chest = 90, waist = 90)
        self.assertIs(test_player.shoulder, 40)
        self.assertIs(test_player.height, 160)
        self.assertIs(test_player.chest, 90)
        self.assertIs(test_player.waist, 90)


# LARPS AND CHARACTERS

class GroupModelTests(TestCase):

    def test_create_group(self):
        """
        create_group creates a Group associated with a Larp.
        """
        group_name = "test group name"
        group = create_group(group_name)
        self.assertEqual(group.name, group_name)
        self.assertEqual(group.larp.name, larp_name())

    def test_create_empty_group(self):
        """
        create_empty_group creates agroup associated with a Larp.
        """
        empty_group = create_group("")
        self.assertEqual(empty_group.larp.name, larp_name())
        self.assertEqual(str(empty_group), larp_name()+" - no group")

    def test_create_characters_assigments(self):
        group = create_group()
        create_characters_assigments(group=group, players=example_players_complete, characters=example_characters)
        for i in range(0,len(example_players_complete)):
            # Testing user creation
            player_info = example_players_complete[i]
            user_search = User.objects.filter(username=player_info["username"])
            self.assertEqual(len(user_search), 1)
            user = user_search[0]
            self.assertEqual(user.username, player_info["username"])
            # Testins player profile creation
            player_profiles = Player.objects.filter(user=user)
            self.assertEqual(len(player_profiles), 1)
            self.assertEqual(player_profiles[0].gender, player_info["gender"])
            # Testing character creation
            character_name = example_characters[i]
            character_search = Character.objects.filter(name=character_name)
            self.assertEqual(len(character_search), 1)
            character = character_search[0]
            self.assertEqual(character.name, character_name)
            self.assertEqual(character.group, group)
            # Testing character assigment
            assigments = CharacterAssigment.objects.filter(character=character, user=user)
            self.assertEqual(len(assigments), 1)


    def test_get_player_profiles_empty(self):
        """
        create_get_player_profiles_empty returns an empty array
        """
        group = create_group()
        player_profiles = group.get_player_profiles()
        self.assertEqual(player_profiles, [])
        all_profiles = Player.objects.all()
        self.assertEqual(str(all_profiles), "<QuerySet []>" )

    def test_get_character_assigments(self):
        group = create_group()
        create_characters_assigments(group, players=example_players_complete, characters=example_characters)
        assigments_group = group.get_character_assigments()
        self.assertEqual(len(assigments_group), len(example_players_complete))
        for i in range(0,len(example_players_complete)):
            self.assertEqual(assigments_group[i].user.username, example_players_complete[i]["username"])
            self.assertEqual(assigments_group[i].character.name, example_characters[i])

    def test_get_player_profiles_users_with_no_profile(self):
        """
        create_get_player_profiles returns empty profiles associated with the users assigned to this group.
        """
        group = create_group()
        create_characters_assigments(group=group, players=example_players_incomplete, characters=example_characters)
        player_profiles = group.get_player_profiles()
        self.assertEqual(str(player_profiles), "[<Player: Maria Gonzalez>, <Player: Andrea Hernandez>]")
        self.assertEqual(player_profiles[0].user.username, example_players_incomplete[0]["username"])
        self.assertEqual(player_profiles[0].chest, 0)
        self.assertEqual(player_profiles[0].waist, 0)
        self.assertEqual(player_profiles[1].user.username, example_players_incomplete[1]["username"])
        self.assertEqual(player_profiles[1].chest, 0)
        self.assertEqual(player_profiles[1].waist, 0)

    def test_get_player_profiles_with_correct_examples(self):
        """
        create_get_player_profiles returns the profiles of the players assigned to this group.
        """
        group = create_group()
        create_characters_assigments(group, players=example_players_complete, characters=example_characters[2:4])
        player_profiles = group.get_player_profiles()
        self.assertEqual(str(player_profiles), "[<Player: Ana Garcia>, <Player: Pepa Perez>]")
        self.assertEqual(player_profiles[0].user.username, example_players_complete[0]["username"])
        self.assertEqual(player_profiles[0].chest, example_players_complete[0]["chest"])
        self.assertEqual(player_profiles[0].waist, example_players_complete[0]["waist"])
        self.assertEqual(player_profiles[1].user.username, example_players_complete[1]["username"])
        self.assertEqual(player_profiles[1].chest, example_players_complete[1]["chest"])
        self.assertEqual(player_profiles[1].waist, example_players_complete[1]["waist"])

    def test_get_player_profiles_player_in_2_runs(self):
        player_repeated = example_players_complete[1]
        uniform = create_uniform_with_player_in_several_runs(sizes=example_sizes, players_info=example_players_complete,
                                                            characters_names=example_characters, player_in_several_runs=player_repeated,
                                                            group_name=example_groups[0], runs=2)
        profiles = uniform.group.get_player_profiles()
        self.assertEqual(len(profiles), len(example_players_complete))


class CharacterModelTests(TestCase):

    def test_create_character(self):
        """
        create_character creates a character for a larp.
        """
        group = create_group(example_groups[1])
        character = Character(group = group, name=example_characters[0])
        self.assertEqual(character.name, example_characters[0])
        self.assertIs(character.group, group)
        self.assertEqual(character.group.name, example_groups[1])
        self.assertEqual(character.group.larp.name, larp_name())

    def test_create_character_assigment(self):
        """
        create_character_assigment assigns a character to a player on a concrete larp run.
        """
        user = User(username="ana", first_name="Ana", last_name="Garcia")
        group = create_group(example_groups[1])
        character = Character(group = group, name=example_characters[0])
        character_assigment = CharacterAssigment(run=1, character=character, user=user)
        self.assertIs(character_assigment.character.group.larp.name, larp_name())
        self.assertIs(character_assigment.character.name, example_characters[0])
        self.assertIs(character_assigment.character.group.name, example_groups[1])
        self.assertIs(character_assigment.user.username, "ana")
        self.assertEqual(str(character_assigment), larp_name()+" run 1 - Marie Curie assigned to Ana Garcia")

    def test_create_character_assigment_without_user(self):
        """
        create_character_assigment assigns a character to a larp run but without an asigned user.
        This is useful when you have a new character that has no player assigned yet.
        """
        larp = Larp(name = larp_name())
        group_name = example_groups[1]
        group = Group(larp=larp, name=group_name)
        character = Character(group = group, name="Marie Curie")
        character_assigment = CharacterAssigment(run=1, character=character)
        self.assertIs(character_assigment.character.group.larp, larp)
        self.assertEqual(character_assigment.character.group.larp.name, larp_name())
        self.assertIs(character_assigment.character, character)
        self.assertEqual(character_assigment.character.name, example_characters[0])
        self.assertIs(character_assigment.character.group, group)
        self.assertEqual(character_assigment.character.group.name, example_groups[1])
        self.assertEqual(str(character_assigment), larp_name()+" run 1 - Marie Curie")

    def test_create_character_assigment(self):
        """
        create_character_assigment assigns a character to a player on a concrete larp run for a character without a group.
        """
        user = User(username="ana", first_name="Ana", last_name="Garcia")
        larp = Larp(name = larp_name())
        empty_group = Group(name="", larp = larp)
        character = Character(group = empty_group, name="Marie Curie")
        character_assigment = CharacterAssigment(run=1, character=character, user=user)
        self.assertIs(character_assigment.character.name, "Marie Curie")
        self.assertIs(character_assigment.character.group.larp, larp)
        self.assertEqual(character_assigment.character.group.larp.name, larp_name())
        self.assertIs(character_assigment.user.username, "ana")
        self.assertEqual(str(character_assigment), larp_name()+" run 1 - Marie Curie assigned to Ana Garcia")


class CharacterAssigmentModelTests(TestCase):

    def test_create_booking(self):
        # initialize
        group = create_group()
        player_info = example_players_complete[0]
        character_name = example_characters[0]
        assigment = create_character_assigment(group, player_info, character_name)
        # generate
        bookings = assigment.get_bookings()
        bookings_search = Bookings.objects.filter(user=assigment.user)
        # validate
        self.assertEqual(len(bookings_search), 1)
        self.assertEqual(bookings_search[0], bookings)
        self.assertEqual(bookings.user.username, player_info["username"])
        self.assertEqual(bookings.larp.name, group.larp.name)
        self.assertEqual(bookings.run, 1)
        self.assertIs(bookings.weapon, None)
        self.assertIs(bookings.bus, None)
        self.assertIs(bookings.accomodation, None)
        self.assertIs(bookings.sleeping_bag, None)
        self.assertIs(bookings.comments, "no")
