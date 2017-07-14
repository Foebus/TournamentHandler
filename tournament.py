# coding=utf-8
import challenger
import tree


class Group:
    def __init__(self, members, title="unnamed"):
        self.challengers = members
        self.challengerNumber = len(members)
        self.scores = []
        self.title = title
        for i in range(self.challengerNumber):
            self.scores.append(0)

    def give_point(self, challenger_id, point_nbr=1):
        if challenger_id < self.challengerNumber:
            self.scores[challenger_id] += point_nbr

    def get_points(self, challenger_id):
        if challenger_id < self.challengerNumber:
            return self.scores[challenger_id]
        else:
            return 0

    def get_winner(self):
        index = 0
        for i in range(self.challengerNumber):
            if self.scores[i] > self.scores[index]:
                index = i
        return self.challengers[index]

    def get_loser(self):
        index = 0
        for i in range(self.challengerNumber):
            if self.scores[i] < self.scores[index]:
                index = i
        return self.challengers[index]

    def sort_challengers_by_points(self):
        order = []
        for i in range(self.challengerNumber):
            order.append(i)
        smthng_changed = True
        while smthng_changed:
            smthng_changed = False
            for i in range(self.challengerNumber - 1):
                if self.scores[i] < self.scores[i + 1]:
                    tmp = self.scores[i]
                    tmp_ord = order[i]
                    self.scores[i] = self.scores[i + 1]
                    order[i] = order[i + 1]
                    self.scores[i + 1] = tmp
                    order[i + 1] = tmp_ord
                    smthng_changed = True
        tmp_challengers = []
        for i in range(self.challengerNumber):
            tmp_challengers.append(self.challengers[i])
        for i in range(self.challengerNumber):
            self.challengers[i] = tmp_challengers[order[i]]
        return self.challengers

    def add_challenger(self, new_challenger, initialscore=0):
        self.challengers.append(new_challenger)
        self.challengerNumber += 1
        self.scores.append(initialscore)

    def remove_challenger(self, old_challenger):
        self.challengers.remove(old_challenger)


