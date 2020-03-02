import pickle
import random
import sys

import pygame
from pygame.constants import QUIT, KEYDOWN, K_ESCAPE

from constants import DEFAULT_POS, GOAL_POS, ROLLOUTS, EVOLUTIONS
from game_board import GameBoard
from simulation import sim
from tree_search.monte_carlo import MCTS
from utils.engine import get_distance

SEEDS = [
    "FOO",
    "BAR",
    "BLAH",
    "STELA",
    "DOMENIK",
]
FINAL_SEED = "FINAL"


def main():
    pygame.init()
    # init pygame sim
    sim.render()

    evos = []

    print(sim.body_character.position)
    print(sim.body_character.position)

    def run(tree):

        board = GameBoard(
            position=DEFAULT_POS,
            destination=GOAL_POS,
            terminal=False,
            hits=0,
            # parent_position=(None, None),
        )
        step = 0
        while True:
            step += 1
            # print("step", step, "distance", get_distance(board.position, board.destination))
            # break the loop from pygame
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit(0)
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    sys.exit(0)

            for _ in range(ROLLOUTS):
                tree.do_rollout(board)
            board = tree.do_choose(board)

            sim.body_character.position = board.position
            sim.render()

            if board.terminal:
                print("WIN STEP", step, "WIN POS", GOAL_POS, "DISTANCE",
                      get_distance(board.position, board.destination), "Position", board.position)
                return step

    # init MCTS
    tree = MCTS()
    try:
        for r in range(EVOLUTIONS):
            random.seed(SEEDS[r])
            print(50 * "-")
            # tree.exploration_weight = random.randint(5, 10) / 10
            sim.body_character.position = DEFAULT_POS
            _run = run(tree)
            evos.append(_run)
            print("[EVOLUTION]", r, "Weight", tree.exploration_weight, "Steps", _run)

            # print(50 * "=")
            # random.seed(FINAL_SEED)
            # print("STARTING FINAL RUN (no exploration)")
            # tree.exploration_weight = 0
            # evos.append(run(tree))
            # print(50 * "=")
    except Exception as e:
        print("EXCEPTION", e)
    finally:
        # save_tree(tree)
        pass

    total = len(evos)
    for idx, evo in enumerate(evos):
        total += evo
        print("Evolution {} with {} hits".format(idx, evo))


def save_tree(tree):
    with open('./Q.pickle', 'w') as f:
        print("save Q.pickle")
        print(pickle.dumps(tree.Q))
        f.write(pickle.dumps(tree.Q))

    with open('./N.pickle', 'w') as f:
        print("save N.pickle")
        print(pickle.dumps(tree.N))
        f.write(pickle.dumps(tree.N))


if __name__ == '__main__':
    try:
        main()
    except:
        print()
