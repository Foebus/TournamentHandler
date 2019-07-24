import random
import os
import pygame


class MusicHandler:
    def __init__(self, music_home="Music"):
        self.music = {
            "general": 'Music/piou.mp3',
            "STR": 'Music/dizi3.mp3',
            "Course": 'Music/clairon2-44.mp3',
            "Plateforme": 'Music/shooting-44.mp3',
            "Combat": 'Music/bongo-44.mp3',
            "Puzzle": 'Music/rythmBrum.mp3',
        }
        self.citations = {}
        for root, dirs, files in os.walk(music_home):
            self.citations[root] = files

    def start_loop(self, genre: str):
        pygame.mixer.music.load(self.music[genre])
        pygame.mixer.music.play(-1)

    @staticmethod
    def stop_music():
        pygame.mixer.music.stop()

    def start_quote(self, source_dir: str):
        chosen = random.randrange(0, len(self.citations[source_dir]))
        pygame.mixer.music.load(os.path.join(source_dir, self.citations[source_dir][chosen]))
        pygame.mixer.music.play(1)
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    def test_quotes(self):
        for folder, files in self.citations.items():
            if folder != "Music" and "broken" not in folder:
                for f in files:
                    pygame.mixer.music.load(os.path.join(folder, f))
                    pygame.mixer.music.play(1)
                    while pygame.mixer.music.get_busy():
                        pygame.time.Clock().tick(10)
