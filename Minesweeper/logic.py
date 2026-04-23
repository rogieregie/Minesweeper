import random
import copy

class Minesweeper:
    def __init__(self, rows, cols, mines):
        self.rows = rows
        self.cols = cols
        self.mines = mines

        self.board = [["0" for _ in range(cols)] for _ in range(rows)]
        self.visible = [["#" for _ in range(cols)] for _ in range(rows)]

        self.undo_stack = []
        self.redo_stack = []

        self.place_mines()
        self.calculate_numbers()

    def place_mines(self):
        count = 0
        while count < self.mines:
            r = random.randint(0, self.rows - 1)
            c = random.randint(0, self.cols - 1)
            if self.board[r][c] != "M":
                self.board[r][c] = "M"
                count += 1

    def calculate_numbers(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] == "M":
                    continue
                self.board[r][c] = str(self.count_adjacent_mines(r, c))

    def count_adjacent_mines(self, r, c):
        count = 0
        for i in range(r - 1, r + 2):
            for j in range(c - 1, c + 2):
                if 0 <= i < self.rows and 0 <= j < self.cols:
                    if self.board[i][j] == "M":
                        count += 1
        return count

    def print_board(self):
        print("\nCurrent Board:")
        print("   " + " ".join(str(c) for c in range(self.cols)))

        for r in range(self.rows):
            print(f"{r}  " + " ".join(str(cell) for cell in self.visible[r]))

    def save_state(self):
        self.undo_stack.append(copy.deepcopy(self.visible))
        self.redo_stack.clear()

    def undo(self):
        if self.undo_stack:
            self.redo_stack.append(copy.deepcopy(self.visible))
            self.visible = self.undo_stack.pop()
        else:
            print("Nothing to undo.")

    def redo(self):
        if self.redo_stack:
            self.undo_stack.append(copy.deepcopy(self.visible))
            self.visible = self.redo_stack.pop()
        else:
            print("Nothing to redo.")

    def reveal(self, r, c):
        if self.visible[r][c] != "#":
            return

        if self.board[r][c] == "M":
            self.visible[r][c] = "M"
            return "lose"

        self.flood_fill(r, c)
        return "continue"

    def flood_fill(self, r, c):
        if not (0 <= r < self.rows and 0 <= c < self.cols):
            return
        if self.visible[r][c] != "#":
            return

        self.visible[r][c] = self.board[r][c]

        if self.board[r][c] == "0":
            for i in range(r - 1, r + 2):
                for j in range(c - 1, c + 2):
                    if i != r or j != c:
                        self.flood_fill(i, j)

    def check_win(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] != "M" and self.visible[r][c] == "#":
                    return False
        return True