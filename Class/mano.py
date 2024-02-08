# 26.01.24

# Class import
from Class.carta import Carta, SPECIAL_CARDS
from Class.mazzo import Mazzo

# General import
import random

# [ class ]
class Mano():
    def __init__(self, mazzo: Mazzo, id_giocatore: str):
        self.id_giocatore = id_giocatore
        self.player = random.sample(mazzo.mazzo, 7)

        # Rimuovi le carte appena inserite
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
    
    def is_carta_possibile(self, carta_scelta: Carta, carta_al_centro: Carta) -> (bool):
        return ( carta_scelta.colore == carta_al_centro.colore or carta_scelta.tipo == carta_al_centro.tipo ) or ( carta_scelta.tipo in SPECIAL_CARDS )

    def get_carte_valide(self, carta_al_centro: Carta) -> list[int]:
        return [i for i in range(len(self.player)) if self.is_carta_possibile(self.player[i], carta_al_centro)]
    
    def get_vettore_pesi(self, carta_al_centro: Carta) -> list[list]:
        carte_valide = self.get_carte_valide(carta_al_centro)
        if len(carte_valide) > 0: 
            carte_pesi = [[carte_i, self.player[carte_i].get_peso()]  for carte_i in self.get_carte_valide(carta_al_centro)]

            # Togli carte con None e riordina
            carte_pesi_valide = list(filter(lambda x: None not in x, carte_pesi))
            return sorted(carte_pesi_valide, key=lambda x: x[1])
        else: return []

    def search_type(self, tipo_cercare: str) -> (int):
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