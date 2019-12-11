import json
import os
from typing import Union


def del_top_line(count: int = 1) -> None:
    for _ in range(count):
        print("\x1b[1A\x1b[2K\x1b[1A")


def save(path: str, data: dict) -> None:
    if not os.path.isdir(path):
        os.mkdir(path)

    actual = data.get('menu').get('turns')

    with open(f"{path}/{actual}.json", 'w') as fp:
        json.dump(data, fp, indent=4)


def load(path: str, turn: int) -> Union[bool, dict]:
    if not os.path.isdir(path) or not os.path.isfile(f"{path}/{turn}.json"):
        return False

    with open(f"{path}/{turn}.json", 'r') as fp:
        data = json.load(fp)
    return dict(data)
