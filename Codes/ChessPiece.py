import operator
from itertools import product


class ChessPiece:

    # NOTE: history is used to keep data, so chess_board.unmake_move() works properly.
    eaten_pieces_history = []
    has_moved_history = []
    position_history = []

    def __init__(self, color, x, y, unicode):
        self.moved = False
        self.color = color
        self.x = x
        self.y = y
        self.type = self.__class__.__name__
        self.unicode = unicode

    def filter_moves(self, moves, chess_board):
        final_moves = moves[:]
        for move in moves:
            chess_board.make_move(self, move[0], move[1], keep_history=True)
            if chess_board.king_is_threatened(self.color, move):
                final_moves.remove(move)
            chess_board.unmake_move(self)
        return final_moves

    def get_moves(self, chess_board):
        pass

    def get_last_eaten(self):
        return self.eaten_pieces_history.pop()

    def set_last_eaten(self, piece):
        self.eaten_pieces_history.append(piece)

    def set_position(self, x, y, keep_history):
        if keep_history:
            self.position_history.append(self.x)
            self.position_history.append(self.y)
            self.has_moved_history.append(self.moved)
        self.x = x
        self.y = y
        self.moved = True

    def set_old_position(self):
        position_y = self.position_history.pop()
        position_x = self.position_history.pop()
        self.y = position_y
        self.x = position_x
        self.moved = self.has_moved_history.pop()

    def get_score(self):
        return 0

    def __repr__(self):
        return '{}: {}|{},{}'.format(self.type, self.color, self.x, self.y)


class Pawn(ChessPiece):

    def get_moves(self, chess_board):
        moves = []
        if chess_board.game_mode == 0 and self.color == 'white' or chess_board.game_mode == 1 and self.color == 'black':
            direction = 1
        else:
            direction = -1
        x = self.x + direction
        if chess_board.has_empty_block(x, self.y):
            moves.append((x, self.y))
            if self.moved is False and chess_board.has_empty_block(x + direction, self.y):
                moves.append((x + direction, self.y))
        if chess_board.is_valid_move(x, self.y - 1):
            if chess_board.has_opponent(self, x, self.y - 1):
                moves.append((x, self.y - 1))
        if chess_board.is_valid_move(self.x + direction, self.y + 1):
            if chess_board.has_opponent(self, x, self.y + 1):
                moves.append((x, self.y + 1))
        return moves

    def get_score(self):
        return 10


class Knight(ChessPiece):

    def get_moves(self, chess_board):
        moves = []
        add = operator.add
        sub = operator.sub
        op_list = [(add, sub), (sub, add), (add, add), (sub, sub)]
        nums = [(1, 2), (2, 1)]
        combinations = list(product(op_list, nums))
        for comb in combinations:
            x = comb[0][0](self.x, comb[1][0])
            y = comb[0][1](self.y, comb[1][1])
            if chess_board.has_empty_block(x, y) or chess_board.has_opponent(self, x, y):
                moves.append((x, y))
        return moves

    def get_score(self):
        return 20


class Bishop(ChessPiece):

    def get_moves(self, chess_board):
        moves = []
        add = operator.add
        sub = operator.sub
        operators = [(add, add), (add, sub), (sub, add), (sub, sub)]
        for ops in operators:
            for i in range(1, 9):
                x = ops[0](self.x, i)
                y = ops[1](self.y, i)
                if not chess_board.is_valid_move(x, y) or chess_board.has_friend(self, x, y):
                    break
                if chess_board.has_empty_block(x, y):
                    moves.append((x, y))
                if chess_board.has_opponent(self, x, y):
                    moves.append((x, y))
                    break
        return moves

    def get_score(self):
        return 30


class Rook(ChessPiece):

    def get_moves(self, chess_board):
        moves = []
        moves += self.get_vertical_moves(chess_board)
        moves += self.get_horizontal_moves(chess_board)
        return moves

    def get_vertical_moves(self, chess_board):
        moves = []
        for op in [operator.add, operator.sub]:
            for i in range(1, 9):
                x = op(self.x, i)
                if not chess_board.is_valid_move(x, self.y) or chess_board.has_friend(self, x, self.y):
                    break
                if chess_board.has_empty_block(x, self.y):
                    moves.append((x, self.y))
                if chess_board.has_opponent(self, x, self.y):
                    moves.append((x, self.y))
                    break
        return moves

    def get_horizontal_moves(self, chess_board):
        moves = []
        for op in [operator.add, operator.sub]:
            for i in range(1, 9):
                y = op(self.y, i)
                if not chess_board.is_valid_move(self.x, y) or chess_board.has_friend(self, self.x, y):
                    break
                if chess_board.has_empty_block(self.x, y):
                    moves.append((self.x, y))
                if chess_board.has_opponent(self, self.x, y):
                    moves.append((self.x, y))
                    break
        return moves

    def get_score(self):
        return 30


class Queen(ChessPiece):

    def get_moves(self, chess_board):
        moves = []
        rook = Rook(self.color, self.x, self.y, self.unicode)
        bishop = Bishop(self.color, self.x, self.y, self.unicode)
        rook_moves = rook.get_moves(chess_board)
        bishop_moves = bishop.get_moves(chess_board)
        if rook_moves:
            moves.extend(rook_moves)
        if bishop_moves:
            moves.extend(bishop_moves)
        return moves

    def get_score(self):
        return 240


class King(ChessPiece):

    def get_moves(self, chess_board):
        moves = []
        moves += self.get_horizontal_moves(chess_board)
        moves += self.get_vertical_moves(chess_board)
        return moves

    def get_vertical_moves(self, chess_board):
        moves = []
        for op in [operator.add, operator.sub]:
            x = op(self.x, 1)
            if chess_board.has_empty_block(x, self.y) or chess_board.has_opponent(self, x, self.y):
                moves.append((x, self.y))
            if chess_board.has_empty_block(x, self.y + 1) or chess_board.has_opponent(self, x, self.y + 1):
                moves.append((x, self.y+1))
            if chess_board.has_empty_block(x, self.y - 1) or chess_board.has_opponent(self, x, self.y - 1):
                moves.append((x, self.y - 1))
        return moves

    def get_horizontal_moves(self, chess_board):
        moves = []
        for op in [operator.add, operator.sub]:
            y = op(self.y, 1)
            if chess_board.has_empty_block(self.x, y) or chess_board.has_opponent(self, self.x, y):
                moves.append((self.x, y))
        return moves

    def get_score(self):
        return 1000
