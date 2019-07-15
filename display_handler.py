import random

import pygame
from pygame.locals import *
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
orig_arrow = pygame.transform.scale(orig_arrow, (133, 73))


def update_score_display(actual_challengers_to_display: Group):
    """

    :param act_height: The height of the lowest image
    :type act_height: int
    :param actual_challengers_to_display: The group of challengers whose name to display
    :type actual_challengers_to_display: TournamentGroup.Group
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


def display_text(pos_x, pos_y, content, surface, associated_rubber=None, text_color=(255, 241, 0), erase_line=False):
    font = pygame.font.Font(None, FONT_SIZE)
    rendered_content = font.render(content, 1, text_color)
    text_pos = rendered_content.get_rect(left=pos_x, top=pos_y)

    title_place = Rect(pos_x, pos_y, len(content) * FONT_SIZE, FONT_SIZE) if not erase_line else Rect(0, pos_y, WIDTH,
                                                                                                      FONT_SIZE)
    if associated_rubber is not None:
        associated_rubber.fill((0, 0, 0))
        surface.blit(associated_rubber, title_place)
    surface.blit(rendered_content, text_pos)

    pygame.display.update(title_place)


def display_challengers(actual_challengers_to_display: Group):
    """

    :param actual_challengers_to_display: the challenger group to display
    """
    font = pygame.font.Font(None, FONT_SIZE)
    challenger_number = actual_challengers_to_display.challenger_number
    challengerSurface.blit(challenger_rubber, (0, 0))
    max_height = 0
    old_width = 0
    scale_ratio = 1
    #  Displays challengers
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
    update_score_display(actual_challengers_to_display)
    #  Display lightnings between challengers
    for i in range(challenger_number - 1):
        challengerSurface.blit(lightning, ((i + 1) * old_width * scale_ratio - lightning.get_width() / 2, 0))

    group = font.render(actual_challengers_to_display.title, 1, (255, 241, 0))
    text_pos = group.get_rect(centerx=challengerSurface.get_width() / 2, top=5)
    title_pos_x = WIDTH / 2 - len(str(actual_challengers_to_display.title)) * FONT_SIZE / 2
    title_place = Rect(title_pos_x, 5, len(str(actual_challengers_to_display.title)) * FONT_SIZE, FONT_SIZE)
    challengerSurface.blit(group_name_background, text_pos)
    challengerSurface.blit(group, text_pos)
    pygame.display.update(title_place)

    challengers_rectangle = Rect(0, 0, WIDTH, HEIGHT)
    pygame.display.update(challengers_rectangle)
    return max_height + FONT_SIZE


def display_winner(ended_tournament: Tournament):
    """

    :param ended_tournament: The tournament where to find the winner
    :type ended_tournament: tournament.Tournament
    """
    reset_display()
    winner = ended_tournament.groups[len(ended_tournament.groups) - 1].winner
    font = pygame.font.Font(None, FONT_SIZE)
    act_width = winner.image.get_width()
    scale_ratio = float(WIDTH) / act_width
    act_height = winner.image.get_height()
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


def animate_arrow_rotation(goal, window_surface, center_x=WIDTH // 2, center_y=HEIGHT // 2):
    clock = pygame.time.Clock()

    goal_rotation = goal * 360
    acceleration_time = random.randrange(50, 100)
    max_speed_time = random.randrange(100, 200)
    deceleration_time = 180

    rot = 0
    max_rot_speed = 8

    image = orig_arrow.copy()
    image.set_colorkey((0, 0, 0))
    rect = image.get_rect()
    rect.center = (center_x, center_y)

    rot = spin_image(window_surface, clock, rect, rot, acceleration_time,
                     acceleration=lambda x, y: x + (max_rot_speed * y) / acceleration_time)
    rot = spin_image(window_surface, clock, rect, rot, max_speed_time, acceleration=lambda x, y: x + max_rot_speed)
    rot = rot % 360
    deceleration_time = ((2 * (goal_rotation - rot)) / max_rot_speed) % 360
    if deceleration_time == 0:
        deceleration_time = 90
    spin_image(window_surface, clock, rect, rot, deceleration_time,
               acceleration=lambda x, y: x + max_rot_speed * (deceleration_time - y) / deceleration_time)


def spin_image(surface, clock, rect, init_rot, total_time, acceleration=lambda x, y: x):
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
        surface.blit(new_image, rect)
        pygame.display.flip()

        if time_counter == total_time:
            running = False
        time_counter += 1
    return rot


def reset_display():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    background = pygame.Surface(screen.get_size())
    background.fill((0, 0, 0))
    windowSurface.blit(background, (0, 0))
