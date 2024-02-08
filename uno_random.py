# 26.01.24 -> 1.02.24

# Class import
from Class.carta import Carta, AVAILABLE_COLORS
from Class.mazzo import Mazzo
from Class.mano import Mano

# General import
import random, sys
from contextlib import contextmanager

# Variabili
numero_player = 3
x_cost_mazzo = 5
giocatori = ['uno', 'due', 'tre']
DO_STAT = False


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
    if get_colore: return random.choice(AVAILABLE_COLORS)
    else:
        if len(lista_carte_valide) == 0: return -1
        else: return random.choice(lista_carte_valide)

def fai_mossa(index_turno: int, mazzo_iniziale: Mazzo, mazzi_giocatori: Mano):

    print("\n####################")
    print(f"-> Id giocatore: {mazzi_giocatori[index_turno].id_giocatore}")
    print(f"-> Carta al centro: {mazzo_iniziale.carta_al_centro.to_string()}")
    print(f"-> Carte giocatore: {mazzi_giocatori[index_turno].to_string(False)}")
    carte_valide = mazzi_giocatori[index_turno].get_carte_valide(mazzo_iniziale.carta_al_centro)
    print(f"-> Carte valide: {carte_valide}")

    # Scelta della carta random
    indice_carta_scelta = logic_stategia(carte_valide, False)
    print(f"-> Carte scelta: {indice_carta_scelta}")

    # Salta
    if indice_carta_scelta == -1:
        carta_random = mazzo_iniziale.get_carta_random()
        mazzi_giocatori[index_turno].player.append(carta_random)

    # Se la carta è valida
    else:
        carta_scelta = mazzi_giocatori[index_turno].player[indice_carta_scelta]
                    
        if carta_scelta.tipo == "new_colore":
            nuovo_colore_scelto = logic_stategia(carte_valide, True)
            print("Colore scelto => ", nuovo_colore_scelto)
            mazzo_iniziale.carta_al_centro = Carta(nuovo_colore_scelto, "nera")
        
        if carta_scelta.colore != "nera":
            mazzo_iniziale.carta_al_centro = carta_scelta

        # Rimuovi carta dal mazzo del giocatore
        mazzi_giocatori[index_turno].delete_card(carta_scelta, mazzo_iniziale)


def main():

    # Crezione mazzo iniziale
    index_turno = 0
    mazzo_iniziale = Mazzo(x_cost_mazzo)
    mazzo_iniziale.inizia()

    # Creazione lista con giocatori
    mazzi_giocatori = []
    for nomi in giocatori:
        mazzi_giocatori.append(Mano(mazzo_iniziale, f"giocatore_{nomi}"))

    while 1:

        fai_mossa(index_turno, mazzo_iniziale, mazzi_giocatori)

        if len(mazzi_giocatori[index_turno].player) == 1:
            print("\nIl giocatore: ", mazzi_giocatori[index_turno].id_giocatore, " chiama UNO")

        if len(mazzi_giocatori[index_turno].player) == 0:
            print("\nVince il giocatore: ", mazzi_giocatori[index_turno].id_giocatore)
            return mazzi_giocatori[index_turno].id_giocatore

        if mazzo_iniziale.carta_al_centro.tipo == "divieto":
            index_turno = nuova_posizione(mazzi_giocatori, index_turno, 2)  

        elif mazzo_iniziale.carta_al_centro.tipo  == "cambio_giro":
            mazzi_giocatori = cambia_giro_invertito(mazzi_giocatori, index_turno-2)

        else:
    
            # Incrementa giocatore di 1
            index_turno = nuova_posizione(mazzi_giocatori, index_turno, 1)

            if mazzo_iniziale.carta_al_centro.tipo == "+4":
                for _ in range(4):
                    carta_random = mazzo_iniziale.get_carta_random()
                    mazzi_giocatori[index_turno].player.append(carta_random)

            if mazzo_iniziale.carta_al_centro.tipo == "+2":
                for _ in range(2):
                    carta_random = mazzo_iniziale.get_carta_random()
                    mazzi_giocatori[index_turno].player.append(carta_random)

def statistica():
    
    stat = {nome:0 for nome in giocatori}
    for i in range(2000):
        print(f"Gioco: {i}")
        with suppress_print():
            result_gioco = main().split("_")[1]
        stat[result_gioco] += 1

    print(stat)


if not DO_STAT:
    main()
else:
    statistica()