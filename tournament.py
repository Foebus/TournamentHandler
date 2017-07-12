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
            self.alpha = Group([marion, liza, lea], "Pool, tour 1")
            self.beta = Group([matthieu, laure], "Pool, tour 1")
            self.delta = Group([heloise, cendrier], "Pool, tour 1")
            self.gamma = Group([chouaps, tim], "Pool, tour 1")
            self.epsilon = Group([valentin, marc], "Pool, tour 1")
            self.alif = Group([lea, laure, valentin, chouaps], "Pool, tour 2")
            self.ba = Group([tim, marion, heloise, matthieu], "Pool, tour 2")
            self.ta = Group([marc, liza, cendrier], "Pool, tour 2")
            self.groups = [self.alpha, self.beta, self.delta, self.gamma, self.epsilon, self.alif,
                           self.ba, self.ta, self.ka, self.ki, self.igitsa]

    def handle_qualifications(self, max_authorized=4):
        if not self.calif:
            self.sort_challengers_by_score()

            if self.challengers_pool[max_authorized - 1].points == self.challengers_pool[max_authorized].points:
                places_to_fill = 1
                while self.challengers_pool[max_authorized - 1].points == \
                        self.challengers_pool[max_authorized - places_to_fill + 1].points:
                    places_to_fill += 1
                people_who_want_it = places_to_fill
                while self.challengers_pool[max_authorized - places_to_fill].points == \
                        self.challengers_pool[max_authorized - places_to_fill + people_who_want_it].points:
                    people_who_want_it += 1
                calif_group = Group([self.challengers_pool[max_authorized - 1], self.challengers_pool[max_authorized]],
                                    "Qualifications")
                for i in range(max_authorized - places_to_fill):
                    if i % 2 == 0:
                        self.ka.add_challenger(self.challengers_pool[i])
                    else:
                        self.ki.add_challenger(self.challengers_pool[i])
                if (people_who_want_it / places_to_fill) % 2 == 0:
                    pre_qualification_nbr = (people_who_want_it / places_to_fill) / 2
                    sub_calif_groups = []
                    for i in range(0, pre_qualification_nbr, 2):
                        sub_calif_groups[i] = Group([], "Qualification")
                        sub_calif_groups[i].add_challenger(self.challengers_pool[max_authorized - places_to_fill + i])
                        sub_calif_groups[i].add_challenger(self.challengers_pool[max_authorized -
                                                                                 places_to_fill + i + 1])
                        if i % 2 == 0:
                            self.tournament_tree.search_node(self.ki)[0].add_child(sub_calif_groups[i])
                        else:
                            self.tournament_tree.search_node(self.ka)[0].add_child(sub_calif_groups[i])
                else:
                    print "I'm not built for this case, handle it yourself!"
                # self.tournament_tree.search_node(self.ki)[0].add_child(calif_group)
                # i = 1
                # while self.challengers_pool[max_authorized - 1].points == self.challengers_pool[
                #             max_authorized + i].points:
                #     sub_calif_group = Group([self.challengers_pool[max_authorized + i + 1],
                #                              self.challengers_pool[max_authorized + i]], "Pre-Qualifications")
                #     self.calif.append(sub_calif_group)
                #     self.calif.append(calif_group)
                #     self.tournament_tree.search_node(calif_group)[0].add_child(sub_calif_group)
                #     i += 2

                self.calif.append(calif_group)
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
                    self.challengers_pool[0].add_points(4 - self.groups[self.doneRound].challengerNumber)
                    for k in range(self.groups[self.doneRound].challengerNumber):
                        self.challengers_pool[self.challengers_pool.index(self.groups[self.doneRound].challengers[k])] \
                            .add_points(self.groups[self.doneRound].challengerNumber - k)
                    if self.doneRound == self.pool_round:
                        self.handle_qualifications()
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
