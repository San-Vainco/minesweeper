import pytest
import src.minesweeper as minesweeper

def test_module_exists():
    assert minesweeper


def test_place_mines():
    game = minesweeper.Minesweeper(3, 3, 2)
    game.place_mines()
    assert len(game.mines) == 2

def test_reveal():
    import random
    random.seed(0)
    game = minesweeper.Minesweeper(3, 3, 2)
    game.place_mines()
    game.reveal(2, 2)
    assert game.revealed == {(2, 2)}


def test_get_board():
    import random
    random.seed(0)
    game = minesweeper.Minesweeper(3, 3, 2)
    game.place_mines()
    # Au début, aucune case n'est révélée
    board = game.get_board()
    assert all(cell == "■" for row in board for cell in row)

    # Révèle une case sûre
    game.reveal(2, 2)
    board = game.get_board()
    # La case (2,2) doit être différente de "■"
    assert board[2][2] != "■"


def test_is_winner():
    import random
    random.seed(0)
    game = minesweeper.Minesweeper(2, 2, 1)
    game.place_mines()

    # Révèle toutes les cases sauf les mines
    for r in range(game.rows):
        for c in range(game.cols):
            if (r, c) not in game.mines:
                game.reveal(r, c)

    assert game.is_winner() is True

    # Si on enlève une case révélée, ce n’est plus gagné
    game = minesweeper.Minesweeper(2, 2, 1)
    game.place_mines()
    for r in range(game.rows):
        for c in range(game.cols):
            if (r, c) not in game.mines and not (r == 0 and c == 0):
                game.reveal(r, c)
    assert game.is_winner() is False


def test_restart():
    import random
    random.seed(0)
    game = minesweeper.Minesweeper(3, 3, 2)
    game.place_mines()
    game.reveal(0, 0)
    assert len(game.revealed) > 0   # au moins une case est révélée

    game.restart()
    # Après restart, plus aucune case ne doit être révélée
    assert game.revealed == set()
    # Le nombre de mines doit rester identique
    assert len(game.mines) == game.num_mines
    # La taille de la grille doit être conservée
    assert len(game.board) == game.rows
    assert len(game.board[0]) == game.cols
