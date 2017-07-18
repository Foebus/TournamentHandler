from time import sleep

import pygame
import sys
import tournament
import pickle
import os.path
from pygame.locals import *

pygame.init()
WIDTH = 1280
HEIGHT = 780
FONT_SIZE = 36
POINT_HEIGHT = 3 * FONT_SIZE
round_nbr = 10
windowSurface = pygame.display.set_mode((WIDTH, HEIGHT))
point_rubber = pygame.display.set_mode((WIDTH, FONT_SIZE))
point_rubber = point_rubber.convert()
point_rubber.fill((0, 0, 0))
pointSurface = pygame.display.set_mode((WIDTH, HEIGHT))
challenger_rubber = pygame.display.set_mode((WIDTH, HEIGHT))
challenger_rubber = challenger_rubber.convert()
challenger_rubber.fill((0, 0, 0))
challengerSurface = pygame.display.set_mode((WIDTH, HEIGHT))
lightning = pygame.image.load("Images/eclair.png")


def update_score_display(actual_challengers_to_display, act_height):
    """

    :param act_height: The height of the lowest image
    :type act_height: int
    :param actual_challengers_to_display: The group of challengers whose name to display
    :type actual_challengers_to_display: tournament.Group
    """
    font = pygame.font.Font(None, FONT_SIZE)
    challenger_number = actual_challengers_to_display.challengerNumber
    point_rectangles = []  # Rect(0, act_height + FONT_SIZE / 2, WIDTH, FONT_SIZE)
    pointSurface.blit(point_rubber,  pointSurface.get_rect(left=0, top=POINT_HEIGHT))
    for i in range(challenger_number):
        point_rectangles.append(Rect((2 * i + 1) * WIDTH / (2 * challenger_number) -
                                     len(str(actual_challengers_to_display.get_points(i))) * FONT_SIZE / 2,
                                     POINT_HEIGHT,
                                     len(str(actual_challengers_to_display.get_points(i)))*FONT_SIZE,
                                     FONT_SIZE))
        points = font.render(str(actual_challengers_to_display.get_points(i)), 1, (255, 0, 0))
        point_pos = points.get_rect(centerx=pointSurface.get_width() * (2 * i + 1) / (challenger_number * 2),
                                    top=POINT_HEIGHT)
        pointSurface.blit(points, point_pos)
        pygame.display.update(point_rectangles[i])


def display_challengers(actual_challengers_to_display):
    """

    :param actual_challengers_to_display: the challenger group to display
    :type actual_challengers_to_display: tournament.Group
    """
    font = pygame.font.Font(None, FONT_SIZE)
    challenger_number = actual_challengers_to_display.challengerNumber
    challengerSurface.blit(challenger_rubber, (0, 0))
    max_height = 0
    old_width = 0
    scale_ratio = 1
    for i in range(challenger_number):
        act_challenger = actual_challengers_to_display.challengers[i]
        challenger_image = act_challenger.image
        old_width = challenger_image.get_width()
        scale_ratio = float(WIDTH) / (challenger_number * old_width)
        old_height = challenger_image.get_height()
        act_challenger.rescale_image(int(old_width * scale_ratio), int(old_height * scale_ratio))
        challenger_image = act_challenger.image
        act_height = challenger_image.get_height()
        challengerSurface.blit(challenger_image, (i * challenger_image.get_width(), POINT_HEIGHT + FONT_SIZE))
        pseudo = font.render(act_challenger.name, 1, (10, 90, 10))
        text_pos = pseudo.get_rect(centerx=challengerSurface.get_width() * (2 * i + 1) / (challenger_number * 2),
                                   top=2 * FONT_SIZE)
        challengerSurface.blit(pseudo, text_pos)
        max_height = max(max_height, act_height)
    update_score_display(actual_challengers_to_display, max_height + FONT_SIZE)
    for i in range(challenger_number - 1):
        challengerSurface.blit(lightning, ((i + 1) * old_width * scale_ratio - lightning.get_width() / 2, 0))
    group = font.render(actual_challengers_to_display.title, 1, (255, 241, 0))

    text_pos = group.get_rect(centerx=challengerSurface.get_width() / 2,
                              top=5)
    challengerSurface.blit(group, text_pos)

    challengers_rectangle = Rect(0, 0, WIDTH, HEIGHT)
    pygame.display.update(challengers_rectangle)
    return max_height + FONT_SIZE


