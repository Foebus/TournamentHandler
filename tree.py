class Tree:
    def __init__(self, initial_value=None, depth=1):
        self.root = Node(None, initial_value)
        self.depth = depth

    def get_root(self):
        return self.root

    def get_depth(self):
        return self.depth

    def search_node(self, value):
        act_depth = 0
        act_branch = []
        for k in range(self.depth):
            act_branch.append(0)
        done = False
        tmp = self.root
        result = []
        while not done:
            if tmp.get_value() == value:
                result.append(tmp)
            if act_depth < self.depth and act_branch[act_depth] < tmp.get_children_nbr():
                tmp = tmp.get_child(act_branch[act_depth])
                act_depth += 1
            else:
                act_branch[act_depth] = 0
                act_depth -= 1
                tmp = tmp.get_parent()
                if tmp is None:
                    done = True
                else:
                    while act_branch[act_depth] >= tmp.get_children_nbr():
                        act_branch[act_depth] = 0
                        tmp = tmp.get_parent()
                        act_depth -= 1
                act_branch[act_depth] += 1
        return result


class Node:
    def __init__(self, parent, initial_value=None):
        self.value = initial_value
        self.children = []
        self.parent = parent

    def add_child(self, child_value):
        self.children.append(Node(self, child_value))

    def get_children(self):
        return self.children

    def get_children_nbr(self):
        return len(self.children)

    def get_child(self, child_id):
        return self.children[child_id]

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value

    def get_parent(self):
        return self.parent
