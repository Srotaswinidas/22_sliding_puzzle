import time
from puzzle import Puzzle

SIZES = (3, 4, 5)


class SlidingPuzzle:
    def __init__(self, size=4):
        self.size = size
        self.puzzle = Puzzle(size)
        self.moves = 0
        self.started = time.monotonic()
        self.finished_at = None

    def elapsed(self):
        end = self.finished_at if self.finished_at is not None else time.monotonic()
        return int(end - self.started)

    def new_board(self, size=None):
        """Recreate only the board; moves and timer carry on."""
        if size is not None:
            self.size = size
        self.puzzle = Puzzle(self.size)

    def display(self):
        print()
        for row in self.puzzle.board:
            print(" ".join(f"{x or ' ':>2}" for x in row))
        print("Moves:", self.moves, " Time:", self.elapsed(), "s")

    def handle(self, key):
        """Process one command. Returns False when the game should stop."""
        if key == "q":
            return False
        if key == "n":
            self.new_board()
            print("New board (moves and timer keep counting).")
        elif key in ("w", "a", "s", "d"):
            if self.puzzle.move(key):
                self.moves += 1
                print("Tile slid.")
            else:
                print("That move is not possible.")
        else:
            print("Use W/A/S/D, N for a new board, Q to quit.")
        return True

    def choose_size(self):
        while True:
            raw = input(f"Board size {SIZES} [4]: ").strip() or "4"
            if raw.isdigit() and int(raw) in SIZES:
                self.new_board(int(raw))
                self.started = time.monotonic()
                return
            print("Pick 3, 4 or 5.")

    def run(self):
        print("Sliding Puzzle — W/A/S/D slides a tile into the blank. N new board, Q quits.")
        try:
            self.choose_size()
            while True:
                self.display()
                if self.puzzle.solved():
                    self.finished_at = time.monotonic()
                    print(f"Solved in {self.moves} moves, {self.elapsed()}s!")
                    return
                if not self.handle(input("> ").strip().lower()):
                    return
        except (EOFError, KeyboardInterrupt):
            print("\nBye.")
