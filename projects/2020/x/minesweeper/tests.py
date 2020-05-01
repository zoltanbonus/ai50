import unittest
from minesweeper import Sentence, MinesweeperAI

class TestMineSweeper(unittest.TestCase):
    def test_known_mines_all_mines(self):
        expected = {(0,1), (1,0), (1,1)}
        sentence = Sentence({(0,1), (1,0), (1,1)}, 3)
        self.assertEqual(sentence.known_mines(), expected)

    def test_known_mines_no_mines(self):
        expected = set()
        sentence = Sentence({(0,1), (1,0), (1,1)}, 2)
        self.assertEqual(sentence.known_mines(), expected)

    def test_known_safes_all_safe(self):
        expected = {(0,1), (1,0), (1,1)}
        sentence = Sentence({(0,1), (1,0), (1,1)}, 0)
        self.assertEqual(sentence.known_safes(), expected)

    def test_known_safes_no_safe(self):
        expected = set()
        sentence = Sentence({(0,1), (1,0), (1,1)}, 1)
        self.assertEqual(sentence.known_safes(), expected)

    def test_mark_mine(self):
        sentence = Sentence({(0,1), (1,0), (1,1)}, 2)
        sentence.mark_mine((0,1))

        self.assertEqual(sentence.cells, {(1,0), (1,1)})
        self.assertEqual(sentence.count, 1)

    def test_mark_safe(self):
        sentence = Sentence({(0,1), (1,0), (1,1)}, 2)
        sentence.mark_safe((0,1))

        self.assertEqual(sentence.cells, {(1,0), (1,1)})
        self.assertEqual(sentence.count, 2)

    def test_add_knowledge_moves_made(self):
        ai = MinesweeperAI()
        ai.add_knowledge((0,0), 1)

        self.assertEqual(ai.moves_made, {(0,0)})
    
    def test_add_knowledge_mark_safe(self):
        ai = MinesweeperAI()
        ai.add_knowledge((0,0), 1)

        self.assertTrue((0,0) in ai.safes)

    def test_add_knowledge_add_sentence(self):
        ai = MinesweeperAI()
        ai.add_knowledge((0,0), 1)

        self.assertEqual(len(ai.knowledge), 1)

    def test_add_knowledge_add_sentence_upper_left_corner(self):
        ai = MinesweeperAI()
        self.assertEqual(ai.get_neighbor_cells(0,0), {(0,1), (1,0), (1,1)})

    def test_add_knowledge_add_sentence_upper_right_corner(self):
        ai = MinesweeperAI()
        self.assertEqual(ai.get_neighbor_cells(0, 7), {(0,6), (1,6), (1,7)})

    def test_add_knowledge_add_sentence_lower_left_corner(self):
        ai = MinesweeperAI()
        self.assertEqual(ai.get_neighbor_cells(7,0), {(7,1), (6,0), (6,1)})

    def test_add_knowledge_add_sentence_lower_right_corner(self):
        ai = MinesweeperAI()
        self.assertEqual(ai.get_neighbor_cells(7,7), {(7,6), (6,7), (6,6)})

if __name__ == '__main__':
    unittest.main()