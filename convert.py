#!/usr/bin/env python3

from dataclasses import dataclass
from os import PathLike
from os.path import exists
import csv
from pathlib import Path



condition_map = defaultdict(
    lambda: '',
    Mint="Mint",
    NearMint="Near Mint",
    Excellent="Near Mint",
    Good="Good (Lightly Played)",
    LightPlayed="Played",
    Played="Heavily Played",
    Poor="Damaged"
    )


@dataclass(frozen=True, slots=True)
class Card:
    quantity: str
    trade_quantity: str
    name: str
    set_code: str
    set_name: str
    collector_num: str
    condition: str
    foil: str
    language: str


def split_data(line):
    data = [
        '"{}"'.format(x)
        for x in list(next(csv.reader([line], delimiter=",", quotechar='"')))
    ]

    quantity = data[1]
    trade_quantity = data[2]
    name = data[3].replace('"', "")
    set_code = data[4].lower()
    set_name = data[5]
    collector_num = data[6]
    condition = condition_map[data[7]]
    foil = '' if data[8] == 'Normal' else 'foil'
    language = data[9]

    card = Card(
        quantity,
        trade_quantity,
        name,
        set_code,
        set_name,
        collector_num,
        condition,
        foil,
        language,
        )

    return card


def convert(file_path: PathLike):
    if not exists(file_path):
        raise OSError(f'{file_path} not found. Place file in root folder.')

    input = open(file_path, "r")
    contents = input.readlines()
    input.close()

    with open("moxfield.csv", "w") as output:
        output.write(
            'Count,"Tradelist Count","Name","Edition","Condition",'
            + '"Language","Foil","Tags","Last Modified","Collector Number"\n'
            )
        for line in contents[2:]:
            card = split_data(line, contents[1])
            output.write(
                f'{card.quantity},{card.trade_quantity},"{card.name}",'
                + f"{card.set_code},{card.condition},{card.language},"
                + f'{card.foil},"","",{card.collector_num}\n'
                )


if __name__ == "__main__":
    import_path = Path("cards.csv")
    convert(import_path)
