import platform
import os
import time
from modules.termcolor import colored

from .board import Board
from .menu import Menu
from .misc import *


class Engine:
    __slots__ = ('board', 'is_playing', 'menu', 'time')

    def __init__(self, board: Board):
        self.board: Board = board
        self.is_playing: bool = False

        self.menu: Menu = Menu(size=self.board.height)
        self.menu.add_command('P', '*P*lace a pawn')
        self.menu.add_command('A', '*A*bandon')
        self.menu.add_command('H', 'Toggle *h*ints')
        self.menu.add_command('U', '*U*ndo a placement')
        self.menu.add_command('R', '*R*edo a placement')
        self.menu.hints = self.board.hints

        self.time = int(time.time())

    def start(self) -> None:
        """
        Lance l'app en faisant le premier rendu
        et en basculant a True is_playing

        :return: None
        """
        self.render()
        self.is_playing = True

    def stop(self) -> None:
        """
        Bascule is_playing a False pour stopper l'app

        :return: None
        """
        self.congratulation()
        self.is_playing = False

    def render(self) -> None:
        """
        Fait le rendu du damier et du menu en faisant un clear pour
        effacer les précédents rendus

        :return: None
        """

        can_play = self.board.set_valid_poses(self.menu.player)
        if not can_play:
            self.menu.player = 'x' if self.menu.player == 'o' else 'o'
            self.menu.turns += 1
            self.board.set_valid_poses(self.menu.player)

        os.system('cls' if platform.system() == 'Windows' else 'clear')
        flat_board = str(self.board).split('\n')
        flat_menu = str(self.menu).split('\n')

        full = max(len(flat_board), len(flat_menu))
        if full == len(flat_board):
            flat_menu.extend(['' for _ in range(full - len(flat_menu))])
        else:
            blank = ' ' * (len(
                flat_board[0]) - 5)  # pourquoi -5 ? bonne question...
            flat_board.extend(
                [blank for _ in range(full - len(flat_board))])

        for i in range(full):
            print(flat_board[i], ' ' * 6,
                  flat_menu[i])

        x = self.menu.pawns[0]
        y = self.menu.pawns[1]

        if x + y == self.menu.size ** 2:
            self.stop()

    def congratulation(self) -> None:
        """
        Affiche le message de victoire

        :return: None
        """
        if self.menu.pawns[0] > self.menu.pawns[1]:
            winner = colored('X', 'red')
            captured = self.menu.pawns[0]
        elif self.menu.pawns[1] > self.menu.pawns[0]:
            winner = colored('O', 'green')
            captured = self.menu.pawns[1]
        else:
            winner = False
            captured = self.menu.pawns[0]

        print("\n\n")
        if winner:
            print(f"Player {winner} won with "
                  f"{captured} pawns !")
        else:
            print(f"Equality, {captured} pawns for 2 players")

    def get_action(self) -> None:
        """
        Demande l'action a effectuer et l'execute si cette action est dispo

        :return: None
        """
        print("Action:")
        action = input('')
        while action.upper() not in self.menu.get_commands():
            del_top_line()  # efface la ligne supérieur
            action = input('')

        del_top_line()
        self.process_action(action.upper())

    def process_action(self, action: str) -> None:
        """
        Execute l'action demandée

        :param str action: Action to do
        :return: None
        """
        if action == 'A':
            self.stop()
        elif action == 'P':
            del_top_line()  # efface la ligne supérieur
            print("Position: (ex: D3) "
                  + colored("or type 'back' to return to the action menu",
                            'cyan',
                            )
                  )

            move = input('')
            while not self.board.is_valid_move(move) \
                    and move != 'back':
                del_top_line(2)
                print(
                    "Invalid position! please enter a new position: (ex: D3)"
                    + colored(
                        "or type 'back' to return to the action menu",
                        'cyan'
                    )
                )
                move = input('')

            if move == 'back':
                del_top_line(2)
                return self.get_action()

            backup = {
                'board': self.board.export(),
                'is_playing': self.is_playing,
                'menu': self.menu.export(),
                'time': self.time
            }
            save(f"games/{self.time}", backup)

            self.menu.pawns = self.board.move(move, self.menu.player)
            self.menu.player = 'x' if self.menu.player == 'o' else 'o'
            self.menu.turns += 1
            self.render()

            save(f"games/{self.time}", {
                'board': self.board.export(),
                'is_playing': self.is_playing,
                'menu': self.menu.export(),
                'time': self.time
            })
        elif action == 'H':
            self.board.toggle_hints()
            self.menu.hints = self.board.hints
            self.render()

        elif action == 'U':
            undo = load(f"games/{self.time}", self.menu.turns - 1)
            if undo:
                self.menu.load(undo.get('menu'))
                self.board.load(undo.get('board'))
                self.render()
            else:
                del_top_line(2)
                print(colored("No backup !", 'red'))

        elif action == 'R':
            redo = load(f"games/{self.time}", self.menu.turns + 1)
            if redo:
                self.menu.load(redo.get('menu'))
                self.board.load(redo.get('board'))
                self.render()
            else:
                del_top_line(2)
                print(colored("No backup !", 'red'))
