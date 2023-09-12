#!/usr/bin/env python3

from dataclasses import dataclass
from os import PathLike
from os.path import exists
import csv
from pathlib import Path

file_path = "dragon_shield.csv"


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


def condition_setter(condition):
    if condition == '"Mint"':
        return '"Mint"'
    elif condition == '"NearMint"' or condition == '"Excellent"':
        return '"Near Mint"'
    elif condition == '"Good"':
        return '"Good (Lightly Played)"'
    elif condition == '"LightPlayed"':
        return '"Played"'
    elif condition == '"Played"':
        return '"Heavily Played"'
    elif condition == '"Poor"':
        return '"Damaged"'
    else:
        return '""'


def foil_setter(foilage):
    if foilage != "Normal":
        return "foil"
    else:
        return ""


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
    condition = condition_setter(data[7])
    foil = foil_setter(data[8])
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
