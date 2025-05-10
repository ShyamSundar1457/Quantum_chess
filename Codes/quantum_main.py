import graphics
from quantum_logic import Board


if __name__ == '__main__':
    keep_playing = True

    chess_board = Board(game_mode=0, ai=True, depth=1, log=True)  # NOTE: game_mode == 0: whites down / 1: blacks down

    while keep_playing:
        graphics.initialize()
        chess_board.place_pieces()
        graphics.draw_background(chess_board)
        keep_playing = graphics.start(chess_board)
        