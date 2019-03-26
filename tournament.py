# coding=utf-8
import pickle
from typing import Optional

import challenger
import tree
import json

from TournamentGroup import Group


class Tournament:
    def __init__(self, tournament_type="elimination directe", pool_rounds=0):
        self.doneRound = -1
        self.tournament_type = tournament_type
        self.challengers = {}
        self.challengers_pool = []
        self.pool_round = pool_rounds
        self.ka = Group([], "Demi-Finale")
        self.ki = Group([], "Demi-Finale")
        self.igitsa = Group([], "Finale")
        self.calif = []
        self.groups = []
        self.tournament_tree = tree.Tree(initial_value=self.igitsa, depth=5)
        self.tournament_tree.get_root().add_child(self.ki)
        self.tournament_tree.get_root().add_child(self.ka)
        self.rattrapages = Group([], "Rattrapages")

    def handle_even_places_to_fill(self, places_to_fill, people_who_want_it, max_authorized):
        # TODO : clean, refactor and refactor this code
        if places_to_fill % 2 == 0:
            pre_qualification_nbr = (people_who_want_it / places_to_fill) / 2
            sub_calif_groups = []
            for i in range(0, pre_qualification_nbr, 2):
                sub_calif_groups.append(Group([], "Qualification"))
                sub_calif_groups[i].add_challenger(self.challengers_pool[max_authorized -
                                                                         places_to_fill + i])
                sub_calif_groups[i].add_challenger(self.challengers_pool[max_authorized -
                                                                         places_to_fill + i + 1])
                if i % 2 == 0:
                    self.tournament_tree.search_node(self.ki)[0].add_child(sub_calif_groups[i])
                else:
                    self.tournament_tree.search_node(self.ka)[0].add_child(sub_calif_groups[i])
                self.calif.append(sub_calif_groups[i])
        else:
            pre_qualification_nbr = (people_who_want_it / places_to_fill) / 2
            sub_calif_groups = []
            calif_groups = []
            for i in range(max(pre_qualification_nbr / 2, 1)):
                calif_groups.append(Group([], "Qualification, deuxième fournée"))
                if i % 2 == 0:
                    self.tournament_tree.search_node(self.ki)[0].add_child(calif_groups[i])
                else:
                    self.tournament_tree.search_node(self.ka)[0].add_child(calif_groups[i])
                self.calif.append(calif_groups[i])
            for i in range(pre_qualification_nbr):
                sub_calif_groups.append(Group([], "Qualification, " + str(people_who_want_it) +
                                              " challengers se disputent " + str(places_to_fill) + " places"))
                sub_calif_groups[i].add_challenger(self.challengers_pool[max_authorized -
                                                                         places_to_fill + i * 2])
                sub_calif_groups[i].add_challenger(self.challengers_pool[max_authorized -
                                                                         places_to_fill + i * 2 + 1])

                self.tournament_tree.search_node(calif_groups[i % len(calif_groups)])[0].add_child(
                    sub_calif_groups[i])
                self.calif.insert(0, sub_calif_groups[i])

    def handle_multiples_three_who_want_it(self, places_to_fill, people_who_want_it, max_authorized):
        # TODO : clean, refactor and refactor this code
        pre_qualification_nbr = people_who_want_it / 3
        calif_groups = []
        for i in range(pre_qualification_nbr):
            calif_groups.append(Group([], "Qualification, " + str(people_who_want_it) +
                                          " challengers se disputent " + str(places_to_fill) + " places"))
            if i % 2 == 0:
                self.tournament_tree.search_node(self.ki)[0].add_child(calif_groups[i])
            else:
                self.tournament_tree.search_node(self.ka)[0].add_child(calif_groups[i])
            self.calif.append(calif_groups[i])
            calif_groups[i].add_challenger(self.challengers_pool[max_authorized - places_to_fill + i * 3])
            calif_groups[i].add_challenger(self.challengers_pool[max_authorized -
                                                                 places_to_fill + i * 3 + 1])
            calif_groups[i].add_challenger(self.challengers_pool[max_authorized -
                                                                 places_to_fill + i * 3 + 2])
        self.calif.append(self.ka)
        self.calif.append(self.ki)
        self.calif.append(self.igitsa)
        self.groups = self.calif
        self.doneRound = -1

        self.tournament_type = "deux_parmi_trois"
        self.pool_round = pre_qualification_nbr

    def handle_qualifications(self, max_authorized=4) -> None:
        # TODO : clean, refactor and refactor this code
        """
            Handles the qualification until the point where there are almost no more challengers
        :param max_authorized: The max number of people to let go after this qualification phase
        """
        if not self.calif:
            self.sort_challengers_by_score()

            if self.challengers_pool[max_authorized - 1].points == self.challengers_pool[max_authorized].points:
                places_to_fill = 1
                while self.challengers_pool[max_authorized - 1].points == \
                        self.challengers_pool[max_authorized - places_to_fill - 1].points:
                    places_to_fill += 1
                people_who_want_it = places_to_fill
                while self.challengers_pool[max_authorized - places_to_fill].points == \
                        self.challengers_pool[max_authorized - places_to_fill + people_who_want_it].points:
                    people_who_want_it += 1

                for i in range(max_authorized - places_to_fill):
                    if i % 2 == 0:
                        self.ka.add_challenger(self.challengers_pool[i])
                    else:
                        self.ki.add_challenger(self.challengers_pool[i])

                #  Handles the qualification depending from the analysed conditions
                if (people_who_want_it / places_to_fill) % 2 == 0 and places_to_fill <= 4:
                    self.handle_even_places_to_fill(places_to_fill, people_who_want_it, max_authorized)
                elif people_who_want_it % 3 == 0 and places_to_fill % 2 == 0:
                    self.handle_multiples_three_who_want_it(places_to_fill, people_who_want_it, max_authorized)
                    return
                else:
                    print("I'm not built for this case, handle it yourself!")
            else:
                for j in range(0, max_authorized - 1, 2):
                    self.ka.add_challenger(self.challengers_pool[j])
                    self.ki.add_challenger(self.challengers_pool[j + 1])
            self.calif.append(self.ka)
            self.calif.append(self.ki)
            self.calif.append(self.igitsa)
            self.groups = self.calif
            self.doneRound = -1
            self.tournament_type = "elimination directe"

    def distribute_challengers(self):
        """
            Add challengers from the pool rounds into direct elimination part of the tree and change mode
        """
        for i in range(self.pool_round):
            self.ka.add_challenger(self.groups[i].challengers[0])
            self.ki.add_challenger(self.groups[i].challengers[1])
        self.tournament_type = "elimination directe"

    def get_next_group(self) -> Optional[Group]:
        """
            Get the next group in the tournament tree
        :return: the next playing group
        """
        if self.doneRound < len(self.groups) - 1:
            if self.doneRound >= 0:
                if self.tournament_type == "elimination directe":
                    node = self.tournament_tree.search_node(self.groups[self.doneRound])[0]
                    if node.get_parent() is not None:
                        node.get_parent().get_value().add_challenger(node.get_value().winner)
                        self.rattrapages.add_challenger(node.get_value().loser)
                elif self.tournament_type == "deux_tours_pool_plus_qualif":
                    self.groups[self.doneRound].sort_challengers_by_points()
                    self.groups[self.doneRound].challengers[0].add_points(4 -
                                                                          self.groups[self.doneRound].challengerNumber)
                    for k in range(self.groups[self.doneRound].challengerNumber):
                        self.challengers_pool[self.challengers_pool.index(self.groups[self.doneRound].challengers[k])] \
                            .add_points(self.groups[self.doneRound].challengerNumber - k)
                    if self.doneRound == self.pool_round-1:
                        self.handle_qualifications()
                elif self.tournament_type == "deux_parmi_trois":
                    self.groups[self.doneRound].remove_challenger(self.groups[self.doneRound].loser)
                    if self.doneRound == self.pool_round-1:
                        self.distribute_challengers()
            self.doneRound += 1
            return self.groups[self.doneRound]
        else:
            return None

    def get_rounds(self):
        return self.doneRound

    def extract_from_json(self, file_path: str) -> None:
        """
            Extract the configuration of a tournament and all its objects (challengers and groups) from a specified json
        :param file_path: string specifying where to find the configuration json
        """
        conf_file = open(file_path, 'r')
        content = json.load(conf_file)

        #  Get the type of the tournament
        self.tournament_type = content["Tournament type"]

        #  Get the challenger names
        for c in content["Challengers"]:
            self.challengers[c["Name"]] = challenger.Challenger(c["Name"], c["Image"])

        #  Then get the groups, fill those as well as the subgroups
        for g in content["Groups"]:
            act_name = g["Name"]
            if not any(group.get_title() == act_name for group in self.groups):
                self.groups.append(Group([], act_name))

            # Find matching index
            for i, group in enumerate(self.groups):
                if group.get_title() == act_name:
                    break

            for n in g["Members"]:
                self.groups[i].add_challenger(self.challengers[n])
            for n in g["SubGroup"]:
                for k, group in enumerate(self.groups):
                    if group.get_title() == n:
                        break
                self.groups[i].add_subgroup(self.groups[k])
            if "Final" in g:
                self.tournament_tree = tree.Tree(initial_value=self.groups[i])

        #  Then create the tournament tree
        root_group = self.tournament_tree.get_root()
        elem = {root_group: root_group.get_value().get_subgroups()}
        future_elem = {}
        passed_elem = []
        d = 0
        while len(elem) > 0:
            for p, g in elem.items():
                for e in g:
                    for group in self.groups:
                        if group.get_title() == e:
                            e = group
                            break
                    if e not in passed_elem:
                        new_node = p.add_child(e)
                        if e.get_subgroups() is not None:
                            future_elem[new_node] = e.get_subgroups()
                passed_elem.append(p)
            elem = future_elem
            future_elem = {}
            d += 1

        self.tournament_tree.depth = d
        # self.tournament_tree.print()
        self.challengers_pool = self.challengers.values()

    def sort_challengers_by_score(self) -> None:
        """
            Sorts the challengers based on their actual score
        """
        done = False

        while not done:
            done = True
            for i in range(len(self.challengers_pool) - 1):
                if self.challengers_pool[i].points < self.challengers_pool[i + 1].points:
                    done = False
                    tmp = self.challengers_pool[i]
                    self.challengers_pool[i] = self.challengers_pool[i + 1]
                    self.challengers_pool[i + 1] = tmp

    def save_yourself(self):
        """
            Saves the actual state of the game into a file named "savegame"
        """
        for c in self.challengers_pool:
            c.unload_image()
        with open("savegame", "wb") as saveFile:
            pickle.dump(self, saveFile)
        for c in self.challengers_pool:
            c.reload_image()
