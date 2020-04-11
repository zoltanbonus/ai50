import unittest
import csv
from degrees import load_data, shortest_path, person_id_for_name
from util import Node, StackFrontier, QueueFrontier


class TestShortestPath(unittest.TestCase):
    def test_find_further_node(self):
        self.assertEqual(len(self.get_shortest_path(
            "small", "Kevin Bacon", "Cary Elwes")), 3)

    def test_find_same_actor(self):
        self.assertEqual(len(self.get_shortest_path(
            "small", "Kevin Bacon", "Kevin Bacon")), 1)

    def test_find_neighbor_node(self):
        self.assertEqual(len(self.get_shortest_path(
            "small", "Kevin Bacon", "Tom Cruise")), 1)

    def test_no_path(self):
        self.assertEqual(self.get_shortest_path(
            "small", "Kevin Bacon", "Emma Watson"), None)

    def test_large_data(self):
        self.assertEqual(len(self.get_shortest_path(
            "large", "Emma Watson", "Jennifer Lawrence")), 3)

    def get_shortest_path(self, directory, sourceName, targetName):
        load_data(directory)
        source = person_id_for_name(sourceName)
        target = person_id_for_name(targetName)
        return shortest_path(source, target)


if __name__ == '__main__':
    unittest.main()
