# coding=utf-8

import pygame
import sys
from tournament import Tournament, Group
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
group_name_background = pygame.display.set_mode((WIDTH, FONT_SIZE))
group_name_background = group_name_background.convert()
group_name_background.fill((0, 0, 0))


def update_score_display(actual_challengers_to_display, act_height = 0):
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


def display_text(pos_x, pos_y, content, size_x, size_y):
    font = pygame.font.Font(None, FONT_SIZE)
    group = font.render(content, 1, (255, 241, 0))
    text_pos = group.get_rect(centerx=challengerSurface.get_width() / 2, top=5)
    title_pos_x = WIDTH / 2 - len(content) * FONT_SIZE / 2
    title_place = Rect(pos_x, pos_y, len(content) * FONT_SIZE, FONT_SIZE)
    challengerSurface.blit(group_name_background, text_pos)
    challengerSurface.blit(group, text_pos)
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
    update_score_display(actual_challengers_to_display, max_height + FONT_SIZE)
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


def display_winner(ended_tournament):
    # type: (tournament) -> None
    """

    :param ended_tournament: The tournament where to find the winner
    :type ended_tournament: tournament.Tournament
    """
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


def animate_arrow_rotation():
    size = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)
    FPS = 30
    clock = pygame.time.Clock()
    BLACK = (0, 0, 0)
    time_counter = 0

    rot = 0
    rot_speed = 2

    image_orig = pygame.image.load("Images/arrow.jpeg")
    image = image_orig.copy()
    image.set_colorkey(BLACK)
    rect = image.get_rect()
    rect.center = (WIDTH // 2, HEIGHT // 2)

    running = True
    while running:
        clock.tick(FPS)
        windowSurface.fill(BLACK)
        old_center = rect.center
        # définir angle de rotation
        rot = (rot + rot_speed) % 360
        # roter l'image originale
        new_image = pygame.transform.rotate(image_orig, rot)
        rect = new_image.get_rect()
        rect.center = old_center
        windowSurface.blit(new_image, rect)
        pygame.display.flip()

        if time_counter == 300:
            running = False
        time_counter += 1


def handle_mouseclick(x, y, actual_challengers):
    (w, h) = pygame.display.get_surface().get_size()
    if y > h/5:
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
    height = display_challengers(actual_challengers)
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
                update_score_display(actual_challengers, height)
                test_over = True
            elif event.type == KEYDOWN and event.key == K_2:
                actual_challengers.give_point(1)
                update_score_display(actual_challengers, height)
                test_over = True
            elif event.type == KEYDOWN and event.key == K_3:
                actual_challengers.give_point(2)
                update_score_display(actual_challengers, height)
                test_over = True
            elif event.type == KEYDOWN and event.key == K_4:
                actual_challengers.give_point(3)
                update_score_display(actual_challengers, height)
                test_over = True
            elif event.type == KEYDOWN and event.key == K_5:
                actual_challengers.give_point(4)
                update_score_display(actual_challengers, height)
                test_over = True
            elif event.type == KEYDOWN and event.key == K_6:
                actual_challengers.give_point(5)
                update_score_display(actual_challengers, height)
                test_over = True
            elif event.type == KEYDOWN and event.key == K_7:
                actual_challengers.give_point(6)
                update_score_display(actual_challengers, height)
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
            points_given += 1
            if points_given == act_test.total_points:
                round_over = True
            else:
                objective, genre = act_test.get_next_test()
                objective = objective.split("\n")
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
    # sleep(10000)


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Challenge en cours')
#  pygame.mouse.set_visible(0)

if os.path.isfile("savegame"):
    pygame.display.set_caption('Sauvegarde trouvée, souhaitez-vous la charger?')

    decision_made = False
    while not decision_made:
        events = pygame.event.get()
        for event in events:
            if (event.type == KEYDOWN and event.key == K_n) or (event.type == KEYDOWN and event.key == K_ESCAPE):
                tournament = Tournament(tournament_type="deux_tours_pool_plus_qualif", pool_rounds=3)
                tournament.extract_from_json("tournament.json")
                decision_made = True
                break
            elif (event.type == KEYDOWN and event.key == K_y) or (event.type == KEYDOWN and event.key == K_INSERT):
                f = open("savegame", "rb")
                tournament = pickle.load(f)
                for c in tournament.challengers_pool:
                    c.reload_image()
                f.close()
                decision_made = True
else:
    tournament = Tournament(tournament_type="deux_tours_pool_plus_qualif", pool_rounds=3)
    tournament.extract_from_json("tournament.json")

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((0, 0, 0))
windowSurface.blit(background, (0, 0))

pygame.display.flip()
initial_game_state = "entering"
game_loop(initial_game_state, tournament)
