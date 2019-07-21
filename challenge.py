import random


class Challenge:

    def __init__(self, total_points):
        self.total_points = total_points
        self.test = []
        test_generator = Test()
        seen_style = []
        while total_points > len(self.test):
            test, style, game = test_generator.create_test()
            if style not in seen_style:
                self.test.append((test, style, game))
                seen_style.append(style)
        self.act_test = self.test[0]

    def get_next_test(self):
        if len(self.test) > 0:
            self.act_test = self.test[0]
            self.test = self.test[1:]
            return self.act_test
        return None, None, None


class Test:
    GAME = {"STR": [
        ("Starcraft 2", "PC"),
        ("Warcraft 3", "PC", ["Duel sur une carte adaptée"]),
        ("Age of Mythology", "PC"),
        ("Starcraft", "PC"),
        ("Empire Earth", "PC"),
        ("Le seigneur des Anneaux", "PC"),
    ],
        "FPS": [("Unreal Tournament3", "PC"),
                ("Unreal Tournament 4", "PC")
                ],
        "Course": [
            ("Rock'N Roll Racing", "PC"),
            ("Mario Kart", "Wii"),
            ("Motor Storm", "PS3"),
        ],
        "Plateforme": [
            ("Super Meat Boy", "PC"),
            ("Axiom Verge", "PC"),
            ("Transistor", "PC"),
            ("Spelunky 2.0", "PC"),
            ("Pix The Cat", "PS4"),
            ("Rogue Legacy", "PS4"),
            ("Syobon Action", "PC"),
            ("Enter the Gungeon", "PC"),
            ("Spelunky", "PC"),
            ("City of Brass", "PC"),
        ],
        "Combat": [
            ("Injustice II", "PC"),
            ("Soul Calibur 5", "PS3"),
            ("Super Smash Bros", "Wii"),
            ("Injustice", "PS3"),
            ("Tekken", "PS3"),
            ("Super Smash Bros", "GameCube"),
            ("Soul Calibur 4", "PS3"),
            ("Dragonball Tenkaichi", "PS2"),
        ],
        "Puzzle": [
            ("Antichamber", "PC", ["trouver le deuxième gun"]),
            ("Baba is you", "PC", ["Faire les 7 premiers niveaux"]),
            ("McPixel", "PC", ["Finir un ensemble de 3 niveaux", "Accéder à un niveau bonus"]),
            ("Timbleweed Park", "PC", ["Finir un chapitre du jeu"])
        ]
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
                             "Puzzle": []
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

        handicap = "" if handicap == "" else "Handicap : " + handicap

        return (game + " sur " + console + "\n" +
                "Objectif : " + objective + "\n" +
                handicap, style, game)
