# 26.01.24

# Class import
from Class.carta import Carta, AVAILABLE_COLORS, AVAILABLE_NUMBERS, SPECIAL_CARDS

# General import
import random

class Mazzo():
    def __init__(self, n_player: int):
        self.mazzo = []
        self.mazzo_usato = []

        # Creazione mazzo
        for _ in range(n_player):

            # Carte normali 
            for color in AVAILABLE_COLORS:
                for number in AVAILABLE_NUMBERS:
                    self.mazzo.append(Carta(color, number))

            # Carte speciali
            for special in SPECIAL_CARDS:
                self.mazzo.append(Carta("null", special))

        # Fai uno shuffle sul mazzon inizale
        random.shuffle(self.mazzo)

    def inizia(self):
        
        # Ottiene una carte random dal mazzo sul tavolo
        self.carta_al_centro = random.choice(self.mazzo)

        # Rimuove la carta dal mazzo appena presa
        self.delete_card(self.carta_al_centro)

    def get_carta_al_centro(self) -> (Carta):
        return self.carta_al_centro

    def get_carta_random(self) -> (Carta):

        # Ottiene una carte random dal mazzo sul tavolo
        carta_scelta_random = random.choice(self.mazzo)

        # Rimuove la carte dal mazzo ma non l'aggiunge al mazzo di scarti
        self.delete_card(carta_scelta_random, random=False)

        # Return della carta random
        return carta_scelta_random

    def ripristina_mazzo(self):

        # Se non ci sono più carte
        if len(self.mazzo)-1 == 0:
            print("-> SHUFFLE \n")

            # Fai uno shuffle sull'array di tutte le carte usate
            random.shuffle(self.mazzo_usato)

            # Aggiungile alla lista di carte sul tavolo
            self.mazzo.extend(self.mazzo_usato)

            # Imposta l'array delle carte usate a []
            self.mazzo_usato = []

    def delete_card(self, carta: Carta, random:bool=True):

        # Controlla se non ci sono più carte
        self.ripristina_mazzo() 

        for i in range(len(self.mazzo)-1):
            if self.mazzo[i] == carta:

                # Aggiungi carta al mazzo di scarto se random True
                if random: 
                    self.mazzo_usato.append(self.mazzo[i])

                # Rimuovila dl mazzo
                del self.mazzo[i]
                break