def display_winner(ended_tournament):
    # type: (tournament) -> None
    """

    :param ended_tournament: The tournament where to find the winner
    :type ended_tournament: tournament.Tournament
    """
    winner = ended_tournament.groups[len(ended_tournament.groups) - 1].get_winner()
    font = pygame.font.Font(None, FONT_SIZE)
    act_width = winner.image.get_width()
    scale_ratio = float(WIDTH) / act_width
    act_height = winner.image.get_height()
    winner.rescale_image(int(act_width * scale_ratio),
                         int(act_height * scale_ratio))
    challenger_image = winner.image
    challengerSurface.blit(challenger_image, (0, 0))
    pseudo = font.render("Bravo, "+winner.name+" pour ta victoire \n\r on peut clairement dire que tu roxes du poney!!",
                         1, (10, 90, 10))
    text_pos = pseudo.get_rect(centerx=windowSurface.get_width() / 2,
                               centery=challenger_image.get_height() - FONT_SIZE * 3)
    challengerSurface.blit(pseudo, text_pos)
    challengers_rectangle = Rect(0, 0, WIDTH, HEIGHT)
    pygame.display.update(challengers_rectangle)


def game_loop(game_state, act_tournament):
    """

    :param game_state: Actual game state
    :type game_state: str
    :param act_tournament: The tournament to play
    :type act_tournament: tournament.Tournament
    """
    round_over = False
    actual_challengers = act_tournament.get_next_group()
    height = display_challengers(actual_challengers)
    loops_in_this_screen = 0
    while game_state != "gameover":
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_1:
                actual_challengers.give_point(0)
                update_score_display(actual_challengers, height)
            elif event.type == KEYDOWN and event.key == K_2:
                actual_challengers.give_point(1)
                update_score_display(actual_challengers, height)
            elif event.type == KEYDOWN and event.key == K_3:
                actual_challengers.give_point(2)
                update_score_display(actual_challengers, height)
            elif event.type == KEYDOWN and event.key == K_4:
                actual_challengers.give_point(3)
                update_score_display(actual_challengers, height)
            elif event.type == KEYDOWN and event.key == K_5:
                actual_challengers.give_point(4)
                update_score_display(actual_challengers, height)
            elif event.type == KEYDOWN and event.key == K_6:
                actual_challengers.give_point(5)
                update_score_display(actual_challengers, height)
            elif event.type == KEYDOWN and event.key == K_7:
                actual_challengers.give_point(6)
                update_score_display(actual_challengers, height)
            elif event.type == KEYDOWN and event.key == K_INSERT:
                round_over = True
            elif event.type == KEYDOWN and event.key == K_s:
                act_tournament.save_yourself()
        if round_over:
            round_over = False
            actual_challengers = act_tournament.get_next_group()
            if actual_challengers is None:
                game_state = "gameover"
            else:
                act_tournament.save_yourself()
                height = display_challengers(actual_challengers)
        pygame.time.delay(100)
        loops_in_this_screen += 1
    display_winner(act_tournament)
    os.remove("savegame")
    # sleep(10000)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Challenge en cours')
pygame.mouse.set_visible(0)

if os.path.isfile("savegame"):
    f = open("savegame", "rb")
    tournament = pickle.load(f)
    for c in tournament.challengers_pool:
        c.reload_image()
    f.close()
else:
    tournament = tournament.Tournament(tournament_type="deux_tours_pool_plus_qualif", pool_rounds=9)

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((0, 0, 0))
windowSurface.blit(background, (0, 0))

pygame.display.flip()
initial_game_state = "entering"
game_loop(initial_game_state, tournament)
