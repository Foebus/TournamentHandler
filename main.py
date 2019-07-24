# coding=utf-8
from time import sleep

import pygame
import sys

from challenge import Challenge, Test
from display_handler import *
import pickle
import os.path
from pygame.locals import *


def handle_events_leaderboard():
    continue_displaying_leaderboard = True
    events = pygame.event.get()
    for event in events:
        if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
            sys.exit()
        elif event.type == MOUSEBUTTONUP:
            continue_displaying_leaderboard = False
    return continue_displaying_leaderboard


enables_animation = True


def handle_events_standard_mode(actual_challengers, act_test, act_tournament, points_given,
                                game_state):
    global enables_animation
    round_over = False
    test_over = False
    ask_for_lb = False
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
            music_handler.test_quotes()
        elif event.type == KEYDOWN and event.key == K_INSERT:
            round_over = True
        elif event.type == KEYDOWN and event.key == K_a:
            enables_animation = not enables_animation
        elif event.type == KEYDOWN and event.key == K_s:
            act_tournament.save_yourself()
        elif event.type == MOUSEBUTTONUP:
            (x, y) = pygame.mouse.get_pos()
            round_over = handle_mouseclick(x, y, actual_challengers)
            if not round_over:
                test_over = True
    if test_over:
        update_score_display(actual_challengers)
        points_given += 1
        if points_given == act_test.total_points:
            round_over = True
        else:
            objective, genre, game = act_test.get_next_test()

            if enables_animation:
                display_genre_game_animation(genre, game)
            display_act_challenge(actual_challengers, objective)

    if round_over:
        act_test = Challenge(3)
        act_tournament.save_yourself()
        actual_challengers = act_tournament.get_next_group(points_given == 3)
        points_given = 0
        if actual_challengers is None:
            game_state = "gameover"
        else:
            objective, genre, game = act_test.get_next_test()

            if enables_animation:
                display_genre_game_animation(genre, game)
            display_act_challenge(actual_challengers, objective)
    return actual_challengers, act_test, act_tournament, points_given, game_state, ask_for_lb


def handle_mouseclick(x, y, actual_challengers: Group):
    (w, h) = pygame.display.get_surface().get_size()
    if y > h / 5:
        i = int(x * actual_challengers.challenger_number / w)
        actual_challengers.give_point(i)
        update_score_display(actual_challengers)
        music_handler.start_quote(actual_challengers.challengers[i].music_dir)
        return False
    else:
        return True


def game_loop(game_state: str, act_tournament: Tournament):
    """

    :param game_state: Actual game state
    :param act_tournament: The tournament to play
    """
    displaying_leader_board = False
    keep_displaying_leaderborad = False
    ask_for_lb = False
    actual_challengers = act_tournament.get_next_group()
    loops_in_this_screen = 0
    points_given = 0

    act_test = Challenge(3)
    o, genre, game = act_test.get_next_test()
    display_genre_game_animation(genre, game)
    display_act_challenge(actual_challengers, act_test.act_test[0])

    while game_state != "gameover":
        if displaying_leader_board:
            keep_displaying_leaderborad = handle_events_leaderboard()
            loops_in_this_screen += 3
        else:
            actual_challengers, act_test, act_tournament, points_given, game_state, ask_for_lb \
                = handle_events_standard_mode(actual_challengers, act_test, act_tournament, points_given, game_state)

        if loops_in_this_screen == 600 or (not keep_displaying_leaderborad and displaying_leader_board) or ask_for_lb:
            loops_in_this_screen = 0
            displaying_leader_board = not displaying_leader_board
            if not displaying_leader_board:
                reset_display()
                display_act_challenge(actual_challengers, act_test.act_test[0])
            else:
                display_leader_board(act_tournament)
            sleep(1)

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
