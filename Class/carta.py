# 26.01.24

SPECIAL_CARDS = ["+4", "cambio_giro", "new_colore"]
AVAILABLE_COLORS = ["r", "g", "v", "b"]
AVAILABLE_NUMBERS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "+2", "divieto"]
PESI = {
    '+4': 10,
    '+2': 9,
    'divieto': 8,
    'cambio_giro': 7,
    'new_colore': 5
}


class Carta():
    def __init__(self, colore:str, tipo:str):
        self.colore = colore
        self.tipo = tipo

    def get_peso(self):
        if self.tipo in list(PESI.keys()):
            return PESI[self.tipo]

    def to_string(self):
        return self.__dict__