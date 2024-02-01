# 26.01.24

# Variable
SPECIAL_CARDS = ["+4", "cambio_giro", "new_colore"]
AVAILABLE_COLORS = ["r", "g", "v", "b"]
AVAILABLE_NUMBERS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "+2", "divieto"]

class Carta():
    def __init__(self, colore:str, tipo:str):
        self.colore = colore
        self.tipo = tipo

    def to_string(self):
        return self.__dict__