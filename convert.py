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


def convert(in_path: PathLike, out_path: PathLike) -> None:
    if not exists(in_path):
        raise FileNotFoundError(
            f'{in_path} not found. Place file in root folder.')

    card_data = generate_cards(in_path)

    with open(out_path, 'w', newline='') as out_file:
        writer = csv.DictWriter(out_file,
                                fieldnames=moxfield_headers,
                                dialect=csv.unix_dialect)
        writer.writeheader()
        for card in card_data:
            writer.writerow(card.get_output_dict())


if __name__ == "__main__":
    input_path = Path("cards.csv")
    output_path = Path("moxfield.csv")
    convert(input_path, output_path)
