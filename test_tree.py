from unittest import TestCase

from TournamentGroup import Group
from challenger import Challenger
from tree import Tree


class TestTree(TestCase):
    m1 = Challenger("Kakouak", "lol")
    m2 = Challenger("Kakouik", "lol")
    m3 = Challenger("Kikouak", "lol")
    m4 = Challenger("Kikouik", "lol")
    g1 = Group([], "Test adding subgroup")
    g2 = Group([m3, m4], "Test adding subgroup 1")
    g3 = Group([m1, m2], "Test adding subgroup 2")

    def test_get_root(self):
        depth = 2
        tournament_tree = Tree(self.g1, depth)
        self.assertEqual(tournament_tree.get_root().get_value(), self.g1)

    def test_get_depth(self):
        depth = 2
        tournament_tree = Tree(self.g1, depth)
        self.assertEqual(tournament_tree.get_depth(), depth)

    def test_search_node(self):
        depth = 2
        tournament_tree = Tree(self.g1, depth)
        tournament_tree.get_root().add_child(self.g2)
        tournament_tree.get_root().add_child(self.g3)
        self.assertEqual(tournament_tree.search_node(self.g2).get_value(), self.g2)
        self.assertEqual(tournament_tree.search_node(self.g3).get_value(), self.g3)
        self.assertEqual(tournament_tree.search_node(self.g1).get_value(), self.g1)
