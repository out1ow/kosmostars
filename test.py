import tkinter
from tkinter import messagebox

WHITE = 1
BLACK = 2
BRD_ROWS = BRD_COLS = 8
CELL_SZ = 100
WINNER = ''
command = '_ _'
root = tkinter.Tk()
root.title('Witcher 4')
canvas = tkinter.Canvas(root, width=CELL_SZ * BRD_ROWS + 500,
                        height=CELL_SZ * BRD_COLS, background='grey')


def correct_coords(row, col):
    return 0 <= row < 8 and 0 <= col < 8


def opponent(color):
    if color == WHITE:
        return BLACK
    else:
        return WHITE


def drawing(board):
    def output():
        global command
        command = comand_line.get('1.0', '1.30').strip()
        comand_line.delete('1.0', '1.30')

    comand_line = tkinter.Text(root, height=5, width=50, bd=4, foreground='green')
    exit_button = tkinter.Button(root, text='exit', width=10, height=2, command=root.destroy)
    move_button = tkinter.Button(root, text='make move', width=58, height=2, command=output)

    cell_colors = ['white', 'black']
    ci = 0

    for row in range(BRD_ROWS):
        for col in range(BRD_COLS):
            x1, y1 = col * CELL_SZ, row * CELL_SZ
            x2, y2 = col * CELL_SZ + CELL_SZ, row * CELL_SZ + CELL_SZ
            canvas.create_rectangle((x1, y1), (x2, y2), fill=cell_colors[ci])
            ci = not ci
        ci = not ci
    for col in range(7):
        canvas.create_text(10, col * CELL_SZ + 90, fill='blue', font='Times 15', text=7 - col)
    for row in range(BRD_ROWS):
        canvas.create_text(row * CELL_SZ + 10, 780, fill='blue', font='Times 15', text=row)
        for col in range(BRD_COLS):
            canvas.create_text(col * 100 + 50, row * 100 + 50, fill='red', font='Times 20',
                               text=board.cell(7 - row, col))
    canvas.create_text(1050, 100, fill='black', font='Times 11',
                       text='Команды:\n'
                            'move <row> <col> <row1> <row1> -- '
                            'ход из клетки (row, col) \n \t \t \t \t  '
                            'в клетку (row1, col1) \n'
                            'castling left -- рокировка влево \n'
                            'castling right -- рокировка вправо \n'
                            'snap pawn <row> <col> <row1> <col1> <figure> -- '
                            'поменять пешку,\n \t \t \t \t'
                            'дошедшую до конца поля, на figure')
    canvas.pack()
    comand_line.place(x=850, y=650)
    move_button.place(x=850, y=750)
    exit_button.place(x=1200, y=10)


def main():
    global command
    board = Board()
    drawing(board)
    console = tkinter.Label(root, font='Times 15')
    while True:
        if WINNER == WHITE:
            winner = tkinter.Label(root, text='Белые победили', font='Times 35',
                                   foreground='white', background='green')
            winner.place(x=650, y=400)
            break
        elif WINNER == BLACK:
            winner = tkinter.Label(root, text='Чёрные победили', font='Times 35',
                                   foreground='black', background='green')
            winner.place(x=650, y=400)
            break
        console.place(x=850, y=600)
        if board.current_player_color() == WHITE:
            console['text'] = 'Ход белых:'
        else:
            console['text'] = 'Ход чёрных:'
        console.place(x=850, y=600)
        if command != '':
            move_type = command.split()[0]
            if move_type == 'move':
                move_type, row, col, row1, col1 = command.split()
                row, col, row1, col1 = int(row), int(col), int(row1), int(col1)
                if board.move_piece(row, col, row1, col1):
                    console['text'] = 'Ход успешен'
                else:
                    messagebox.showerror('Error', 'Координаты некорректы! Попробуйте другой ход!')
                drawing(board)
            elif move_type == 'castling':
                move_type, direction = command.split()
                if board.color == WHITE:
                    if direction == 'left':
                        if board.castling0():
                            console['text'] = 'Ход успешен'
                    elif direction == 'right':
                        if board.castling7():
                            console['text'] = 'Ход успешен'
                        else:
                            messagebox.showerror('Error', 'Невозможно совершить рокировку')
                    else:
                        messagebox.showerror('Error',
                                             'Координаты некорректы! Попробуйте другой ход!')
                else:
                    if direction == 'left':
                        board.castling7()
                        console['text'] = 'Ход успешен'
                    elif direction == 'right':
                        if board.castling0():
                            console['text'] = 'Ход успешен'
                        else:
                            messagebox.showerror('Error', 'Невозможно совершить рокировку')
                    else:
                        messagebox.showerror('Error',
                                             'Координаты некорректы! Попробуйте другой ход!')
                drawing(board)
            elif move_type == 'snap':
                move_type, row, col, row1, col1, figure = command.split()
                row, col, row1, col1 = int(row), int(col), int(row1), int(col1)
                if board.move_and_promote_pawn(row, col, row1, col1, figure):
                    console['text'] = 'Ход успешен'
                else:
                    messagebox.showerror('Error', 'Координаты некорректы! Попробуйте другой ход!')
                drawing(board)
            else:
                pass
        command = '_ _'
        console.place(x=850, y=600)
        root.update()


