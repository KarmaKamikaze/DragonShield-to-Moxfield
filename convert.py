from os import PathLike
from os.path import exists
import csv
from pathlib import Path

file_path = "dragon_shield.csv"


class Card_Data:
    def __init__(
        self,
        quantity,
        trade_quantity,
        name,
        set_code,
        set_name,
        collector_num,
        condition,
        foil,
        language,
    ):
        self.quantity = quantity
        self.trade_quantity = trade_quantity
        self.name = name
        self.set_code = set_code
        self.set_name = set_name  # set name is not relevant to conversion
        self.collector_num = collector_num
        self.condition = condition
        self.foil = foil
        self.language = language


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

    card = Card_Data(
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
        print(f'File not found. Place "{file_path}" in root folder.')
    else:
        input = open(file_path, "r")
        contents = input.readlines()
        input.close()

        with open("moxfield.csv", "w") as output:
            output.write(
                'Count,"Tradelist Count","Name","Edition","Condition",'
                + '"Language","Foil","Tags","Last Modified","Collector Number"\n'
            )
            for line in contents[2:]:
                card = split_data(line)
                output.write(
                    f'{card.quantity},{card.trade_quantity},"{card.name}",'
                    + f"{card.set_code},{card.condition},{card.language},"
                    + f'{card.foil},"","",{card.collector_num}\n'
                )


if __name__ == "__main__":
    import_path = Path("cards.csv")
    convert(import_path)