class Tournament:
    def __init__(self, tournament_type="elimination directe", pool_rounds=0):
        self.doneRound = -1
        self.tournament_type = tournament_type
        marc = challenger.Challenger("Xenouvite", "Images/marc.png")
        marion = challenger.Challenger("Kiwi", "Images/marion.jpg")
        chouaps = challenger.Challenger("Chouaps", "Images/chouaps.png")
        cendrier = challenger.Challenger("Cendrier", "Images/cendrier.png")
        laure = challenger.Challenger("Grinty", "Images/laure.png")
        liza = challenger.Challenger("Liza", "Images/liza.jpg")
        valentin = challenger.Challenger("valentin", "Images/valentin.jpg")
        matthieu = challenger.Challenger("matthieu", "Images/matthieu.jpg")
        heloise = challenger.Challenger("heloise", "Images/heloise.jpg")
        tim = challenger.Challenger("Ancestral", "Images/tim.jpg")
        lea = challenger.Challenger("MegaBombasse", "Images/lea.png")

        self.challengers_pool = [marc, marion, chouaps, cendrier, liza, laure, valentin, matthieu, heloise, tim, lea]
        self.pool_round = pool_rounds
        self.ka = Group([], "Demi-Finale")
        self.ki = Group([], "Demi-Finale")
        self.igitsa = Group([], "Finale")
        self.calif = []
        self.tournament_tree = tree.Tree(initial_value=self.igitsa, depth=5)
        self.tournament_tree.get_root().add_child(self.ki)
        self.tournament_tree.get_root().add_child(self.ka)
        self.rattrapages = Group([], "Rattrapages")
        if tournament_type == "elimination directe":
            self.alpha = Group([marion, liza], "alpha")
            self.beta = Group([matthieu, laure], "beta")
            self.delta = Group([heloise, cendrier], "delta")
            self.gamma = Group([chouaps, tim], "gamma")
            self.epsilon = Group([valentin, marc], "epsilon")
            self.alif = Group([], "alif")
            self.ba = Group([], "ba")
            self.ta = Group([lea], "ta")
            self.groups = [self.alpha, self.beta, self.delta, self.gamma, self.epsilon, self.rattrapages, self.alif,
                           self.ba, self.ta, self.ka, self.ki, self.igitsa]
            self.tournament_tree.search_node(self.ki)[0].add_child(self.rattrapages)
            self.tournament_tree.search_node(self.ka)[0].add_child(self.alif)
            self.tournament_tree.search_node(self.ka)[0].add_child(self.ta)
            self.tournament_tree.search_node(self.ki)[0].add_child(self.ba)

            self.tournament_tree.search_node(self.alif)[0].add_child(self.alpha)
            self.tournament_tree.search_node(self.alif)[0].add_child(self.gamma)
            self.tournament_tree.search_node(self.ta)[0].add_child(self.beta)
            self.tournament_tree.search_node(self.ba)[0].add_child(self.epsilon)
            self.tournament_tree.search_node(self.ba)[0].add_child(self.delta)

        else:
            self.beta = Group([matthieu, laure], "Pool renard")
            self.ta = Group([marc, liza, cendrier], "Pool et pill")
            self.gamma = Group([chouaps, tim], "Pool d'eau")
            self.alpha = Group([marion, liza, lea], "Pool coq")
            self.epsilon = Group([valentin, marc], "Pool ayer")
            self.delta = Group([heloise, cendrier], "Pool ai piou, piou, piou")
            self.alif = Group([lea, laure, valentin, chouaps], "Pool ie")
            self.ba = Group([tim, marion, heloise, matthieu], "Pool, the swimming one")
            self.groups = [self.alpha, self.beta, self.delta, self.gamma, self.epsilon, self.alif,
                           self.ba, self.ta, self.ka, self.ki, self.igitsa]

    def handle_qualifications(self, max_authorized=4):
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
                if (people_who_want_it / places_to_fill) % 2 == 0 and places_to_fill <= 4:
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
                        for i in range(pre_qualification_nbr / 2):
                            calif_groups.append(Group([], "Qualification, deuxième fournée"))
                            if i % 2 == 0:
                                self.tournament_tree.search_node(self.ki)[0].add_child(calif_groups[i])
                            else:
                                self.tournament_tree.search_node(self.ka)[0].add_child(calif_groups[i])
                            self.calif.append(calif_groups[i])
                        for i in range(pre_qualification_nbr):
                            sub_calif_groups.append(Group([], "Qualification, " + str(people_who_want_it) +
                                                          " challengers se disputent " + str(places_to_fill)+" places"))
                            sub_calif_groups[i].add_challenger(self.challengers_pool[max_authorized -
                                                                                     places_to_fill + i * 2])
                            sub_calif_groups[i].add_challenger(self.challengers_pool[max_authorized -
                                                                                     places_to_fill + i * 2 + 1])

                            self.tournament_tree.search_node(calif_groups[i % len(calif_groups)])[0].add_child(
                                sub_calif_groups[i])
                            self.calif.insert(0, sub_calif_groups[i])
                elif people_who_want_it % 3 == 0 and places_to_fill % 2 == 0:
                    pre_qualification_nbr = people_who_want_it / 3
                    calif_groups = []
                    for i in range(pre_qualification_nbr):
                        calif_groups.append(Group([], "Qualification, " + str(people_who_want_it) +
                                                      " challengers se disputent " + str(places_to_fill)+" places"))
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
                    return
                else:
                    print "I'm not built for this case, handle it yourself!"
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
        for i in range(self.pool_round):
            self.ka.add_challenger(self.groups[i].challengers[0])
            self.ki.add_challenger(self.groups[i].challengers[1])
        self.tournament_type = "elimination directe"

    def get_next_group(self):
        if self.doneRound < len(self.groups) - 1:
            if self.doneRound >= 0:
                if self.tournament_type == "elimination directe":
                    node = self.tournament_tree.search_node(self.groups[self.doneRound])[0]
                    if node.get_parent() is not None:
                        node.get_parent().get_value().add_challenger(node.get_value().get_winner())
                        self.rattrapages.add_challenger(node.get_value().get_loser())
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
                    self.groups[self.doneRound].remove_challenger(self.groups[self.doneRound].get_loser())
                    if self.doneRound == self.pool_round-1:
                        self.distribute_challengers()
            self.doneRound += 1
            return self.groups[self.doneRound]
        else:
            return None

    def get_rounds(self):
        return self.doneRound

    def extract_from_xml(self, file_path):
        pass

    def sort_challengers_by_score(self):
        done = False

        while not done:
            done = True
            for i in range(len(self.challengers_pool) - 1):
                if self.challengers_pool[i].points < self.challengers_pool[i + 1].points:
                    done = False
                    tmp = self.challengers_pool[i]
                    self.challengers_pool[i] = self.challengers_pool[i + 1]
                    self.challengers_pool[i + 1] = tmp
