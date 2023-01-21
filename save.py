import shelve

import variable
from units import *
from variable import RES, SEP


class Saves:
    def __init__(self):
        self.file = shelve.open('sources/saves/saves')

    def saving(self, board):
        field_copy = board.field[:]
        for i in range(10):
            for j in range(10):
                unit = ''
                if board.field[i][j] is None:
                    continue

                if type(board.field[i][j]) == Box:
                    field_copy[i][j] = 'B'
                    continue

                if board.field[i][j].get_side() == RES:
                    unit += 'r'
                else:
                    unit += 's'

                if type(board.field[i][j]) == Trooper:
                    unit += 'T'
                elif type(board.field[i][j]) == ElitTrooper:
                    unit += 'E'
                elif type(board.field[i][j]) == Hero:
                    unit += 'H'

                if board.field[i][j].is_moved:
                    unit += '1'
                else:
                    unit += '0'

                if board.field[i][j].is_attacked:
                    unit += '1'
                else:
                    unit += '0'

                unit += str(board.field[i][j].hp)
                field_copy[i][j] = unit

        self.file['field'] = field_copy
        self.file['side'] = variable.side
        self.file['res_count'] = variable.res_count
        self.file['sep_count'] = variable.sep_count
        self.file['res_score'] = variable.res_score
        self.file['sep_score'] = variable.sep_score
        self.file['total_score'] = variable.total_score

    def load(self, board):
        field_copy = self.file['field']
        board.field = field_copy[:]
        for i in range(10):
            for j in range(10):
                unit = field_copy[i][j]
                if field_copy[i][j] is None:
                    continue

                if unit[0] == 'B':
                    board.field[i][j] = Box()
                    continue

                if unit[1] == 'T':
                    board.field[i][j] = Trooper(RES if unit[0] == 'r' else SEP)
                elif unit[1] == 'E':
                    board.field[i][j] = ElitTrooper(RES if unit[0] == 'r' else SEP)
                elif unit[1] == 'H':
                    board.field[i][j] = Hero(RES if unit[0] == 'r' else SEP)

                if unit[2] == '0':
                    board.field[i][j].is_moved = False
                else:
                    board.field[i][j].is_moved = True

                if unit[3] == '0':
                    board.field[i][j].is_attacked = False
                else:
                    board.field[i][j].is_attacked = True

                board.field[i][j].hp = int(unit[4:])

        variable.side = self.file['side']
        variable.res_count = self.file['res_count']
        variable.sep_count = self.file['sep_count']
        variable.res_score = self.file['res_score']
        variable.sep_score = self.file['sep_score']
        variable.total_score = self.file['total_score']

    def __del__(self):
        self.file.close()
