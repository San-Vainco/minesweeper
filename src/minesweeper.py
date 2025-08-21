""" This module implements the Minesweeper game. """
# minesweeper.py
import random


class Minesweeper:
    def __init__(self, rows:int, cols:int, num_mines:int):
        self.rows = rows
        self.cols = cols
        self.num_mines = num_mines
        self.board = [["" for _ in range(cols)] for _ in range(rows)]
        self.mines = set()
        self.revealed = set()
        self.place_mines()


    """ Randomly place mines on the board, updating adjacent cells with mine counts. """
    def place_mines(self):
        while len(self.mines) < self.num_mines:
            r,c = random.randint(0, self.rows - 1), random.randint(0, self.cols - 1)
            if (r, c) not in self.mines:
                self.mines.add((r, c))
                self.board[r][c] =  '💣'

        for r, c in self.mines:
            for i in range(r-1, r+2):
                for j in range(c-1, c+2):
                    if 0 <= i < self.rows and 0 <= j < self.cols and self.board[i][j] != '💣':
                        if self.board[i][j] == '':
                            self.board[i][j] = 1
                        else:
                            self.board[i][j] += 1



    def reveal(self, row: int, col: int) -> str:
        """Reveal a cell on the board.
        Any adjacent cells with no mines are also revealed.
        Returns "Game Over" if a mine is revealed, "Continue" otherwise.
        """
        # Hors bornes ou déjà révélée → rien à faire
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            return "Continue"
        if (row, col) in self.revealed:
            return "Continue"

        # Mine ?
        if (row, col) in self.mines or self.board[row][col] == "💣":
            self.revealed.add((row, col))
            return "Game Over"

        # Case numérotée (>0) → on révèle juste cette case
        if self.board[row][col] != "":
            self.revealed.add((row, col))
            return "Continue"

        # Case vide ("") → flood-fill pour révéler les zones vides et leurs bordures
        q = deque([(row, col)])
        while q:
            r, c = q.popleft()
            if (r, c) in self.revealed:
                continue
            self.revealed.add((r, c))

            # Si cette case est vide, on propage
            if self.board[r][c] == "":
                for i in range(r - 1, r + 2):
                    for j in range(c - 1, c + 2):
                        if 0 <= i < self.rows and 0 <= j < self.cols:
                            if (i, j) in self.mines or (i, j) in self.revealed:
                                continue
                            # On révèle toujours les numéros adjacents aux vides,
                            # et on continue la propagation uniquement sur les vides.
                            if self.board[i][j] == "":
                                q.append((i, j))
                            else:
                                self.revealed.add((i, j))

        return "Continue"



    def get_board(self) -> list:
        """Return the current visible state of the board."""
        visible = []
        for r in range(self.rows):
            row = []
            for c in range(self.cols):
                if (r, c) in self.revealed:
                    row.append(self.board[r][c])
                else:
                    row.append("■")
            visible.append(row)
        return visible


    def is_winner(self) -> bool:
        """Check if the game has been won."""
        total_cells = self.rows * self.cols
        safe_cells = total_cells - self.num_mines
        return len([cell for cell in self.revealed if cell not in self.mines]) == safe_cells




    def restart(self) -> None:
        """ Restart the game with the same parameters. """
        self.__init__(self.rows, self.cols, self.num_mines)
