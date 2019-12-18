from utils.board import Board
from utils.engine import Engine


if __name__ == '__main__':
    size = input("Entrez la taille du plateau (inf à 26 et pair): ")
    while not size.isdigit() \
            or int(size) < 4 or int(size) > 26 \
            or int(size) % 2 == 1:
        size = input("Err, entrez la taille du plateau (inf à 26 et pair): ")

    width = height = int(size)

    board = Board(width, height)
    board.make_board()

    engine = Engine(board)
    engine.start()

    try:
        while engine.is_playing:
            engine.get_action()
    except (KeyboardInterrupt, EOFError):
        engine.stop()
