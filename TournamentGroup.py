class Group:
    isOrdered: bool
    title: str

    def __init__(self, members: [], title: str = "unnamed"):
        self.challengers = members
        self.subgroups = {}
        self.scores = {}
        self.title = title
        self.isOrdered = True
        for i in self.challengers:
            self.scores[i] = 0

    @property
    def challenger_number(self):
        return len(self.challengers)

    @property
    def winner(self):
        if self.isOrdered:
            return self.challengers[0]
        else:
            index = self.challengers[0]
            for i in self.challengers:
                if self.scores[i] > self.scores[index]:
                    index = i
            return index

    @property
    def loser(self):
        if self.isOrdered:
            return self.challengers[len(self.challengers)-1]
        else:
            index = self.challengers[0]
            for i in self.challengers:
                if self.scores[i] < self.scores[index]:
                    index = i
            return index

    def get_title(self) -> str:
        return self.title

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

    def sort_challengers_by_points(self):
        """
            Sorts the challengers by point in decreasing order
        :return: returns the newly sorted array
        """
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

    def add_challenger(self, new_challenger, initial_score: int = 0) -> None:
        """
            Appends a new challenger to the challengers list
        :param new_challenger: The challenger to add
        :param initial_score: The initial score of this new challenger (default value is 0)
        """
        self.challengers.append(new_challenger)
        self.scores[new_challenger] = initial_score
        self.isOrdered = initial_score == 0 and self.isOrdered

    def remove_challenger(self, old_challenger):
        """
            Removes the challenger given in parameter from the challengers array if present
        :param old_challenger: The challenger to remove
        """
        self.challengers.remove(old_challenger)

    def add_subgroup(self, new_subgroup):
        """
            Adds a subgroup to the subgroups of this group
        :param new_subgroup: The new subgroup to add
        :type new_subgroup: Group
        """
        self.subgroups[new_subgroup.get_title()] = new_subgroup

    def get_subgroups(self):
        """
            Gets the subgroups of that group if there are some, None otherwise
        :return:
        """
        if len(self.subgroups) > 0:
            return self.subgroups
        else:
            return None
