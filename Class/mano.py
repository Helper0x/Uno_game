# 26.01.24

# Class import
from Class.carta import Carta, SPECIAL_CARDS
from Class.mazzo import Mazzo

# General import
import random

# [ class ]
class Mano():
    carte_per_giocatore = 7
    
    def __init__(self, mazzo: Mazzo, id_giocatore: str):
        self.id_giocatore = id_giocatore
        self.player = random.sample(mazzo.mazzo, self.carte_per_giocatore)

        # Rimuovi le carte dal mazzo appena prese
        for card in self.player:
            mazzo.delete_card(card)

    def delete_card(self, carta: Carta, mazzo: Mazzo):
        for i in range(len(self.player)):
            if self.player[i] == carta:

                # Aggiungi la carta al mazzo di scarti
                mazzo.mazzo_usato.append(self.player[i])

                # Elimina dal mazzo del giocatore
                del self.player[i]
                break
    
    def is_carta_possibile(self, carta_scelta: Carta, carta_al_centro: Carta):
        return ( carta_scelta.colore == carta_al_centro.colore or carta_scelta.tipo == carta_al_centro.tipo ) or ( carta_scelta.tipo in SPECIAL_CARDS )

    def get_carte_valide(self, carta_al_centro: Carta):
        indici_validi = []

        for i in range(len(self.player)):
            if self.is_carta_possibile(self.player[i], carta_al_centro):
                indici_validi.append(i)

        return indici_validi
    
    def search_type(self, tipo_cercare: str):
        for i in range(len(self.player)):
            if self.player[i].tipo == tipo_cercare:
                return i
        return -1

    def to_string(self, show:bool = False):
        s = ""

        for i, card in enumerate(self.player):
            if show:
                print(f"{i}: {card.to_string()}")
            s += f"{i}({card.colore}_{card.tipo}) "
            
        return s