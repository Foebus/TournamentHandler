import pygame
from pygame.locals import *


class Challenger:
    def __init__(self, name, image_path, initial_points=0):
        self.name = name
        self.rawImage = pygame.image.load(image_path)
        self.image = self.rawImage.convert()
        self.points = initial_points

    def rescale_image(self, width, height):
        self.image = pygame.transform.scale(self.rawImage, (width, height))

    def add_points(self, value):
        self.points += value