class Board:
    def __init__(self):
        self.color = WHITE
        self.field = []
        for row in range(8):
            self.field.append([None] * 8)
        self.field[0] = [
            Rook(WHITE), Knight(WHITE), Bishop(WHITE), Queen(WHITE),
            King(WHITE), Bishop(WHITE), Knight(WHITE), Rook(WHITE)
        ]
        self.field[1] = [
            Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE),
            Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE)
        ]
        self.field[6] = [
            Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK),
            Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK)
        ]
        self.field[7] = [
            Rook(BLACK), Knight(BLACK), Bishop(BLACK), Queen(BLACK),
            King(BLACK), Bishop(BLACK), Knight(BLACK), Rook(BLACK)]

    def current_player_color(self):
        return self.color

    def cell(self, row, col):
        piece = self.field[row][col]
        if piece is None:
            return '  '
        color = piece.get_color()
        c = 'w' if color == WHITE else 'b'
        return c + piece.char()

    def get_piece(self, row, col):
        return self.field[row][col]

    def move_piece(self, row, col, row1, col1):
        global WINNER
        if not correct_coords(row, col) or not correct_coords(row1, col1):
            return False
        if row == row1 and col == col1:
            return False
        piece = self.field[row][col]
        if piece is None:
            return False
        if piece.get_color() != self.color:
            return False
        if self.field[row1][col1] is None:
            if not piece.can_move(self, row, col, row1, col1):
                return False
        elif self.field[row1][col1].get_color() == opponent(piece.get_color()):
            if not piece.can_attack(self, row, col, row1, col1):
                return False
            elif self.field[row1][col1].char() == 'K':
                WINNER = self.color
        else:
            return False
        piece.is_moved = True
        self.field[row][col] = None
        self.field[row1][col1] = piece
        self.color = opponent(self.color)
        return True

    def move_and_promote_pawn(self, row, col, row1, col1, char):
        if self.get_piece(row, col).char() != 'P':
            return False
        if row1 != 0 and row1 != 7:
            return False
        if char == 'P' or char == 'K':
            return False
        if self.get_piece(row, col).get_color() == WHITE and row1 == 7:
            if self.move_piece(row, col, row1, col1):
                if char == 'Q':
                    self.field[row1][col1] = Queen(WHITE)
                elif char == 'R':
                    self.field[row1][col1] = Rook(WHITE)
                elif char == 'B':
                    self.field[row1][col1] = Bishop(WHITE)
                elif char == 'N':
                    self.field[row1][col1] = Knight(WHITE)
                else:
                    return False
                return True
            return False
        elif self.get_piece(row, col).get_color() == BLACK and row1 == 0:
            if self.move_piece(row, col, row1, col1):
                if char == 'Q':
                    self.field[row1][col1] = Queen(BLACK)
                elif char == 'R':
                    self.field[row1][col1] = Rook(BLACK)
                elif char == 'B':
                    self.field[row1][col1] = Bishop(BLACK)
                elif char == 'N':
                    self.field[row1][col1] = Knight(BLACK)
                else:
                    return False
                return True
        return False

    def castling0(self):
        if self.color == WHITE:
            if self.field[0][4] is None:
                return False
            if self.field[0][4].char() != 'K':
                return False
            color = self.field[0][4].get_color
            if self.field[0][0] is None:
                return False
            if self.field[0][4].is_moved:
                return False
            if self.field[0][0].is_moved:
                return False
            if self.field[0][0].char() == 'R':
                if self.move_piece(0, 0, 0, 3):
                    self.field[0][4] = None
                    self.field[0][2] = King(color)
                    return True
        else:
            if self.field[7][4] is None:
                return False
            if self.field[7][4].char() != 'K':
                return False
            color = self.field[7][4].get_color
            if self.field[7][0] is None:
                return False
            if self.field[7][4].is_moved:
                return False
            if self.field[7][0].is_moved:
                return False
            if self.field[7][0].char() == 'R':
                if self.move_piece(7, 0, 7, 3):
                    self.field[7][4] = None
                    self.field[7][2] = King(color)
                    return True
        return False

    def castling7(self):
        if self.color == WHITE:
            if self.field[0][4] is None:
                return False
            if self.field[0][4].char() != 'K':
                return False
            color = self.field[0][4].get_color
            if self.field[0][7] is None:
                return False
            if self.field[0][4].is_moved:
                return False
            if self.field[0][7].is_moved:
                return False
            if self.field[0][7].char() == 'R':
                if self.move_piece(0, 7, 0, 5):
                    self.field[0][4] = None
                    self.field[0][6] = King(color)
                    return True
        else:
            if self.field[7][4] is None:
                return False
            if self.field[7][4].char() != 'K':
                return False
            color = self.field[7][4].get_color
            if self.field[7][7] is None:
                return False
            if self.field[7][4].is_moved:
                return False
            if self.field[7][7].is_moved:
                return False
            if self.field[7][7].char() == 'R':
                if self.move_piece(7, 7, 7, 5):
                    self.field[7][4] = None
                    self.field[7][6] = King(color)
                    return True
        return False


