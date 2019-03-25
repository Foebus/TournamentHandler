import pygame


class Challenger:
    def __init__(self, name, image_path, initial_points=0):
        self.name = name
        self.image_path = image_path
        self.points = initial_points
        try:
            self.rawImage = pygame.image.load(image_path)
            self.image = self.rawImage
        except:
            self.rawImage = None
            self.image = None

    def rescale_image(self, width, height):
        if self.image is not None:
            self.image = pygame.transform.scale(self.rawImage, (width, height))

    def add_points(self, value):
        self.points += value

    def change_image(self, image_path):
        self.rawImage = pygame.image.load(image_path)
        self.image = self.rawImage

    def reload_image(self):
        self.change_image(self.image_path)

    def unload_image(self):
        self.rawImage = None
        self.image = None
