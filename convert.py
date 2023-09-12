#!/usr/bin/env python3

import csv
from dataclasses import dataclass
from os import PathLike
from os.path import exists
from collections import defaultdict
from pathlib import Path


condition_map = defaultdict(
    lambda: '',
    Mint="M",
    NearMint="NM",
    Excellent="NM",
    Good="LP",
    LightPlayed="MP",
    Played="HP",
    Poor="D"
    )

moxfield_headers = [
    "Count",
    "Name",
    "Edition",
    "Condition",
    "Language",
    "Foil",
    "Collector Number"
    ]


@dataclass(frozen=True, slots=True)
class CardData:
    quantity: str
    trade_quantity: str
    name: str
    set_code: str
    set_name: str
    collector_num: str
    condition: str
    foil: str
    language: str

    def get_output_dict(self) -> dict[str, str]:
        return {
            'Count': self.quantity,
            # Tradelist count is not used in Moxfield
            # 'Tradelist Count': self.trade_quantity,
            'Name': self.name,
            'Edition': self.set_code,
            'Condition': self.condition,
            'Language': self.language,
            'Foil': self.foil,
            'Collector Number': self.collector_num
            }


def generate_cards(csv_path: PathLike) -> list[CardData]:
    retval: list[CardData] = []

    with open(csv_path, 'r') as csv_file:
        # The first line is a seperator definition
        seperator = csv_file.readline().split('=')[1].strip('"\n')
        csv_reader = csv.DictReader(csv_file, delimiter=seperator)

        data_row: dict
        for data_row in csv_reader:
            # Dragon Shield adds a junk data row at the end
            if data_row['Quantity'] == '':
                continue

            foil = data_row['Printing'].lower()
            if foil not in ('etched', 'foil'):
                foil = ''

            card = CardData(
                data_row['Quantity'],
                data_row['Trade Quantity'],
                data_row['Card Name'],
                data_row['Set Code'],
                data_row['Set Name'],
                data_row['Card Number'],
                condition_map[data_row['Condition']],
                foil,
                data_row['Language'],
                )

            retval.append(card)

    return retval


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
