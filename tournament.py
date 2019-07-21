# coding=utf-8
import pickle
import random
from typing import Optional

import challenger
import tree
import json

from TournamentGroup import Group


class Tournament:
    def __init__(self, tournament_type="elimination directe", pool_rounds=0):
        self.CONNEXITY_THRESHOLD = 3
        self.seen_duels = {}
        self.actual_round = -1
        self.tournament_type = tournament_type
        self.actual_group = None
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

    def __handle_even_places_to_fill(self, places_to_fill, people_who_want_it, max_authorized):
        # TODO : clean, refactor and refactor this code
        if places_to_fill % 2 == 0:
            pre_qualification_nbr = (people_who_want_it / places_to_fill) / 2
            sub_calif_groups = []
            for i in range(0, pre_qualification_nbr, 2):
                sub_calif_groups.append(Group([], "Qualification"))
                sub_calif_groups[i].add_challenger(self.challengers_pool[max_authorized - places_to_fill + i])
                sub_calif_groups[i].add_challenger(self.challengers_pool[max_authorized - places_to_fill + i + 1])
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

    def __handle_multiples_three_who_want_it(self, places_to_fill, people_who_want_it, max_authorized):
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
        self.actual_round = -1

        self.tournament_type = "deux_parmi_trois"
        self.pool_round = pre_qualification_nbr

    def __handle_qualifications(self, max_authorized=4) -> None:
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
                    self.__handle_even_places_to_fill(places_to_fill, people_who_want_it, max_authorized)
                elif people_who_want_it % 3 == 0 and places_to_fill % 2 == 0:
                    self.__handle_multiples_three_who_want_it(places_to_fill, people_who_want_it, max_authorized)
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
            self.actual_round = -1
            self.tournament_type = "elimination directe"

    def __distribute_challengers(self):
        """
            Add challengers from the pool rounds into direct elimination part of the tree and change mode
        """
        for i in range(self.pool_round):
            self.ka.add_challenger(self.groups[i].challengers[0])
            self.ki.add_challenger(self.groups[i].challengers[1])
        self.tournament_type = "elimination directe"

    def get_next_group(self, is_valid=True) -> Optional[Group]:
        """
            Get the next group in the tournament tree depending on the tournament type
        :return: the next playing group
        """
        if self.actual_round < len(self.groups) - 1:
            if self.actual_round >= 0 or self.tournament_type == "randomized pool":
                if self.tournament_type == "elimination directe":
                    if not is_valid:
                        return self.actual_group
                    actual_node = self.tournament_tree.search_node(self.actual_group)
                    if actual_node.get_parent() is not None:
                        actual_node.get_parent().get_value().add_challenger(self.actual_group.winner)
                        self.rattrapages.add_challenger(self.actual_group.loser)
                elif self.tournament_type == "deux_tours_pool_plus_qualif":
                    self.actual_group.sort_challengers_by_points()
                    self.actual_group.challengers[0].add_points(4 - self.actual_group.challenger_number)
                    for k in range(self.actual_group.challenger_number):
                        self.challengers_pool[self.challengers_pool.index(self.actual_group.challengers[k])] \
                            .add_points(self.actual_group.challenger_number - k)
                    if self.actual_round == self.pool_round - 1:
                        self.__handle_qualifications()
                elif self.tournament_type == "deux_parmi_trois":
                    self.actual_group.remove_challenger(self.actual_group.loser)
                    if self.actual_round == self.pool_round - 1:
                        self.__distribute_challengers()
                elif self.tournament_type == "randomized pool":
                    min_connected = self._get_min_connected_node()
                    if min_connected < self.CONNEXITY_THRESHOLD:
                        self.actual_round = min(self.actual_round + 1, 1)
                        return self._handle_get_next_group_rand(is_valid)
                    else:
                        self.__distribute_challengers_rand()

            self.actual_round += 1
            self.actual_group = self.groups[self.actual_round]
            return self.actual_group
        else:
            return None

    def get_rounds(self):
        return self.actual_round

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
            i = 0
            for i, group in enumerate(self.groups):
                if group.get_title() == act_name:
                    break

            for n in g["Members"]:
                self.groups[i].add_challenger(self.challengers[n])
            for n in g["SubGroup"]:
                k = 0
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

        self.tournament_tree.depth = d + 1
        # self.tournament_tree.print()
        self.challengers_pool = list(self.challengers.values())

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
        return

    def _handle_get_next_group_rand(self, is_valid=True):
        if self.actual_round > 0 and is_valid:
            duel = self.actual_group.winner, self.actual_group.loser
            if self.actual_group.winner not in self.seen_duels.keys():
                self.seen_duels[self.actual_group.winner] = []
            if self.actual_group.loser not in self.seen_duels.keys():
                self.seen_duels[self.actual_group.loser] = []
            self.seen_duels[self.actual_group.winner].append(duel)
            self.seen_duels[self.actual_group.loser].append(duel)
            self.actual_group.winner.add_points(self.actual_group.get_points(self.actual_group.winner))
            self.actual_group.loser.add_points(self.actual_group.get_points(self.actual_group.loser))
        new_duelist = {}
        second_choice_duelists = {}
        total_weights = 0
        max_weight = 0
        for d in self.challengers.keys():
            if self.challengers[d] not in list(self.seen_duels.keys()):
                new_duelist[d] = 1
                total_weights += 1
            elif len(self.seen_duels) >= len(self.challengers) - 1:
                if len(self.seen_duels[self.challengers[d]]) < 3:
                    this_weight = len(self.seen_duels[self.challengers[d]])
                    total_weights += this_weight
                    new_duelist[d] = this_weight
                    max_weight = max(this_weight, max_weight)
                else:
                    second_choice_duelists[d] = 1

        if len(self.seen_duels) < len(self.challengers):
            duelist1 = list(new_duelist.keys())[random.randrange(0, len(new_duelist))]
            duelist2 = duelist1
            while duelist2 == duelist1:
                duelist2 = list(new_duelist.keys())[random.randrange(0, len(new_duelist))]
            self.actual_group = Group([self.challengers[duelist1], self.challengers[duelist2]], "Poule aléatoire")
        elif self.pool_round * 2 * len(self.challengers) >= len(self.seen_duels):
            first = self.get_rand(total_weights, max_weight + 2, new_duelist)
            second = first
            tries = 0
            while (first == second or (first, second) in self.seen_duels[self.challengers[first]] or (second, first) in
                   self.seen_duels[self.challengers[first]]) and tries < 1000:
                second = self.get_rand(total_weights, max_weight + 2, new_duelist)
                tries += 1
            while first == second or (first, second) in self.seen_duels[self.challengers[first]] or (second, first) in \
                    self.seen_duels[self.challengers[first]]:
                second = self.get_rand(len(second_choice_duelists), 3, second_choice_duelists)

            self.actual_group = Group([self.challengers[first], self.challengers[second]], "Poule aléatoire")

        return self.actual_group

    @staticmethod
    def get_rand(total_weights: int, max_weight: int, val_dict: dict):
        first = random.randrange(0, total_weights)
        first_index = 0
        while first > max_weight - val_dict[list(val_dict.keys())[first_index]]:
            first -= val_dict[list(val_dict.keys())[first_index]]
            first_index += 1
        return list(val_dict.keys())[first_index]

    def _get_min_connected_node(self):
        if len(self.seen_duels) == 0:
            return 0
        min_connection = len(self.challengers)
        for c in self.challengers_pool:
            if c in self.seen_duels.keys() and len(self.seen_duels[c]) < min_connection:
                min_connection = len(self.seen_duels[c])
            elif c not in self.seen_duels.keys():
                min_connection = 0
        return min_connection

    def __distribute_challengers_rand(self):
        self.pool_round = 2
        self.sort_challengers_by_score()
        pool1 = Group(self.challengers_pool[:2])
        pool2 = Group(self.challengers_pool[2:4])
        self.ki = self.groups[0]
        self.ka = self.groups[1]
        self.igitsa = self.groups[2]
        self.groups = [pool1, pool2] + self.groups
        self.__distribute_challengers()
        self.actual_round = 1
