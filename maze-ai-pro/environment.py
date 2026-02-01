import random
import math
import time
from collections import deque
import json
import os


class SrodowiskoLabiryntu:
    def __init__(self, plansza):
        self.labirynt = plansza
        self.wiersze = len(self.labirynt)
        self.kolumny = len(self.labirynt[0])
        self.pozycja_start = self.znajdz_start()
        self.pozycja_agenta = self.pozycja_start[:]
        self.akcje = ['gora', 'dol', 'lewo', 'prawo']
        self.przestrzen_akcji = len(self.akcje)
        self.odleglosc_start_cel = self.oblicz_odleglosc_euklidesowa(self.pozycja_start, self.znajdz_cel())

    def znajdz_start(self):
        for r in range(self.wiersze):
            for c in range(self.kolumny):
                if self.labirynt[r][c] == 0:
                    return [r, c]
        return [1, 1]

    def znajdz_cel(self):
        for r in range(self.wiersze):
            for c in range(self.kolumny):
                if self.labirynt[r][c] == 9:
                    return [r, c]
        return [self.wiersze - 2, self.kolumny - 2]

    def oblicz_odleglosc_euklidesowa(self, p1, p2):
        return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

    def reset(self):
        self.pozycja_agenta = self.pozycja_start[:]
        return self.pobierz_obserwacje()

    def pobierz_obserwacje(self):
        r, c = self.pozycja_agenta
        obserwacja = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.wiersze and 0 <= nc < self.kolumny:
                obserwacja.append(self.labirynt[nr][nc])
            else:
                obserwacja.append(1)
        return tuple(obserwacja)

    def krok(self, indeks_akcji):
        akcja = self.akcje[indeks_akcji]
        poprzednia_pozycja = self.pozycja_agenta[:]
        poprzednia_odleglosc = self.oblicz_odleglosc_euklidesowa(self.pozycja_agenta, self.znajdz_cel())

        if akcja == 'gora':
            nr = self.pozycja_agenta[0] - 1
            nc = self.pozycja_agenta[1]
        elif akcja == 'dol':
            nr = self.pozycja_agenta[0] + 1
            nc = self.pozycja_agenta[1]
        elif akcja == 'lewo':
            nr = self.pozycja_agenta[0]
            nc = self.pozycja_agenta[1] - 1
        elif akcja == 'prawo':
            nr = self.pozycja_agenta[0]
            nc = self.pozycja_agenta[1] + 1

        if 0 <= nr < self.wiersze and 0 <= nc < self.kolumny:
            if self.labirynt[nr][nc] != 1:
                self.pozycja_agenta = [nr, nc]

        nowa_odleglosc = self.oblicz_odleglosc_euklidesowa(self.pozycja_agenta, self.znajdz_cel())
        nagroda = 0
        zakonczono = False

        if self.labirynt[self.pozycja_agenta[0]][self.pozycja_agenta[1]] == 9:
            nagroda = 100
            zakonczono = True
        elif self.pozycja_agenta == poprzednia_pozycja:
            nagroda = -10
        else:
            if nowa_odleglosc < poprzednia_odleglosc:
                nagroda = 2
            else:
                nagroda = -1

        nastepna_obserwacja = self.pobierz_obserwacje()
        return nastepna_obserwacja, nagroda, zakonczono, self.pozycja_agenta[:]


