# 26.01.24

# Class import
from Class.carta import Carta
from Class.mazzo import Mazzo
from Class.mano import Mano

# Variabili
numero_player = 3


def fai_mossa(index_turno: int, mazzo_iniziale: Mazzo, mazzi_giocatori: Mano):

    print("\n####################")
    print(f"-> Id giocatore: {mazzi_giocatori[index_turno].id_giocatore}")
    carta_al_centro = mazzo_iniziale.get_carta_al_centro()
    print(f"-> Carta al centro: {carta_al_centro.to_string()}")
    print(f"-> Carte giocatore: {mazzi_giocatori[index_turno].to_string(False)}")
    print(f"-> Carte valide: {mazzi_giocatori[index_turno].get_carte_valide(carta_al_centro)}")

    indice_carta_scelta = input("Scegli una carta: -1(pesca): ")
    
    if indice_carta_scelta.isdigit() or indice_carta_scelta == "-1":
        indice_carta_scelta = int(indice_carta_scelta)

        if -1 <= indice_carta_scelta and indice_carta_scelta <= len(mazzi_giocatori[index_turno].player)-1:

            # Salta
            if indice_carta_scelta == -1:
                carta_random = mazzo_iniziale.get_carta_random()
                print(f"-> Carta random: {carta_random.__dict__}")
                mazzi_giocatori[index_turno].player.append(carta_random)

            # Carta
            else:

                # Se la carta è valida
                carta_scelta = mazzi_giocatori[index_turno].player[indice_carta_scelta]
                if mazzi_giocatori[index_turno].is_carta_possibile(carta_scelta, carta_al_centro):
                    ss_return = ""

                    if carta_scelta.get_tipo() == "+4":
                        ss_return = "carte+4"

                    elif carta_scelta.get_tipo() == "+2":
                        ss_return = "carte+2"
                    
                    elif carta_scelta.get_tipo() == "new_colore":
                        nuovo_colore_scelto = input(f"Scelgi colore tra [r, g, v, b]: ")
                        mazzo_iniziale.carta_al_centro = Carta(nuovo_colore_scelto, None)

                    elif carta_scelta.get_tipo() == "divieto":
                        ss_return = "giocatori+1"

                    elif carta_scelta.get_tipo() == "cambio_giro":
                        ss_return = "giocatore_inverti"
                    
                    else:
                        mazzo_iniziale.carta_al_centro = carta_scelta

                    # Rimuovi carta dal mazzo del giocatore
                    mazzi_giocatori[index_turno].delete_card(carta_scelta, mazzo_iniziale)
                    return ss_return

                else:
                    print("Carta non valida")
                    fai_mossa(index_turno, mazzo_iniziale, mazzi_giocatori)

        else:
            print("Valore carta fuori dal numero di carte")
            fai_mossa(index_turno, mazzo_iniziale, mazzi_giocatori)

    else:
        print("Valore input sbagliato")
        fai_mossa(index_turno, mazzo_iniziale, mazzi_giocatori)

    print("\n")

def nuova_posizione(lista, posizione_attuale, spostamento):
    if 0 <= posizione_attuale <= len(lista):
        return (posizione_attuale + spostamento) % len(lista)

def cambia_giro_invertito(lista_giocatori, index_giocatore_selezionato):
    nuova_lista_giocatori = lista_giocatori[index_giocatore_selezionato:] + lista_giocatori[:index_giocatore_selezionato]
    return nuova_lista_giocatori[::-1]

def main():

    # Crezione mazzo iniziale
    index_turno = 0
    mazzo_iniziale = Mazzo(3)
    mazzo_iniziale.inizia()

    # Creazione lista con giocatori
    mazzi_giocatori = []
    for nomi in ['uno', 'due', 'tre']:
        mazzi_giocatori.append(Mano(mazzo_iniziale, f"giocatore_{nomi}"))

    # Inizio
    while 1:

        return_mossa = fai_mossa(index_turno, mazzo_iniziale, mazzi_giocatori)

        # Fine del gioco
        if len(mazzi_giocatori[index_turno].player) == 0:
            print("\nFINE")
            print(mazzi_giocatori[index_turno].id_giocatore)
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

main()