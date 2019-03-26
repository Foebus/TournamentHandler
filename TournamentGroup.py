class Group:
    title: str

    def __init__(self, members, title="unnamed"):
        self.challengers = members
        self.challengerNumber = len(members)
        self.subgroups = {}
        self.scores = {}
        self.title = title
        self.isOrdered = True
        for i in self.challengers:
            self.scores[i] = 0

    def give_point(self, challenger_id, point_nbr=1):
        """
        Gives points to a challenger
        :param challenger_id: the challenger to give points to
        :param point_nbr: the number of points to give
        """
        if challenger_id in self.scores.keys():
            self.scores[challenger_id] += point_nbr
            self.isOrdered = False
        else:
            for i, c in enumerate(self.challengers):
                if i == challenger_id:
                    self.scores[c] += point_nbr
                    self.isOrdered = False
                    break

    def get_points(self, challenger_id):
        """
        Gets the actual points of a challenger
        :param challenger_id: The challenger we want the points from
        :return: His actual number of points
        """
        if challenger_id in self.scores.keys():
            return self.scores[challenger_id]
        else:
            for i, c in enumerate(self.challengers):
                if i == challenger_id:
                    return self.scores[c]
            return 0

    @property
    def get_winner(self):
        if self.isOrdered:
            return self.challengers[0]
        else:
            index = self.challengers[0]
            for i in self.challengers:
                if self.scores[i] > self.scores[index]:
                    index = i
            return index

    @property
    def get_loser(self):
        if self.isOrdered:
            return self.challengers[len(self.challengers)-1]
        else:
            index = self.challengers[0]
            for i in self.challengers:
                if self.scores[i] < self.scores[index]:
                    index = i
            return index

    def sort_challengers_by_points(self):
        if not self.isOrdered:
            order = []
            for k, i in self.scores.items():
                order.append((i, k))
            order.sort()

            nb = len(self.challengers)
            for i, d in enumerate(order):
                self.challengers[nb - i - 1] = d[1]
            self.isOrdered = True
        return self.challengers

    def add_challenger(self, new_challenger, initialscore=0):
        self.challengers.append(new_challenger)
        self.challengerNumber += 1
        self.scores[new_challenger] = initialscore
        self.isOrdered = initialscore == 0

    def remove_challenger(self, old_challenger):
        self.challengers.remove(old_challenger)

    def get_title(self):
        return self.title

    def add_subgroup(self, new_subgroup):
        """

        :type new_subgroup: Group
        """
        self.subgroups[new_subgroup.get_title()] = new_subgroup

    def get_subgroups(self):
        if len(self.subgroups) > 0:
            return self.subgroups
        else:
            return None
