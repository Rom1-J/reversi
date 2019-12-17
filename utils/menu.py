import re
from modules.termcolor import colored
from .pawn import Pawn


class Menu:
    __slots__ = ('turns', 'player', 'pawns', 'commands', 'hints', 'size')

    def __init__(self, turns: int = 1, player: str = 'o', pawns=None,
                 commands=None, hints: bool = False, size: int = 8):
        if pawns is None:
            pawns = [2, 2]
        if commands is None:
            commands = {}

        self.turns: int = turns
        self.player: str = player
        self.pawns: list = pawns
        self.commands: dict = commands
        self.hints: bool = hints
        self.size: int = size

    def add_command(self, name: str, description: str, disabled=False) -> None:
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

    def export(self) -> dict:
        return {
            'turns': self.turns,
            'player': self.player,
            'pawns': self.pawns,
            'commands': self.commands,
            'hints': self.hints
        }

    def load(self, data: dict) -> None:
        self.turns = data.get('turns')
        self.player = data.get('player')
        self.pawns = data.get('pawns')
        self.commands = data.get('commands')
        self.hints = data.get('hints')

    def __str__(self):
        player = str(Pawn(self.player))
        menu = colored(f"Turns {self.turns}\n", "yellow")
        menu += f"It is the turn of {player}\n"
        menu += f"{player} can play\n"
        menu += "\n"
        menu += f"Pawns : {str(Pawn('x'))} {colored(self.pawns[0], 'red')}" \
                f" {int((self.pawns[0]*100)/(self.size**2))}%\n"
        menu += f"        {str(Pawn('o'))} {colored(self.pawns[1], 'green')}" \
                f" {int((self.pawns[1]*100)/(self.size**2))}%\n"
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
