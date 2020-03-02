import random
from collections import namedtuple

from constants import BOARD_WIDTH, BORDER_WIDTH, BOARD_HEIGHT, MOVE_CHOICES, WIN_DISTANCE, MAX_HITS
from tree_search.monte_carlo import Node
from utils.engine import get_distance

_GS = namedtuple("GameState", "position destination terminal hits")


def get_valid_choices(board):
    choices = list()
    for choice in MOVE_CHOICES:
        # # can not go back to parent
        # can_not_walk_back = board.parent_position[0] == choice[0] and board.parent_position[1] == choice[1]
        # if can_not_walk_back:
        #     continue

        # can not move left
        can_not_walk_left = board.position[0] <= BORDER_WIDTH and choice[0] < 0
        if can_not_walk_left:
            continue

        # can not move right
        can_not_walk_right = board.position[0] >= BOARD_WIDTH - BORDER_WIDTH and choice[0] > 0
        if can_not_walk_right:
            continue

        # can not move down
        can_not_walk_down = board.position[1] <= BORDER_WIDTH and choice[1] < 0
        if can_not_walk_down:
            continue

        # can not move up
        can_not_walk_up = board.position[1] >= BOARD_HEIGHT - BORDER_WIDTH and choice[1] > 0
        if can_not_walk_up:
            continue

        # append choice
        choices.append(choice)

    return choices


def get_children(board):
    res = set()
    for pos in get_valid_choices(board):
        pos = (board.position[0] + pos[0], board.position[1] + pos[1])
        res.add(board.make_move(pos, board.destination))
    return res


class GameBoard(_GS, Node):
    def make_move(board, position, destination):
        distance = get_distance(position, destination)
        terminal = distance <= WIN_DISTANCE or board.hits >= MAX_HITS
        # if terminal and distance <= WIN_DISTANCE:
        #     print("WON", distance, board.hits)
        # elif terminal:
        #     print("LOST", distance, board.hits)
        return GameBoard(position, destination, terminal, board.hits + 1)

    def find_children(board):
        # If the game is finished then no moves can be made
        if board.terminal:
            return set()
        # Otherwise, you can make a move in each of the empty spots
        return get_children(board)

    def find_random_child(board):
        # If the game is finished then no moves can be made
        if board.terminal:
            return None
        # choose a random motion vector to move
        choices = get_valid_choices(board)
        r = random.randint(0, len(choices) - 1)
        choice = choices[r]
        next_position = (board.position[0] + choice[0], board.position[1] + choice[1])
        return board.make_move(next_position, board.destination)

    def reward(board):
        if not board.terminal:
            raise RuntimeError(f"reward called on nonterminal board {board}")
        if get_distance(board.position, board.destination):
            return 0
        return 1

    def is_terminal(board):
        return board.terminal
