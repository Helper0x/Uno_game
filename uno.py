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
numero_player = 4
giocatori = ['uno', 'due', 'tre', '4']


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

def play_color(is_re, mazzo: Mazzo):
    if not is_re:
        return random.choice(AVAILABLE_COLORS)
    else:
        color_counts = {col: 0 for col in AVAILABLE_COLORS}
        for carte in mazzo.player:
            if carte.colore != "nera":  # Escludi carte speciali
                color_counts[carte.colore] += 1
        return max(color_counts, key=color_counts.get)


def get_carda_pesante(carte_centro: Carta, mazzo: Mano):
    for index, carta in enumerate(mazzo.player):
        if carta.tipo in ["+4"]:
            return index
        if carta.tipo in ["+2", "divieto"] and carta.colore == carte_centro.colore:
            return index
    return -1

def get_best_by_color(carte_centro: Carta, mazzo: Mano):
    colori_carte = {col: [] for col in AVAILABLE_COLORS}
    for i in range(len(mazzo.player)):
        carta = mazzo.player[i]
        if carta.colore != "nera":
            colori_carte[carta.colore].append(i)

    indici_colori_centro = colori_carte[carte_centro.colore]

    return random.choice(indici_colori_centro) if indici_colori_centro else -1


def play_card(is_re, indici_carte_validi, carte_next, carte_centro, mazzo: Mano):
    if len(indici_carte_validi) == 0:
        return -1

    if is_re and carte_next <= 2:
        index_best_card = get_carda_pesante(carte_centro, mazzo)
        if index_best_card != -1:
            index_cambio_giro = mazzo.search_type("cambio_giro")

            if index_cambio_giro != -1:
                return index_cambio_giro
            else:
                indice_col = get_best_by_color(carte_centro, mazzo)
                return indice_col if indice_col != -1 else random.choice(indici_carte_validi)
        
    if is_re:
        indici_special = []
        indici_normali = []
        
        for spec in ["+2", "+4", "divieto", "cambio_giro"]:
            indici_special.append(mazzo.search_type(spec))
        indice_speciali_filter = list(filter(lambda x: x != -1, indici_special))  # Remove -1
        
        for spec in AVAILABLE_COLORS[0:9]:
            indici_normali.append(mazzo.search_type(spec))
        indice_normal_filter = list(filter(lambda x: x != -1, indici_special))  # Remove -1
        indice_normal_filter.extend(indice_speciali_filter)

        indice_normal_filter_valid = []
        for index_new in indice_normal_filter:
            if index_new in indici_carte_validi:
                indice_normal_filter_valid.append(index_new)

        if len(indice_normal_filter_valid) != 0:
            return indice_normal_filter_valid[0]
        else:

            indice_col = get_best_by_color(carte_centro, mazzo)
            return indice_col if indice_col != -1 else random.choice(indici_carte_validi)
            

    if not is_re:
        return random.choice(indici_carte_validi)

def logic_stategia(id_giocatore:str, carta_centro:Carta, mazzo:Mano, carte_next:int, get_colore:bool):
    id_player = id_giocatore.split("_")[1]
    is_re = (id_player == "uno")
    carte_valide = mazzo.get_carte_valide(carta_centro)

    if get_colore: 
        return play_color(is_re, mazzo) 
    else:
        if len(carte_valide) == 0: 
            return -1
        else: 
            return play_card(is_re, carte_valide, carte_next, carta_centro, mazzo) 


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
    indice_carta_scelta = logic_stategia(id_giocatore, carta_al_centro, mazzi_giocatori[index_turno], len(mazzi_giocatori[(index_turno+2) % len(giocatori)].player), False)
    print(f"--> Carta scelta: {indice_carta_scelta}")

    # Carte logic
    # Salta
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
            nuovo_colore_scelto = logic_stategia(id_giocatore, carta_al_centro, mazzi_giocatori[index_turno], len(mazzi_giocatori[(index_turno+2) % len(giocatori)].player), True)
            print(f"--> Colore scelto: {nuovo_colore_scelto}")
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
    for i in range(1000):
        print(f"Gioco: {i}")
        with suppress_print():
            result_gioco = main().split("_")[1]
        stat[result_gioco] += 1

    print(stat)

main()
