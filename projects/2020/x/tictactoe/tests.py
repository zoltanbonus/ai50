import unittest
from tictactoe import player, X, EMPTY, O, initial_state, actions, result, winner, terminal, utility, minimax


class TestShortestPath(unittest.TestCase):
    def test_player_initial_state(self):
        self.assertEqual(player(initial_state()), X)

    def test_player_Os_move(self):
        board = [[X, EMPTY, EMPTY],
                 [EMPTY, EMPTY, EMPTY],
                 [EMPTY, EMPTY, EMPTY]]
        self.assertEqual(player(board), O)

    def test_player_Xs_move(self):
        board = [[X, EMPTY, EMPTY],
                 [EMPTY, O, EMPTY],
                 [EMPTY, EMPTY, EMPTY]]
        self.assertEqual(player(board), X)

    def test_actions_initial_state(self):
        expected = {(0, 0), (0, 1), (0, 2),
                    (1, 0), (1, 1), (1, 2),
                    (2, 0), (2, 1), (2, 2)}

        self.assertEqual(actions(initial_state()), expected)

    def test_actions_mid_game(self):
        board = [[X, EMPTY, EMPTY],
                 [EMPTY, O, EMPTY],
                 [X, EMPTY, EMPTY]]

        expected = {(0, 1), (0, 2),
                    (1, 0), (1, 2),
                    (2, 1), (2, 2)}

        self.assertEqual(actions(board), expected)

    def test_actions_end_game(self):
        board = [[X, X, O],
                 [O, O, EMPTY],
                 [X, O, X]]

        expected = {(1, 2)}

        self.assertEqual(actions(board), expected)

    def test_actions_terminal_board(self):
        board = [[X, X, O],
                 [O, O, O],
                 [X, O, X]]

        expected = set()

        self.assertEqual(actions(board), expected)

    def test_result_input_board_unmodified(self):
        board = initial_state()
        action = (0, 0)

        result(board, action)
        self.assertEqual(board, initial_state())

    def test_result_initial_state(self):
        board = initial_state()
        action = (0, 0)
        expected = [[X, EMPTY, EMPTY],
                    [EMPTY, EMPTY, EMPTY],
                    [EMPTY, EMPTY, EMPTY]]

        self.assertEqual(result(board, action), expected)

    def test_result_mid_game(self):
        board = [[X, EMPTY, X],
                 [O, O, EMPTY],
                 [X, EMPTY, EMPTY]]
        action = (1, 2)
        expected = [[X, EMPTY, X],
                    [O, O, O],
                    [X, EMPTY, EMPTY]]

        self.assertEqual(result(board, action), expected)

    def test_result_invalid_move(self):
        board = [[X, EMPTY, X],
                 [O, O, EMPTY],
                 [X, EMPTY, EMPTY]]
        action = (0, 0)

        self.assertRaises(Exception, result, board, action)

    def test_winner_initial_state(self):
        board = initial_state()
        self.assertEqual(winner(board), None)

    def test_winner_mid_game(self):
        board = [[X, EMPTY, X],
                 [O, O, EMPTY],
                 [X, EMPTY, EMPTY]]
        self.assertEqual(winner(board), None)

    def test_winner_tie(self):
        board = [[X, X, O],
                 [O, O, X],
                 [X, O, X]]
        self.assertEqual(winner(board), None)

    def test_winner_vertical_0(self):
        board = [[X, EMPTY, O],
                 [X, EMPTY, O],
                 [X, EMPTY, X]]
        self.assertEqual(winner(board), X)

    def test_winner_vertical_1(self):
        board = [[O, X, O],
                 [X, X, O],
                 [O, X, X]]
        self.assertEqual(winner(board), X)

    def test_winner_vertical_2(self):
        board = [[X, EMPTY, O],
                 [X, EMPTY, O],
                 [EMPTY, EMPTY, O]]
        self.assertEqual(winner(board), O)

    def test_winner_horizontal_0(self):
        board = [[X, X, X],
                 [O, EMPTY, O],
                 [EMPTY, EMPTY, O]]
        self.assertEqual(winner(board), X)

    def test_winner_horizontal_1(self):
        board = [[X, O, X],
                 [O, O, O],
                 [EMPTY, X, X]]
        self.assertEqual(winner(board), O)

    def test_winner_horizontal_2(self):
        board = [[X, O, X],
                 [O, O, EMPTY],
                 [X, X, X]]
        self.assertEqual(winner(board), X)

    def test_winner_diagonal_0(self):
        board = [[X, O, O],
                 [O, X, EMPTY],
                 [O, X, X]]
        self.assertEqual(winner(board), X)

    def test_winner_diagonal_1(self):
        board = [[O, O, X],
                 [O, X, EMPTY],
                 [X, X, O]]
        self.assertEqual(winner(board), X)

    def test_terminal_initial_state(self):
        self.assertEqual(terminal(initial_state()), False)

    def test_terminal_mid_game(self):
        board = [[X, EMPTY, X],
                 [O, O, EMPTY],
                 [X, EMPTY, EMPTY]]
        self.assertEqual(terminal(board), False)

    def test_terminal_tie(self):
        board = [[X, X, O],
                 [O, O, X],
                 [X, O, X]]
        self.assertEqual(terminal(board), True)

    def test_terminal_x_wins(self):
        board = [[X, O, O],
                 [O, X, EMPTY],
                 [O, X, X]]
        self.assertEqual(terminal(board), True)

    def test_utility_x_wins(self):
        board = [[X, O, O],
                 [O, X, EMPTY],
                 [O, X, X]]
        self.assertEqual(utility(board), 1)

    def test_utility_o_wins(self):
        board = [[O, O, O],
                 [X, X, EMPTY],
                 [O, X, X]]
        self.assertEqual(utility(board), -1)

    def test_utility_tie(self):
        board = [[X, X, O],
                 [O, O, X],
                 [X, O, X]]
        self.assertEqual(utility(board), 0)

    def test_minimax_terminal(self):
        board = [[X, X, O],
                 [O, O, X],
                 [X, O, X]]
        self.assertEqual(minimax(board), None)

    def test_minimax_x_wins(self):
        board = [[X, X, EMPTY],
                 [O, O, EMPTY],
                 [EMPTY, EMPTY, EMPTY]]
        self.assertEqual(minimax(board), (0, 2))

    def test_minimax_tie(self):
        board = [[X, X, O],
                 [O, O, X],
                 [X, O, EMPTY]]
        self.assertEqual(minimax(board), (2, 2))

    def test_minimax_prevent_o_from_winning(self):
        board = [[X, X, O],
                 [O, O, EMPTY],
                 [EMPTY, EMPTY, EMPTY]]
        self.assertEqual(minimax(board), (1, 2))


if __name__ == '__main__':
    unittest.main()
