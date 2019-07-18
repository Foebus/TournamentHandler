import random
from enum import Enum

import pygame
from pygame.locals import *

from challenge import Test
from tournament import Group, Tournament

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

objectiveSurface = pygame.display.set_mode((WIDTH, HEIGHT))

lightning = pygame.image.load("Images/eclair.png")
group_name_background = pygame.display.set_mode((WIDTH, FONT_SIZE))
group_name_background = group_name_background.convert()
group_name_background.fill((0, 0, 0))

orig_arrow = pygame.image.load("Images/arrow.png")
orig_arrow = pygame.transform.scale(orig_arrow, (399, 219))


class WheelKind(Enum):
    GENRE, COMBAT, COURSE, PLATEFORME, PUZZLE, STR, FPS = 0, 1, 2, 3, 4, 5, 6


wheel_information = {
    WheelKind.GENRE: (Test.GENRE, pygame.image.load("Images/Roue_Type.png")),
    WheelKind.COMBAT: (Test.GAME["Combat"], pygame.image.load("Images/Roue_Combat.png")),
    WheelKind.COURSE: (Test.GAME["Course"], pygame.image.load("Images/Roue_Course.png")),
    WheelKind.PLATEFORME: (Test.GAME["Plateforme"], pygame.image.load("Images/Roue_Plateforme.png")),
    WheelKind.PUZZLE: (Test.GAME["Puzzle"], pygame.image.load("Images/Roue_Puzzle.png")),
    WheelKind.STR: (Test.GAME["STR"], pygame.image.load("Images/Roue_STR.png"))
}


def update_score_display(actual_challengers_to_display: Group):
    """

    :param actual_challengers_to_display: The group of challengers whose name to display
    """
    font = pygame.font.Font(None, FONT_SIZE)
    challenger_number = actual_challengers_to_display.challenger_number
    point_rectangles = []  # Rect(0, act_height + FONT_SIZE / 2, WIDTH, FONT_SIZE)
    pointSurface.blit(point_rubber, pointSurface.get_rect(left=0, top=POINT_HEIGHT))
    for i in range(challenger_number):
        point_rectangles.append(Rect((2 * i + 1) * WIDTH / (2 * challenger_number) -
                                     len(str(actual_challengers_to_display.get_points(i))) * FONT_SIZE / 2,
                                     POINT_HEIGHT,
                                     len(str(actual_challengers_to_display.get_points(i))) * FONT_SIZE,
                                     FONT_SIZE))
        points = font.render(str(actual_challengers_to_display.get_points(i)), 1, (255, 0, 0))
        point_pos = points.get_rect(centerx=pointSurface.get_width() * (2 * i + 1) / (challenger_number * 2),
                                    top=POINT_HEIGHT)
        pointSurface.blit(points, point_pos)
        pygame.display.update(point_rectangles[i])


def display_text(pos_x, pos_y, content, surface, associated_rubber=None, text_color=(255, 241, 0), erase_line=False,
                 font_size=FONT_SIZE):
    font = pygame.font.Font(None, font_size)
    rendered_content = font.render(content, 1, text_color)
    text_pos = rendered_content.get_rect(left=pos_x, top=pos_y)

    title_place = Rect(pos_x, pos_y, len(content) * font_size, font_size) if not erase_line else Rect(0, pos_y, WIDTH,
                                                                                                      font_size)
    if associated_rubber is not None:
        associated_rubber.fill((0, 0, 0))
        surface.blit(associated_rubber, title_place)
    surface.blit(rendered_content, text_pos)

    pygame.display.update(title_place)


def display_challengers(actual_challengers_to_display: Group):
    """

    :param actual_challengers_to_display: the challenger group to display
    """
    challenger_number = actual_challengers_to_display.challenger_number

    challengerSurface.blit(challenger_rubber, (0, 0))
    wanted_challenger_width = WIDTH * 2 // 3
    max_height = 0
    #  Displays challengers
    for i in range(challenger_number):
        act_challenger = actual_challengers_to_display.challengers[i]
        challenger_image = act_challenger.image

        old_width = challenger_image.get_width()
        old_height = challenger_image.get_height()
        scale_ratio = float(wanted_challenger_width) / (challenger_number * old_width)
        act_challenger.rescale_image(int(old_width * scale_ratio), int(old_height * scale_ratio))

        challenger_image = act_challenger.image
        act_height = challenger_image.get_height()
        act_width = challenger_image.get_width()
        challengerSurface.blit(challenger_image, (
            i * WIDTH / challenger_number + (WIDTH / challenger_number - act_width) / 2, POINT_HEIGHT + FONT_SIZE))

        display_text(
            challengerSurface.get_width() * (2 * i + 1) / (2 * challenger_number) - FONT_SIZE * len(
                act_challenger.name) / 4, 2 * FONT_SIZE,
            act_challenger.name, challengerSurface, text_color=(60, 140, 60), erase_line=False)
        max_height = max(max_height, act_height)
    update_score_display(actual_challengers_to_display)
    #  Display lightnings between challengers
    for i in range(challenger_number - 1):
        challengerSurface.blit(lightning, ((i + 1) * WIDTH / challenger_number - lightning.get_width() / 2, 0))

    #  Display title
    display_text(pos_x=WIDTH / 2 - len(str(actual_challengers_to_display.title)) * FONT_SIZE / 2, pos_y=15,
                 content=actual_challengers_to_display.title, surface=challengerSurface)

    challengers_rectangle = Rect(0, 0, WIDTH, HEIGHT)
    pygame.display.update(challengers_rectangle)
    return max_height + FONT_SIZE