class AgentQUCZENIE:
    def __init__(self, przestrzen_akcji, wsp_uczenia=0.1, wsp_dyskont=0.95, epsilon=1.0, zanik_epsilon=0.995,
                 min_epsilon=0.01):
        self.przestrzen_akcji = przestrzen_akcji
        self.wsp_uczenia = wsp_uczenia
        self.wsp_dyskont = wsp_dyskont
        self.epsilon = epsilon
        self.zanik_epsilon = zanik_epsilon
        self.min_epsilon = min_epsilon
        self.tablica_q = {}
        self.historia_uczenia = []
        self.wskazowki = {}

    def dodaj_wskazowke(self, obserwacja, preferowana_akcja, sila=1.0):
        if obserwacja not in self.wskazowki:
            self.wskazowki[obserwacja] = {}
        if preferowana_akcja not in self.wskazowki[obserwacja]:
            self.wskazowki[obserwacja][preferowana_akcja] = 0
        self.wskazowki[obserwacja][preferowana_akcja] += sila

    def wybierz_akcje(self, obserwacja):
        if random.random() <= self.epsilon:
            return random.randrange(self.przestrzen_akcji)
        else:
            if obserwacja not in self.tablica_q:
                self.tablica_q[obserwacja] = [0.0] * self.przestrzen_akcji

            wartosci = self.tablica_q[obserwacja][:]

            if obserwacja in self.wskazowki:
                for akcja, sila in self.wskazowki[obserwacja].items():
                    if 0 <= akcja < len(wartosci):
                        wartosci[akcja] += sila * 10.0

            max_wartosc = max(wartosci)
            najlepsze_akcje = [i for i, v in enumerate(wartosci) if v == max_wartosc]
            return random.choice(najlepsze_akcje)

    def najlepsza_akcja(self, obserwacja):
        if obserwacja not in self.tablica_q:
            return random.randrange(self.przestrzen_akcji)
        wartosci = self.tablica_q[obserwacja]
        max_wartosc = max(wartosci)
        najlepsze_akcje = [i for i, v in enumerate(wartosci) if v == max_wartosc]
        return random.choice(najlepsze_akcje)

    def ucz_sie(self, obserwacja, akcja, nagroda, nastepna_obserwacja, zakonczono):
        if obserwacja not in self.tablica_q:
            self.tablica_q[obserwacja] = [0.0] * self.przestrzen_akcji
        if nastepna_obserwacja not in self.tablica_q:
            self.tablica_q[nastepna_obserwacja] = [0.0] * self.przestrzen_akcji

        predykcja = self.tablica_q[obserwacja][akcja]
        if not zakonczono:
            nastepny_max = max(self.tablica_q[nastepna_obserwacja])
            cel = nagroda + self.wsp_dyskont * nastepny_max
        else:
            cel = nagroda
        self.tablica_q[obserwacja][akcja] += self.wsp_uczenia * (cel - predykcja)

        if self.epsilon > self.min_epsilon:
            self.epsilon *= self.zanik_epsilon


class TrackerWydajnosci:
    def __init__(self):
        self.dane_wydajnosci = {}
        self.wczytaj_dane_wydajnosci()

    def wczytaj_dane_wydajnosci(self):
        try:
            if os.path.exists('wydajnosc.json'):
                with open('wydajnosc.json', 'r') as f:
                    self.dane_wydajnosci = json.load(f)
        except:
            self.dane_wydajnosci = {}

    def zapisz_dane_wydajnosci(self):
        try:
            with open('wydajnosc.json', 'w') as f:
                json.dump(self.dane_wydajnosci, f, indent=2)
        except:
            pass

    def zaktualizuj_wydajnosc(self, nazwa_modelu, nazwa_labiryntu, czas, epizody, sukces):
        if nazwa_modelu not in self.dane_wydajnosci:
            self.dane_wydajnosci[nazwa_modelu] = {
                'labirynt': nazwa_labiryntu,
                'czas': czas,
                'epizody': epizody,
                'sukces': sukces,
                'timestamp': time.time()  # Teraz time jest zdefiniowane
            }
        else:
            self.dane_wydajnosci[nazwa_modelu].update({
                'labirynt': nazwa_labiryntu,
                'czas': czas,
                'epizody': epizody,
                'sukces': sukces,
                'timestamp': time.time()
            })

        self.zapisz_dane_wydajnosci()

    def pobierz_ranking(self):
        ranking = []
        for nazwa_modelu, dane in self.dane_wydajnosci.items():
            ranking.append({
                'model': nazwa_modelu,
                'labirynt': dane['labirynt'],
                'czas': dane['czas'],
                'epizody': dane['epizody'],
                'sukces': dane['sukces']
            })

        ranking.sort(key=lambda x: (-x['sukces'], x['czas']))
        return ranking