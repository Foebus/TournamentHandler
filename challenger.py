import pygame
from pygame.locals import *


class Challenger:
    def __init__(self, real_name, name, image_path, initial_points=0):
        self.name = name
        self.real_name = real_name
        self.change_image("Images/"+real_name+".png")
        self.points = initial_points

    def rescale_image(self, width, height):
        self.image = pygame.transform.scale(self.rawImage, (width, height))

    def add_points(self, value):
        self.points += value

    def change_image(self, image_path):
        self.rawImage = pygame.image.load(image_path)
        self.image = self.rawImage

    def reload_image(self):
        self.change_image("Images/"+self.real_name+".png")

    def unload_image(self):
        self.rawImage = None
        self.image = None