def display_winner(ended_tournament: Tournament):
    """

    :param ended_tournament: The tournament where to find the winner
    """
    reset_display()
    winner = ended_tournament.groups[len(ended_tournament.groups) - 1].winner
    font = pygame.font.Font(None, FONT_SIZE)
    act_width = winner.image.get_width()
    act_height = winner.image.get_height()
    scale_ratio = float(HEIGHT) / act_height
    winner.rescale_image(int(act_width * scale_ratio),
                         int(act_height * scale_ratio))
    challenger_image = winner.image
    challengerSurface.blit(challenger_image, (0, 0))
    pseudo = font.render(
        "Bravo, " + winner.name + " pour ta victoire \n\r on peut clairement dire que tu roxes du poney!!",
        1, (10, 90, 10))
    text_pos = pseudo.get_rect(centerx=windowSurface.get_width() / 2,
                               centery=challenger_image.get_height() - FONT_SIZE * 3)
    challengerSurface.blit(pseudo, text_pos)
    challengers_rectangle = Rect(0, 0, WIDTH, HEIGHT)
    pygame.display.update(challengers_rectangle)


def spin_wheel(kind, objective):
    data, image = wheel_information[WheelKind[kind]]
    side = min(WIDTH, HEIGHT)
    image = pygame.transform.scale(image, (side, side))
    image_background = pygame.Surface((WIDTH, HEIGHT))
    image_background.fill((0, 0, 0))
    image_background.blit(image,
                          ((WIDTH - side) / 2, (HEIGHT - side) / 2))  # (image.get_width(), POINT_HEIGHT + FONT_SIZE))
    for index, val in enumerate(data):
        if objective in val:
            animate_arrow_rotation(index / len(data), windowSurface, image_background)
            return


def animate_arrow_rotation(goal, window_surface, background=None, center_x=WIDTH // 2, center_y=HEIGHT // 2):
    clock = pygame.time.Clock()

    goal_rotation = goal * 360
    acceleration_time = random.randrange(50, 100)
    max_speed_time = random.randrange(100, 200)
    deceleration_time = 180

    rot = 0
    max_rot_speed = 20

    image = orig_arrow.copy()
    image.set_colorkey((0, 0, 0))
    rect = image.get_rect()
    rect.center = (center_x, center_y)

    rot = spin_image(window_surface, clock, rect, rot, acceleration_time,
                     acceleration=lambda x, y: x + (max_rot_speed * y) / acceleration_time, background=background)
    rot = spin_image(window_surface, clock, rect, rot, max_speed_time, acceleration=lambda x, y: x + max_rot_speed,
                     background=background, stop_at_click=True)
    rot = rot % 360
    deceleration_time = int(((2 * (goal_rotation - rot)) / max_rot_speed)) % 360
    if deceleration_time == 0:
        deceleration_time = 90
    spin_image(window_surface, clock, rect, rot, deceleration_time,
               acceleration=lambda x, y: x + max_rot_speed * (deceleration_time - y) / deceleration_time,
               background=background)


def spin_image(surface, clock, rect, init_rot, total_time, acceleration=lambda x, y: x, stop_at_click=False,
               background=None):
    fps = 30
    time_counter = 0
    black = (0, 0, 0)
    rot = init_rot
    running = True
    while running:
        clock.tick(fps)
        surface.fill(black)
        old_center = rect.center
        # définir angle de rotation
        rot = acceleration(rot, time_counter)
        # roter l'image originale
        new_image = pygame.transform.rotate(orig_arrow, rot)
        rect = new_image.get_rect()
        rect.center = old_center
        if background is not None:
            surface.blit(background, (0, 0))
        surface.blit(new_image, rect)
        pygame.display.flip()

        events = pygame.event.get()
        for event in events:
            if event.type == MOUSEBUTTONUP and stop_at_click:
                running = False

        if time_counter == total_time:
            running = False
        time_counter += 1
    return rot


def reset_display():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    background = pygame.Surface(screen.get_size())
    background.fill((0, 0, 0))
    windowSurface.blit(background, (0, 0))
