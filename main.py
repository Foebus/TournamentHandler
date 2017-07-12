import pygame
import sys
import tournament
from pygame.locals import *

pygame.init()
WIDTH = 1280
HEIGHT = 780
FONT_SIZE = 36
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
    font = pygame.font.Font(None, FONT_SIZE)
    challenger_number = actual_challengers_to_display.challengerNumber
    point_rectangle = Rect(0, act_height + FONT_SIZE/2, WIDTH, FONT_SIZE)
    pointSurface.blit(point_rubber, point_rectangle)
    for i in range(challenger_number):
        points = font.render(str(actual_challengers_to_display.get_points(i)), 1, (255, 0, 0))
        point_pos = points.get_rect(centerx=windowSurface.get_width() * (2 * i + 1) / (challenger_number*2),
                                    centery=act_height + FONT_SIZE)
        pointSurface.blit(points, point_pos)
    pygame.display.update(point_rectangle)


def display_challengers(actual_challengers_to_display):
    font = pygame.font.Font(None, FONT_SIZE)
    challenger_number = actual_challengers_to_display.challengerNumber
    challengerSurface.blit(challenger_rubber, (0, 0))
    max_height = 0
    for i in range(challenger_number):
        act_width = actual_challengers_to_display.challengers[i].image.get_width()
        scale_ratio = float(WIDTH) / (challenger_number*act_width)
        act_height = actual_challengers_to_display.challengers[i].image.get_height()
        actual_challengers_to_display.challengers[i].rescale_image(int(act_width*scale_ratio),
                                                                   int(act_height*scale_ratio))
        act_height = actual_challengers_to_display.challengers[i].image.get_height()
        challenger_image = actual_challengers_to_display.challengers[i].image
        challengerSurface.blit(challenger_image, (i * challenger_image.get_width(), 0))
        pseudo = font.render(actual_challengers_to_display.challengers[i].name, 1, (10, 90, 10))
        text_pos = pseudo.get_rect(centerx=windowSurface.get_width() * (2*i+1) / (challenger_number*2),
                                   centery=challenger_image.get_height() + FONT_SIZE)
        challengerSurface.blit(pseudo, text_pos)
        max_height = max(max_height, act_height)

    for i in range(challenger_number-1):
        challengerSurface.blit(lightning, ((i+1) * act_width * scale_ratio - lightning.get_width()/2, 0))
    update_score_display(actual_challengers_to_display, max_height+FONT_SIZE)
    group = font.render(actual_challengers_to_display.title, 1, (0, 0, 250))
    text_pos = group.get_rect(centerx=windowSurface.get_width() / 2,
                              centery=50)
    challengerSurface.blit(group, text_pos)

    challengers_rectangle = Rect(0, 0, WIDTH, HEIGHT)
    pygame.display.update(challengers_rectangle)
    return max_height + FONT_SIZE


def game_loop(game_state, act_tournament):
    round_over = False
    actual_challengers = act_tournament.get_next_group()
    height = display_challengers(actual_challengers)
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

        if round_over:
            round_over = False
            actual_challengers = act_tournament.get_next_group()
            if actual_challengers is None:
                game_state = "gameover"
            else:
                height = display_challengers(actual_challengers)
        pygame.time.delay(1000)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Challenge en cours')
pygame.mouse.set_visible(0)

tournament = tournament.Tournament(tournament_type="deux_tours_pool_plus_qualif", pool_rounds=8)

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((0, 0, 0))
windowSurface.blit(background, (0, 0))

pygame.display.flip()
initial_gamestate = "entering"
game_loop(initial_gamestate, tournament)
