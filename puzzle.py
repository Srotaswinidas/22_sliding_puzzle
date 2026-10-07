import random

BLANK_DELTA = {"w": (1, 0), "s": (-1, 0), "a": (0, 1), "d": (0, -1)}
OPPOSITE = {"w": "s", "s": "w", "a": "d", "d": "a"}


class Puzzle:
    def __init__(self, size=4):
        if size < 2:
            raise ValueError("size must be at least 2")
        self.size = size
        self.goal = list(range(1, size * size)) + [0]
        self.board = self.make_board()

    def make_board(self):
        """Start from the solved board and apply random legal moves, so the
        result is always reachable (solvable)."""
        self.board = [self.goal[r * self.size:(r + 1) * self.size] for r in range(self.size)]
        while True:
            last = None
            for _ in range(self.size * self.size * 30 + random.randint(0, 11)):
                options = [d for d in BLANK_DELTA if d != OPPOSITE.get(last) and self._can_move(d)]
                last = random.choice(options)
                self.move(last)
            if not self.solved():  # never start already solved
                return self.board

    def blank_pos(self):
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] == 0:
                    return r, c

    def _can_move(self, direction):
        r, c = self.blank_pos()
        dr, dc = BLANK_DELTA[direction]
        return 0 <= r + dr < self.size and 0 <= c + dc < self.size

    def move(self, direction):
        """Slide a tile into the blank. Returns True only if a tile moved."""
        if direction not in BLANK_DELTA or not self._can_move(direction):
            return False
        r, c = self.blank_pos()
        dr, dc = BLANK_DELTA[direction]
        nr, nc = r + dr, c + dc
        self.board[r][c], self.board[nr][nc] = self.board[nr][nc], self.board[r][c]
        return True

    def solved(self):
        return sum(self.board, []) == self.goal
