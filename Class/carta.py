# 26.01.24

class Carta():

    def __init__(self, colore:str, tipo:str):
        self.colore = colore
        self.tipo = tipo

    def get_colore(self) -> (str):
        return self.colore
    
    def get_tipo(self) -> (str):
        return self.tipo
    
    def to_string(self):
        return self.__dict__
