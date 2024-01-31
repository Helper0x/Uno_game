# 25.01.24

# Import
import random

# Variable
carte_per_giocatore = 8



def is_mossa_possibile(carta_scelta, carta_attuale):
    return carta_scelta[0] == carta_attuale[0] or carta_scelta[1] == carta_attuale[1]

def delete_iniziale(player_mazzo, totale_mazzo):
    for i in range(len(player_mazzo)-1):
        for k in range(len(totale_mazzo)-1):
            if totale_mazzo[k] == player_mazzo[i]:
                del totale_mazzo[i]

    return totale_mazzo

def print_carte_valide(mazzo, carta_al_centro):
    s = ""
    s_all = ""
    for i in range(len(mazzo)):
        s_all += f"{i}: {mazzo[i]} | "
        if is_mossa_possibile(mazzo[i], carta_al_centro):
            s += f"{i}: {mazzo[i]} | "

    if s != "":
        print(f"Carte valid => {s}, carte nel mazzo => {s_all}, n carte => {len(mazzo)}")
    else:
        print(f"Carte valid => [Nessuna: ss], carte nel mazzo => {s_all}, n carte => {len(mazzo)}")

def dai_carta_random(mazzo, mazzo_totale):

    if len(mazzo_totale) > 0:

        mazzo.extend([random.choice(mazzo_totale)])

        for k in range(len(mazzo_totale)-1):
            if mazzo_totale[k] == mazzo[-1]:
                del mazzo_totale[k]

        return mazzo
    
    else:
        print("Carte finite")
        return mazzo

def fai_la_mossa(mazzo, carta_attuale, mazzo_totale):
    print_carte_valide(mazzo, carta_attuale)
    
    index_carta = input("Scegli l'indice dal mazzo: ").strip()

    if str(index_carta) == "ss":
        return carta_attuale, dai_carta_random(mazzo, mazzo_totale), False
    
    elif 0 <= int(index_carta) <= len(mazzo):
        index_carta = int(index_carta)

        if is_mossa_possibile(mazzo[index_carta], carta_attuale):
            carta_attuale = mazzo[index_carta]
            del mazzo[index_carta]

            return carta_attuale, mazzo, True

        else:
            print(f"Non puoi giocare questa carta: {mazzo[index_carta]}")
            fai_la_mossa(mazzo, carta_attuale, mazzo_totale)

    else:
        print("Carta fuori dal mazzo")
        fai_la_mossa(mazzo, carta_attuale, mazzo_totale)

def start_game():

    colori_disponibili = ["r", "g", "v", "b"]
    numeri_disponibili = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    carte_disponibili = []
    carte_usate = []

    for col in colori_disponibili:
        for num in numeri_disponibili:
            carte_disponibili.append([col, num])

    player_1 = random.sample(carte_disponibili, carte_per_giocatore)
    player_2 = random.sample(carte_disponibili, carte_per_giocatore)
    carte_disponibili = delete_iniziale(player_1, carte_disponibili)
    carte_disponibili = delete_iniziale(player_2, carte_disponibili)
    carta_iniziale = random.choice(carte_disponibili)

    print(f"Carta al centro {carta_iniziale}, carte del mazzo rimanenti: {len(carte_disponibili)}")
    while 1:

        print("\nGiocatore 1:")
        carta_iniziale, player_1, return_valid = fai_la_mossa(player_1, carta_iniziale, carte_disponibili)
        if return_valid:
            print("Carta al centro => ", carta_iniziale, "\n")
            carte_usate.extend([carta_iniziale])
        if player_1 == False:
            print("Carte finite ancora")

        print("\nGiocatore 2:")
        carta_iniziale, player_2, return_valid = fai_la_mossa(player_2, carta_iniziale, carte_disponibili)
        if return_valid:
            print("Carta al centro => ", carta_iniziale, "\n")
            carte_usate.extend([carta_iniziale])


        print(f"Carte del mazzo rimanenti: {len(carte_disponibili)}")
        print(f"Carte usate: {len(carte_usate)}")
        print("\n")
            
        if len(carte_disponibili) < 4:
            print("SHUFFLE")
            carte_disponibili = random.shuffle(carte_usate)
            carte_usate = []


        if len(player_1) == 0:
            print("Player 1: !!!! UNO")
            break

        if len(player_2) == 0:
            print("Player 2: !!! UNO")
            break

start_game()