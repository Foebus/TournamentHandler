import random


class Challenge:

    def __init__(self, total_points):
        self.total_points = total_points
        self.test = []
        test_generator = Test()
        seen_style = []
        while total_points > len(self.test):
            test, style = test_generator.create_test()
            if style not in seen_style:
                self.test.append((test, style))
                seen_style.append(style)

    def get_next_test(self):
        if len(self.test) > 0:
            result = self.test[0]
            self.test = self.test[1:]
            return result
        return None, None


class Test:
    GAME = {"STR": [("Warcraft 3", "PC", ["Duel sur une carte adaptée"]),
                    ("Le seigneur des Anneaux", "PC"), ("Starcraft", "PC"),
                    ("Starcraft 2", "PC"), ("Empire Earth", "PC"), ("Age of Mythology", "PC"),
                    ("Age of Empire", "PC")],
            "FPS": [("Unreal Tournament3", "PC"), ("Far Cry 4", "PC"), ("Far cry primal", "PC"),
                    ("Unreal Tournament 4", "PC"), ("Metroid", "GameCube"),
                    ("Fortnite", "PC"), ("Overwatch", "PC")],
            "Course": [("Mario Kart", "Wii"), ("Rock'N Roll Racing", "PC"), ("Motor Storm", "PS3")],
            "Plateforme": [("Super Meat Boy", "PC"), ("Syobon Action", "PC"), ("Spelunky", "PC"),
                           ("Spelunky 2.0", "PC"), ("Pix The Cat", "PS4"), ("Mr Robot", "PS4"),
                           ("Transistor", "PC"), ("Axiom Verge", "PC"), ("City of Brass", "PC"),
                           ("Enter the Gungeon", "PC"), ("Rogue Legacy", "PS4")],
            "Combat": [("Injustice II", "PC"), ("Injustice", "PS3"), ("Soul Calibur 4", "PS3"),
                       ("Soul Calibur 5", "PS3"), ("Tekken", "PS3"), ("Dragonball Tenkaichi", "PS2"),
                       ("Super Smash Bros", "GameCube"), ("Super Smash Bros", "Wii")],
            "Puzzle": [("Antichamber", "PC"),
                       ("Journey", "PC"),
                       ("Baba is you", "PC"),
                       ("Prime number Labyrinth", "PC"),
                       ("McPixel", "PC"),
                       ("Timbleweed Park", "PC"),
                       ("Hearthstone", "PC")]
            }

    GENRE = {
        "Plateforme": 0,
        "STR": 1,
        "Course": 2,
        "Puzzle": 3,
        "Combat": 4,
        "FPS": 5
             }

    CHALLENGE_DESCRIPTION = {"STR": ["Duel", "Combat en Coop, celui qui a le meilleur score à la fin gagne",
                                     "Le premier à avoir amassé 500 de chaque type de ressource gagne"],
                             "FPS": ["Duel sur petite cart",
                                     "Celui qui survit le plus longtemps, pourchassé par le champion, 3 morts",
                                     "Capture de drapeau avec 5 bot par équipe en mode facile",
                                     "Co-op contre ordi niveau habitué, celui qui fait le plus de kill"
                                     ],
                             "Course": ["Course, celui qui met le moins de temps gagne!"],
                             "Plateforme": ["Scoring, 3 niveaux", "SpeedRun, 3 niveaux",
                                            "Scoring, 5 niveaux", "SpeedRun, 5 niveaux",
                                            "Scoring, 7 niveaux", "SpeedRun, 7 niveaux",
                                            "SpeedRun, 3 niveaux à 100%"],
                             "Combat": ["Premier à 3 victoires", "Premier à 5 victoires",
                                        "Premier à 7 victoires", "Survie contre le Champion, meilleur timer"],
                             "Puzzle": ["Passer les 5 premiers points de contrôle"]
                             }

    HANDICAP = {"PC": ["en ayant l'écran à l'envers", "en ayant la souris en mauvaise main", "à la trackball",
                       "en ayant l'écran tourné d'un quart de tour",
                       "avec un clavier Azerty (sans changer le mapping)",
                       "en ayant accès à l'écran de l'autre"],
                "PS2": ["avec la mannette à l'envers", "avec une seule main"],
                "PS3": ["avec la mannette à l'envers", "avec une seule main"],
                "PS4": ["avec la mannette à l'envers", "avec une seule main"],
                "Wii": ["avec le volant", "sans le nunchuk"],
                "GameCube": ["avec la mannette à l'envers", "avec une seule main"]
                }

    def create_test(self):
        style = list(self.GAME.keys())[random.randrange(0, len(self.GAME))]
        game_index = random.randrange(0, len(self.GAME[style]))
        game = self.GAME[style][game_index][0]
        console = self.GAME[style][game_index][1]
        specific_challenge = self.GAME[style][game_index][2] if len(self.GAME[style][game_index]) > 2 else []
        handicap = ""
        if random.random() > 0.9:
            handicap = self.HANDICAP[console][random.randrange(0, len(self.HANDICAP[console]))]

        possible_objective = self.CHALLENGE_DESCRIPTION[style] + specific_challenge

        objective = possible_objective[random.randrange(0, len(possible_objective))]

        handicap = "" if handicap == "" else "Mais vous devrez le faire " + handicap

        return ("Le Défi se fera sur " + game + " sur " + console + "\n" +
                "L'objectif sera " + objective + "\n" +
                handicap, style)
