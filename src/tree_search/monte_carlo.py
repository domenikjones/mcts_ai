"""
A minimal implementation of Monte Carlo tree search (MCTS) in Python 3
Luke Harold Miles, July 2019, Public Domain Dedication
See also https://en.wikipedia.org/wiki/Monte_Carlo_tree_search
https://gist.github.com/qpwo/c538c6f73727e254fdc7fab81024f6e1
"""
import math
from abc import ABC, abstractmethod
from collections import defaultdict, namedtuple

from constants import EXPLORATION_RATE


class MCTS:
    """Monte Carlo tree searcher. First rollout the tree then choose a move."""

    def __init__(self, exploration_weight=EXPLORATION_RATE):
        # print("MCTS.INIT")
        self.Q = defaultdict(int)  # total reward of each node
        self.N = defaultdict(int)  # total visit count for each node
        self.children = dict()  # children of each node
        self.exploration_weight = exploration_weight

    def do_choose(self, node):
        """Choose the best successor of node. (Choose a move in the game)"""
        # print("DO_CHOOSE")
        if node.is_terminal():
            raise RuntimeError(f"choose called on terminal node {node}")

        if node not in self.children:
            return node.find_random_child()

        def score(n):
            _n = clean_node(n)
            if self.N[_n] == 0:
                return float("-inf")  # avoid unseen moves
            return self.Q[_n] / self.N[_n]  # average reward

        return max(self.children[node], key=score)

    def do_rollout(self, node):
        """"Make the tree one layer better. (Train for one iteration.)"""
        # print("DO_ROLLOUT")
        path = self._select(node)
        leaf = path[-1]
        self._expand(leaf)
        reward = self._simulate(leaf)
        self._backpropagate(path, reward)

    def _simulate(self, node):
        """Returns the reward for a random simulation (to completion) of `node`"""
        # print("SIMULATE", self.exploration_weight)
        while True:
            if node.is_terminal():
                return node.reward()
            node = node.find_random_child()

    def _select(self, node):
        """Find an unexplored descendent of `node`"""
        # print("SELECT")
        path = []
        while True:
            path.append(node)
            if node not in self.children or not self.children[node]:
                # node is either unexplored or terminal
                return path
            unexplored = self.children[node] - self.children.keys()
            if unexplored:
                n = unexplored.pop()
                path.append(n)
                return path
            node = self._uct_select(node)  # descend a layer deeper

    def _expand(self, node):
        """Update the `children` dict with the children of `node`"""
        # print("EXPAND")
        if node in self.children:
            return  # already expanded
        self.children[node] = node.find_children()

    def _backpropagate(self, path, reward):
        """Send the reward back up to the ancestors of the leaf"""
        # print("BACKPROPAGATE")
        for node in reversed(path):
            _n = clean_node(node)
            self.N[_n] += 1
            self.Q[_n] += reward
            reward = 1

    def _uct_select(self, node):
        """Select a child of node, balancing exploration & exploitation"""
        # print("UCT_SELECT")
        # All children of node should already be expanded:
        assert all(n in self.children for n in self.children[node])

        log_N_vertex = math.log(self.N[clean_node(node)])

        def uct(n):
            _n = clean_node(n)
            """Upper confidence bound for trees"""
            return self.Q[_n] / self.N[_n] + self.exploration_weight * math.sqrt(
                log_N_vertex / self.N[_n]
            )

        return max(self.children[node], key=uct)


_NODE = namedtuple("NODE", 'position destination parent')


def clean_node(node):
    return node
    # return _NODE(position=node.position, destination=node.destination)


class Node(ABC):
    """
    A representation of a single board state.
    MCTS works by constructing a tree of these Nodes.
    Could be e.g. a chess or checkers board state.
    """

    @abstractmethod
    def find_children(self):
        """All possible successors of this board state"""
        return set()

    @abstractmethod
    def find_random_child(self):
        """Random successor of this board state (for more efficient simulation)"""
        return None

    @abstractmethod
    def is_terminal(self):
        """Returns True if the node has no children"""
        return True

    @abstractmethod
    def reward(self):
        """Assumes `self` is terminal node. 1=win, 0=loss, .5=tie, etc"""
        return 0

    @abstractmethod
    def __hash__(self):
        """Nodes must be hashable"""
        return 123456789

    @abstractmethod
    def __eq__(node1, node2):
        """Nodes must be comparable"""
        return True
