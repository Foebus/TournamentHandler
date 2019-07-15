# coding=utf-8
from time import sleep

import pygame
import sys

from challenge import Challenge, Test
from tournament import Tournament
from display_handler import *
import pickle
import os.path
from pygame.locals import *


def handle_mouseclick(x, y, actual_challengers):
    (w, h) = pygame.display.get_surface().get_size()
    if y > h / 5:
        i = int(x * actual_challengers.challenger_number / w)
        actual_challengers.give_point(i)
        update_score_display(actual_challengers)
        return False
    else:
        return True


def game_loop(game_state, act_tournament):
    """

    :param game_state: Actual game state
    :type game_state: str
    :param act_tournament: The tournament to play
    :type act_tournament: tournament.Tournament
    """
    round_over = False
    test_over = True
    actual_challengers = act_tournament.get_next_group()
    loops_in_this_screen = 0
    points_given = -1
    act_test = Challenge(3)
    while game_state != "gameover":
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_1:
                actual_challengers.give_point(0)
                test_over = True
            elif event.type == KEYDOWN and event.key == K_2:
                actual_challengers.give_point(1)
                test_over = True
            elif event.type == KEYDOWN and event.key == K_3:
                actual_challengers.give_point(2)
                test_over = True
            elif event.type == KEYDOWN and event.key == K_4:
                actual_challengers.give_point(3)
                test_over = True
            elif event.type == KEYDOWN and event.key == K_5:
                actual_challengers.give_point(4)
                test_over = True
            elif event.type == KEYDOWN and event.key == K_6:
                actual_challengers.give_point(5)
                test_over = True
            elif event.type == KEYDOWN and event.key == K_7:
                actual_challengers.give_point(6)
                test_over = True
            elif event.type == KEYDOWN and event.key == K_8:
                animate_arrow_rotation(1, windowSurface)
            elif event.type == KEYDOWN and event.key == K_INSERT:
                round_over = True
            elif event.type == KEYDOWN and event.key == K_s:
                act_tournament.save_yourself()
            elif event.type == MOUSEBUTTONUP:
                (x, y) = pygame.mouse.get_pos()
                round_over = handle_mouseclick(x, y, actual_challengers)
                if not round_over:
                    test_over = True
        if test_over:
            test_over = False
            update_score_display(actual_challengers)
            points_given += 1
            if points_given == act_test.total_points:
                round_over = True
            else:
                objective, genre = act_test.get_next_test()
                objective = objective.split("\n")

                animate_arrow_rotation(Test.GENRE[genre] / len(Test.GENRE), windowSurface)
                display_challengers(actual_challengers)

                if len(objective) < 3:
                    objective += [" "]
                for i, line in enumerate(objective):
                    left = (WIDTH - 3 * FONT_SIZE * len(line) // 8) / 2
                    top = 5 * HEIGHT / 6 + i * FONT_SIZE
                    objective_rubber = pygame.Surface((len(line) * FONT_SIZE, FONT_SIZE))
                    objective_rubber.fill((0, 0, 0))
                    display_text(left, top, line, objectiveSurface, objective_rubber, erase_line=True)

        if round_over:
            round_over = False
            points_given = -1
            test_over = True
            act_test = Challenge(3)
            actual_challengers = act_tournament.get_next_group()
            if actual_challengers is None:
                game_state = "gameover"
            else:
                act_tournament.save_yourself()
                height = display_challengers(actual_challengers)

        pygame.time.delay(100)
        loops_in_this_screen += 1
    display_winner(act_tournament)
    try:
        os.remove("savegame")
    except:
        print("And no need to erase the saved game!")
    sleep(300)


pygame.display.set_caption('Challenge en cours')
#  pygame.mouse.set_visible(0)

if os.path.isfile("savegame"):
    pygame.display.set_caption('Sauvegarde trouvée, souhaitez-vous la charger?')

    decision_made = False
    while not decision_made:
        loading_events = pygame.event.get()
        for loading_event in loading_events:
            if (loading_event.type == KEYDOWN and loading_event.key == K_n) or (
                    loading_event.type == KEYDOWN and loading_event.key == K_ESCAPE):
                tournament = Tournament(tournament_type="deux_tours_pool_plus_qualif", pool_rounds=3)
                tournament.extract_from_json("tournament.json")
                decision_made = True
                break
            elif (loading_event.type == KEYDOWN and loading_event.key == K_y) or (
                    loading_event.type == KEYDOWN and loading_event.key == K_INSERT):
                f = open("savegame", "rb")
                tournament = pickle.load(f)
                for c in tournament.challengers_pool:
                    c.reload_image()
                f.close()
                decision_made = True
else:
    tournament = Tournament(tournament_type="deux_tours_pool_plus_qualif", pool_rounds=3)
    tournament.extract_from_json("tournament.json")

reset_display()

pygame.display.flip()
initial_game_state = "entering"
game_loop(initial_game_state, tournament)
