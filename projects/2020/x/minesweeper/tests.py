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

    def test_mark_mine_single_element(self):
        sentence = Sentence({(0,2)}, 1)
        sentence.mark_mine((0,2))

        self.assertEqual(sentence.cells, set())
        self.assertEqual(sentence.count, 0)

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

    def test_add_knowledge_get_neighbors_lower_right_corner(self):
        ai = MinesweeperAI()
        self.assertEqual(ai.get_neighbor_cells(7,7), {(7,6), (6,7), (6,6)})

    def test_add_knowledge_get_neighbors_middle(self):
        ai = MinesweeperAI()
        self.assertEqual(ai.get_neighbor_cells(1,1), {(0,0), (0,1), (0,2), (1,0), (1,2), (2,0), (2,1), (2,2)})

    def test_add_knowledge_inferred_sentence(self):
        ai = MinesweeperAI()
        existingSentence = Sentence({(0,1),(1,1),(1,2)}, 1)
        ai.knowledge.append(existingSentence)

        existingSentence2 = Sentence({(0,1), (1,1), (1,2),(0,2), (2,2) }, 2)
        ai.knowledge.append(existingSentence2)

        ai.infer_sentences()
        self.assertEqual(len(ai.knowledge), 3)

    def test_add_knowledge_inferred_sentence2(self):
        ai = MinesweeperAI()
        existingSentence = Sentence({(0, 4), (1, 4)}, 1)
        ai.knowledge.append(existingSentence)

        ai.infer_sentences()
        self.assertEqual(len(ai.knowledge), 1)

    def test_make_safe_move_happy_path(self):
        ai = MinesweeperAI()
        ai.moves_made.add((0,0))
        ai.safes.add((0,0))
        ai.safes.add((2,2))

        self.assertEqual(ai.make_safe_move(), (2,2))

    def test_make_safe_move_no_safes(self):
        ai = MinesweeperAI()
        ai.moves_made.add((0,0))

        self.assertEqual(ai.make_safe_move(), None)

    def test_make_safe_move_no_unexplored_safes(self):
        ai = MinesweeperAI()
        ai.moves_made.add((0,0))
        ai.moves_made.add((2,2))
        ai.safes.add((0,0))
        ai.safes.add((2,2))

        self.assertEqual(ai.make_safe_move(), None)

    def test_make_random_move(self):
        ai = MinesweeperAI()
        ai.moves_made.add((0,0))
        ai.mines.add((0,1))

        self.assertEqual(ai.make_random_move(), (0,2))


if __name__ == '__main__':
    unittest.main()