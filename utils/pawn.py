from modules.termcolor import colored


class Pawn:
    """Class pour les pions

    **Status**:
        - x = pion du joueur X
        - . = emplacement vide
        - o = pion du joueur O
        - h = indice
        - p = coup possible
    """
    __slots__ = ('status', 'visible')

    def __init__(self, status: str):
        self.status: str = status
        self.visible: bool = False

    def get_player(self) -> str:
        """
        Retourne le joueur à qui appartient le Pawn

        :return: str
        """
        return self.status

    def set_visible(self, visibility: bool):
        """
        Affiche ou non les coups possibles

        :param bool visibility: is hint enabled ?
        """
        self.visible = visibility

    def __str__(self):
        if self.status == 'x':
            return colored('X', 'red')
        elif self.status == 'o':
            return colored('O', 'green')
        elif self.status == 'p':
            return colored('?', 'cyan', attrs=['bold', 'blink'])
        elif self.status == 'h' and self.visible:
            return colored('.', 'cyan', attrs=['bold', 'blink'])
        return '.'

    def __repr__(self):
        return "<utils.pawn.Pawn status='%s' visible='%s'>" \
               % (self.status, self.visible)