class Figure:
    def __init__(self, color):
        self.color = color
        self.is_moved = False

    def get_color(self):
        return self.color

    def char(self):
        pass

    def can_move(self):
        pass

    def can_attack(self):
        pass


class Pawn(Figure):
    def __init__(self, color):
        super().__init__(color)

    def char(self):
        return 'P'

    def can_move(self, board, row, col, row1, col1):
        # Пешка может ходить только по вертикали
        if col != col1:
            return False

        # Пешка может сделать из начального положения ход на 2 клетки
        # вперёд, поэтому поместим индекс начального ряда в start_row.
        if self.color == WHITE:
            direction = 1
            start_row = 1
        else:
            direction = -1
            start_row = 6

        # ход на 1 клетку
        if row + direction == row1:
            return True

        # ход на 2 клетки из начального положения
        if (row == start_row
                and row + 2 * direction == row1
                and board.field[row + direction][col] is None):
            return True
        return False

    def can_attack(self, board, row, col, row1, col1):
        direction = 1 if (self.color == WHITE) else -1
        return (row + direction == row1
                and (col + 1 == col1 or col - 1 == col1))


class Rook(Figure):
    def __init__(self, color):
        super().__init__(color)

    def char(self):
        return 'R'

    def can_move(self, board, row, col, row1, col1):
        # Невозможно сделать ход в клетку,
        # которая не лежит в том же ряду или столбце клеток.
        if row != row1 and col != col1:
            return False

        step = 1 if (row1 >= row) else -1
        for r in range(row + step, row1, step):
            # Если на пути по вертикали есть фигура
            if not (board.get_piece(r, col) is None):
                return False

        step = 1 if (col1 >= col) else -1
        for c in range(col + step, col1, step):
            # Если на пути по горизонтали есть фигура
            if not (board.get_piece(row, c) is None):
                return False
        return True

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class King(Figure):
    def __init__(self, color):
        super().__init__(color)

    def char(self):
        return 'K'

    def can_move(self, board, row, col, row1, col1):
        if abs(row1 - row) == 1 and col1 == col:
            return True
        elif row == row1 and abs(col1 - col) == 1:
            return True
        elif abs(row1 - row) == 1 and abs(col1 - col) == 1:
            return True
        return False

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class Knight(Figure):
    def __init__(self, color):
        super().__init__(color)

    def char(self):
        return 'N'  # kNight, буква 'K' уже занята королём

    def can_move(self, board, row, col, row1, col1):
        if ((abs(row1 - row) == 2 and abs(col1 - col) == 1) or
            (abs(row1 - row) == 1 and abs(col1 - col) == 2)) and \
                (board.get_piece(row1, col1) is None):
            return True
        else:
            return False

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class Bishop(Figure):
    def __init__(self, color):
        super().__init__(color)

    def char(self):
        return 'B'

    def can_move(self, board, row, col, row1, col1):
        if row - col == row1 - col1:
            step = 1 if (row1 >= row) else -1
            for i in range(row + step, row1, step):
                a = col - row + i
                if not (board.get_piece(i, a) is None):
                    return False
            return True
        if row + col == row1 + col1:
            step = 1 if (row1 >= row) else -1
            for i in range(row + step, row1, step):
                a = row + col - i
                if not (board.get_piece(i, a) is None):
                    return False
            return True
        return False

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class Queen(Bishop, Rook, Figure):
    def __init__(self, color):
        super().__init__(color)

    def char(self):
        return 'Q'

    def can_move(self, board, row, col, row1, col1):
        return Bishop.can_move(self, board, row, col, row1, col1) or \
               Rook.can_move(self, board, row, col, row1, col1)

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


if __name__ == "__main__":
    main()
root.mainloop()
