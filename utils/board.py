import string
from typing import Union

from .pawn import Pawn


class Grid(list):
    def __init__(self, grid=None):
        super().__init__()

        if grid is None:
            grid = []

        self.grid: list = grid

    def get(self, position: list) -> Union[Pawn, bool]:
        if self.is_position_valid(position):
            return self.grid[position[0]][position[1]]
        else:
            return False

    def set(self, position: list, value: Pawn) -> None:
        if self.is_position_valid(position):
            self.grid[position[0]][position[1]] = value

    def replace(self, search: str, replace: str = '.') -> None:
        for i, row in enumerate(self.grid):
            for j, pawn in enumerate(row):
                if pawn.status == search:
                    self.grid[i][j] = Pawn(replace)

    def same(self, position: list, value: str) -> bool:
        return self.get(position).status == value

    def is_position_valid(self, position: list) -> bool:
        return 0 <= position[0] < len(self.grid) \
               and 0 <= position[1] < len(self.grid[0])

    def __str__(self):
        result = "[\n"
        for row in self.grid:
            result += f"   [{' '.join([pawn.status for pawn in row])}]\n"
        result += "]"
        return result

    def __iter__(self):
        return enumerate(self.grid)


class Board:
    __slots__ = ('width', 'height', 'grid', 'hints')

    DIRECTIONS = [
        (-1, -1), (0, -1), (1, -1),
        (-1, 0), (1, 0),
        (-1, 1), (0, 1), (1, 1)]

    def __init__(self, width: int, height: int):
        self.width: int = width
        self.height: int = height
        self.grid: Grid = Grid()
        self.hints: bool = False

    def make_board(self) -> None:
        """
        Initialise la grille a vide avec les pionts déja placés au centre

        :return: None
        """
        self.grid: Grid = Grid([
            [Pawn('.') for _ in range(self.width)]
            for _ in range(self.height)
        ])

        middle_inf, middle_sup = int((self.width / 2) - 1), int(self.width / 2)

        self.grid.set([middle_inf, middle_inf], Pawn('x'))
        self.grid.set([middle_inf, middle_sup], Pawn('o'))
        self.grid.set([middle_sup, middle_inf], Pawn('o'))
        self.grid.set([middle_sup, middle_sup], Pawn('x'))

    def set_valid_poses(self, player: str) -> bool:
        """
        Définie les positions valides et retourne True s'il y en a

        :param str player: Player who need positions
        :return: bool - True if there is/are valid position(s)
        """
        adv = 'x' if player == 'o' else 'o'

        self.grid.replace('p', '.')

        valid = False
        for i, row in self.grid:
            for j, col in enumerate(row):
                if self.grid.get([i, j]).status == adv:

                    for direction in self.DIRECTIONS:
                        vector = [i + direction[0], j + direction[1]]
                        opposite_vector = [i - direction[0], j - direction[1]]

                        if self.grid.get(vector) \
                                and self.grid.get(opposite_vector):

                            if self.grid.same(vector, '.'):
                                if self.grid.same(opposite_vector, player):
                                    self.grid.set(vector, Pawn('p'))
                                    valid = True
                                elif self.grid.same(opposite_vector, adv):
                                    if self.browse_vector(opposite_vector, direction, player):
                                        self.grid.set(vector, Pawn('p'))
                                        valid = True
        return valid

    def browse_vector(self, pose: list, vector: tuple, player: str) -> bool:
        while self.is_on_board([pose[0] - vector[0], pose[1] - vector[1]]) and \
                self.grid[pose[0]][pose[1]].status != '.':
            pose = [pose[0] - vector[0], pose[1] - vector[1]]
            if self.grid[pose[0]][pose[1]].status == player:
                return True
        return False

    def is_on_board(self, pose: list) -> bool:
        """
        Retourne True si la place est sur le damier

        :param pose: position to check
        :return: bool - True or False if the emplacement is on board or not
        """
        return 0 <= pose[0] < self.width and 1 <= pose[1] < self.height

    def is_valid_move(self, move: str) -> bool:
        """
        Retourne si le choix de position est valide

        :param str move: Position where pawn need to be placed
        :return: bool - True or False if pose is valid or not
        """
        pose = self.parser(move)

        return pose and self.is_on_board(pose) and self.grid[pose[0]][
            pose[1]].status == 'p'

    def move(self, move: str, player: str) -> list:
        """
        Ajoute un pion du joueur player a la position move

        :param str move: position to where pawn needs to be placed
        :param str player: player to move
        :return: list: Count of new pawns for each player
        """
        pose = self.parser(move)
        self.grid[pose[0]][pose[1]] = Pawn(player)
        self.flip(pose, player)
        return self.count()

    def flip(self, pose: list, player: str) -> None:
        for direction in self.DIRECTIONS:
            if self.browse_vector(pose, (0 - direction[0], 0 - direction[1]),
                                  player):
                checked_pose = [pose[0] + direction[0], pose[1] + direction[1]]
                while self.is_on_board(checked_pose):
                    if self.grid[checked_pose[0]][checked_pose[1]].status \
                            in ['.', player, 'p']:
                        break
                    else:
                        self.grid[checked_pose[0]][checked_pose[1]] = Pawn(
                            player)
                    checked_pose = [checked_pose[0] + direction[0],
                                    checked_pose[1] + direction[1]]

    def count(self) -> list:
        pawns = [0, 0]

        for row in self.grid:
            for pawn in row:
                if pawn.status == 'x':
                    pawns[0] += 1
                elif pawn.status == 'o':
                    pawns[1] += 1

        return pawns

    def toggle_hints(self) -> None:
        """
        Active ou désactive les possibilitées

        :return: None
        """
        self.hints = not self.hints

    @staticmethod
    def parser(to_parse: str) -> Union[bool, list]:
        """
        Retourne la position dans la grille de la saisie utilisateur

        :param str to_parse: Entered pose
        :return:
            - bool - False if entered pos isn't conform
            - list - Pose in the grid
        """
        if len(to_parse) == 2:
            if to_parse[0].isdigit() or not to_parse[1].isdigit():
                return False
            col = string.ascii_uppercase.index(to_parse[0].upper())
            row = int(to_parse[1]) - 1
            return [row, col]
        elif len(to_parse) == 3:
            if to_parse[0].isdigit() \
                    or (not to_parse[1].isdigit()
                        and not to_parse[2].isdigit()):
                return False
            row = int(to_parse[1:]) - 1
            col = string.ascii_uppercase.index(to_parse[0].upper())
            return [row, col]
        return False

    def get_grid(self) -> list:
        return self.grid.copy()

    def __str__(self):
        header = '   \33[33m' \
                 + ' '.join([string.ascii_uppercase[i]
                             for i in range(self.width)]
                            )
        board = f"{header}\n"

        for i, row in enumerate(self.grid, start=1):
            board += ' ' if i < 10 else ''
            board += f"\33[33m{i}\33[37m "
            for j, pawn in enumerate(row, start=1):
                pawn.set_visible(self.hints)
                board += str(f"{pawn} " if j != len(row) else pawn)
            board += '\n'

        return board[:-1]
