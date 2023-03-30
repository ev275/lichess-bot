"""
Some example strategies for people who want to create a custom, homemade bot.
"""

from __future__ import annotations
import chess
from chess.engine import PlayResult
import random
from engine_wrapper import MinimalEngine
from typing import Any

from evaluation.mixins import PieceSquareMixin, PieceValueMixin
from search.alphabeta import AlphaBetaMixin
from output_tables import TOP_SYMMETRIC_TABLE, TOP_NON_SYMMETRIC_TABLE, TOP_ANTICHESS_SYMMETRIC_TABLE
from definitions import INFINITE


class ExampleEngine(MinimalEngine):
    pass

class GoodEngine(AlphaBetaMixin, PieceValueMixin, PieceSquareMixin):
    pass

class MyEngine(MinimalEngine):
    def search(self, board: chess.Board, *args: Any) -> PlayResult:
        score, pv = GoodEngine(board, TOP_SYMMETRIC_TABLE).search(-INFINITE, +INFINITE, 6)

        # safety net for when no good move is found
        if not pv: 
            pv = [move for move in board.legal_moves]

        # find best move
        best_move = pv[0] # could set to random.choice(pv) instead for variablility
        return PlayResult(best_move, None)


# Strategy names and ideas from tom7's excellent eloWorld video

class RandomMove(ExampleEngine):
    def search(self, board: chess.Board, *args: Any) -> PlayResult:
        return PlayResult(random.choice(list(board.legal_moves)), None)


class Alphabetical(ExampleEngine):
    def search(self, board: chess.Board, *args: Any) -> PlayResult:
        moves = list(board.legal_moves)
        moves.sort(key=board.san)
        return PlayResult(moves[0], None)


class FirstMove(ExampleEngine):
    """Gets the first move when sorted by uci representation"""
    def search(self, board: chess.Board, *args: Any) -> PlayResult:
        moves = list(board.legal_moves)
        moves.sort(key=str)
        return PlayResult(moves[0], None)
