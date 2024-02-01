# 26.01.24 -> 1.02.24

# Class import
from Class.carta import Carta, AVAILABLE_COLORS
from Class.mazzo import Mazzo
from Class.mano import Mano

# General import
import time, random
from contextlib import contextmanager
import sys

# Variabili
numero_player = 5
giocatori = ['uno', 'due', 'tre', 'quattro', 'cinque']


@contextmanager
def suppress_print():
    original_stdout = sys.stdout
    sys.stdout = open('nul', 'w')
    try:
        yield
    finally:
        sys.stdout = original_stdout


def nuova_posizione(lista, posizione_attuale, spostamento):
    return (posizione_attuale + spostamento) % len(lista)

def cambia_giro_invertito(lista_giocatori, index_giocatore_selezionato):
    nuova_lista_giocatori = lista_giocatori[index_giocatore_selezionato:] + lista_giocatori[:index_giocatore_selezionato]
    return nuova_lista_giocatori[::-1]

def logic_stategia(lista_carte_valide, get_colore):
    if get_colore:
        return random.choice(AVAILABLE_COLORS)
    else:
        if len(lista_carte_valide) == 0:
            return -1
        else:
            return random.choice(lista_carte_valide)

def fai_mossa(index_turno: int, mazzo_iniziale: Mazzo, mazzi_giocatori: Mano):

    id_giocatore = mazzi_giocatori[index_turno].id_giocatore
    carta_al_centro = mazzo_iniziale.carta_al_centro
    carte_valide = mazzi_giocatori[index_turno].get_carte_valide(carta_al_centro)

    print("\n####################")
    print(f"-> Id giocatore: {id_giocatore}")
    print(f"-> Carta al centro: {carta_al_centro.to_string()}")
    print(f"-> Carte giocatore: {mazzi_giocatori[index_turno].to_string(False)}")
    print(f"-> Carte valide: {carte_valide}")

    # Scelta della carta random
    indice_carta_scelta = logic_stategia(carte_valide, False)

    # Salta
    print(f"-> Carte scelta: {indice_carta_scelta}")
    if indice_carta_scelta == -1:
        carta_random = mazzo_iniziale.get_carta_random()
        print(f"-> Carta random: {carta_random.__dict__}")
        mazzi_giocatori[index_turno].player.append(carta_random)

    # Carta
    else:

        # Se la carta è valida
        carta_scelta = mazzi_giocatori[index_turno].player[indice_carta_scelta]
        ss_return = ""

        if carta_scelta.tipo == "+4":
            ss_return = "carte+4"

        elif carta_scelta.tipo == "+2":
            ss_return = "carte+2"
                    
        elif carta_scelta.tipo == "new_colore":
            nuovo_colore_scelto = logic_stategia(carte_valide, True)
            mazzo_iniziale.carta_al_centro = Carta(nuovo_colore_scelto, None)

        elif carta_scelta.tipo == "divieto":
            ss_return = "giocatori+1"

        elif carta_scelta.tipo == "cambio_giro":
            ss_return = "giocatore_inverti"
                    
        else:
            mazzo_iniziale.carta_al_centro = carta_scelta

        # Rimuovi carta dal mazzo del giocatore
        mazzi_giocatori[index_turno].delete_card(carta_scelta, mazzo_iniziale)
        return ss_return

    print("\n")

def main():

    # Crezione mazzo iniziale
    index_turno = 0
    mazzo_iniziale = Mazzo(3)
    mazzo_iniziale.inizia()

    # Creazione lista con giocatori
    mazzi_giocatori = []
    for nomi in giocatori:
        mazzi_giocatori.append(Mano(mazzo_iniziale, f"giocatore_{nomi}"))

    # Inizio
    while 1:

        return_mossa = fai_mossa(index_turno, mazzo_iniziale, mazzi_giocatori)

        # Fine del gioco
        if len(mazzi_giocatori[index_turno].player) == 0:
            print("\nFINE")
            print(mazzi_giocatori[index_turno].id_giocatore)
            return mazzi_giocatori[index_turno].id_giocatore
            break

        if return_mossa == "giocatori+1":
            index_turno = nuova_posizione(mazzi_giocatori, index_turno, 2)  

        elif return_mossa == "giocatore_inverti":
            mazzi_giocatori = cambia_giro_invertito(mazzi_giocatori, index_turno-2)

        else:
    
            # Incrementa giocatore di 1
            index_turno = nuova_posizione(mazzi_giocatori, index_turno, 1)

            if return_mossa == "carte+4":
                for _ in range(4):
                    carta_random = mazzo_iniziale.get_carta_random()
                    print(f"-> Carta random: {carta_random.__dict__}, aggiunta al mazzo: {index_turno}")
                    mazzi_giocatori[index_turno].player.append(carta_random)

            if return_mossa == "carte+2":
                for _ in range(2):
                    carta_random = mazzo_iniziale.get_carta_random()
                    print(f"-> Carta random: {carta_random.__dict__}, aggiunta al mazzo: {index_turno}")
                    mazzi_giocatori[index_turno].player.append(carta_random)

def statistica():
    
    stat = {nome:0 for nome in giocatori}
    for i in range(2000):
        print(f"Gioco: {i}")
        with suppress_print():
            result_gioco = main().split("_")[1]
        stat[result_gioco] += 1

    print(stat)

statistica()