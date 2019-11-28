import re
from modules.termcolor import colored
from .pawn import Pawn


class Menu:
    __slots__ = ('_turns', '_player', 'pawns', 'commands', '_hints')

    def __init__(self, turns: int = 1, player: str = 'o', pawns=None,
                 commands=None, hints: bool = False):
        if pawns is None:
            pawns = [2, 2]
        if commands is None:
            commands = {}

        self._turns: int = turns
        self._player: str = player
        self.pawns: list = pawns
        self.commands: dict = commands
        self._hints: bool = hints

    def add_command(self, name: str, description: str, disabled=False):
        """
        Ajoute une nouvelle commande avec son déclancheur et sa description

        :param str name: Trigger for the command
        :param str description: What the command do
        :param bool disabled: Is this command enabled ?
        """
        if disabled:
            description += colored(' (disabled)', 'red')
        self.commands[name] = description

    def get_commands(self) -> list:
        """
        Retourne la liste des déclancheurs pour les commandes

        :return: list - list of all possible triggers
        """
        commands = {}
        for key, value in self.commands.items():
            if '(disabled)' not in value:
                commands[key] = value
        return list(commands.keys())

    @property
    def turns(self) -> int:
        return self._turns

    @property
    def player(self) -> str:
        return self._player

    @property
    def hints(self) -> bool:
        return self._hints

    @turns.setter
    def turns(self, turn: int):
        self._turns = turn

    @player.setter
    def player(self, current: int):
        self._player = current

    @hints.setter
    def hints(self, hint: bool):
        self._hints = hint

    def __str__(self):
        player = str(Pawn(self.player))
        menu = colored(f"Turns {self.turns}\n", "yellow")
        menu += f"It is the turn of {player}\n"
        menu += f"{player} can play\n"
        menu += "\n"
        menu += f"Pawns : {str(Pawn('x'))} {colored(self.pawns[0], 'red')}\n"
        menu += f"        {str(Pawn('o'))} {colored(self.pawns[1], 'green')}\n"
        menu += "\n"
        menu += "Commands :\n"
        for name, description in self.commands.items():
            regex = r"(\*[A-Za-z]\*)"
            match = re.findall(regex, description, re.MULTILINE)[0]
            description = description.replace(match, colored(match, 'yellow'))
            description = description.replace('*', '')
            menu += f"   {colored(name, 'yellow')}: {description}\n"
        menu += "\n"
        menu += "Hints : " + (
            colored("On", 'green') if self.hints else colored("Off", 'red')
        )

        return menu
