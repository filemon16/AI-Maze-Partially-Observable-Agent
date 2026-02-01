import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import time
import threading
import os

try:
    import matplotlib

    matplotlib.use('TkAgg')
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from matplotlib.figure import Figure

    MATPLOTLIB_AVAILABLE = True
except:
    MATPLOTLIB_AVAILABLE = False


class OknoPostepuUczenia:
    def __init__(self, rodzic, aplikacja):
        self.okno = tk.Toplevel(rodzic)
        self.okno.title("Postęp Uczenia")
        self.okno.geometry("900x700")
        self.okno.configure(bg="#2c3e50")
        self.aplikacja = aplikacja

        self.podglad_canvas = tk.Canvas(self.okno, width=220, height=220, bg="#34495e", relief="solid", bd=2)
        self.podglad_canvas.pack(pady=10)

        if MATPLOTLIB_AVAILABLE:
            self.fig = Figure(figsize=(8, 4), dpi=100)
            self.ax1 = self.fig.add_subplot(121)
            self.ax2 = self.fig.add_subplot(122)
            self.canvas_wykres = FigureCanvasTkAgg(self.fig, master=self.okno)
            self.canvas_wykres.get_tk_widget().pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
            self.aktualizuj_wykresy()
        else:
            etykieta_brak_matplotlib = tk.Label(self.okno, text="Wykresy niedostępne - zainstaluj matplotlib",
                                                bg="#2c3e50", fg="#e74c3c", font=("Segoe UI", 10))
            etykieta_brak_matplotlib.pack(pady=5)

        self.tekst_statystyk = tk.Text(self.okno, height=8, width=90, bg="#34495e", fg="#ecf0f1", font=("Consolas", 9))
        self.tekst_statystyk.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

        przycisk_zamknij = ttk.Button(self.okno, text="Zamknij", command=self.okno.destroy)
        przycisk_zamknij.pack(pady=10)

        self.narysuj_widok_agenta([1, 1, 1, 1])
        self.okno.after(1000, self.aktualizuj_cyklicznie)

    def narysuj_widok_agenta(self, obserwacja):
        self.podglad_canvas.delete("all")
        rozmiar_komorki = 55

        kierunki = [
            ("Góra", 1, 0, obserwacja[0]),
            ("Dół", 1, 2, obserwacja[1]),
            ("Lewo", 0, 1, obserwacja[2]),
            ("Prawo", 2, 1, obserwacja[3])
        ]

        for etykieta, kolumna, wiersz, wartosc in kierunki:
            x1 = kolumna * rozmiar_komorki
            y1 = wiersz * rozmiar_komorki
            x2 = x1 + rozmiar_komorki
            y2 = y1 + rozmiar_komorki

            if wartosc == 1:
                kolor = "#34495e"
            elif wartosc == 9:
                kolor = "#2ecc71"
            else:
                kolor = "#3498db"

            self.podglad_canvas.create_rectangle(x1, y1, x2, y2, fill=kolor, outline="#2c3e50", width=2)
            self.podglad_canvas.create_text(x1 + rozmiar_komorki // 2, y1 + rozmiar_komorki // 2, text=etykieta,
                                            fill="#ecf0f1", font=("Arial", 9, "bold"))

    def aktualizuj_statystyki(self, epizod, sukces, srednie_kroki, czas, wszystkie_epizody):
        self.tekst_statystyk.config(state=tk.NORMAL)
        self.tekst_statystyk.delete(1.0, tk.END)
        self.tekst_statystyk.insert(tk.END, f"📊 SZCZEGÓŁOWY POSTĘP UCZENIA:\n")
        self.tekst_statystyk.insert(tk.END, f"{'=' * 50}\n")
        self.tekst_statystyk.insert(tk.END, f"Epizod: {epizod:,} / {wszystkie_epizody:,}\n")
        self.tekst_statystyk.insert(tk.END, f"Wskaźnik Sukcesu: {sukces:.2f}%\n")
        self.tekst_statystyk.insert(tk.END, f"Średnia Liczba Kroków: {srednie_kroki:.1f}\n")
        self.tekst_statystyk.insert(tk.END, f"Czas Sesji: {czas:.2f} sekund\n")
        self.tekst_statystyk.insert(tk.END, f"Epsilon (Eksploracja): {self.aplikacja.agent.epsilon:.4f}\n")
        self.tekst_statystyk.insert(tk.END, f"Liczba Stanów w Q-Table: {len(self.aplikacja.agent.tablica_q):,}\n")
        self.tekst_statystyk.insert(tk.END, f"\n🧠 STRATEGIA AGENTA:\n")
        self.tekst_statystyk.insert(tk.END, f"- Agent widzi TYLKO 4 sąsiednie komórki\n")
        self.tekst_statystyk.insert(tk.END, f"- Nauczył się rozpoznawać wzorce prowadzące do celu\n")
        self.tekst_statystyk.insert(tk.END, f"- Używa nagród za zbliżanie się do celu\n")
        self.tekst_statystyk.config(state=tk.DISABLED)

        if MATPLOTLIB_AVAILABLE:
            self.aktualizuj_wykresy()

    def aktualizuj_wykresy(self):
        if not hasattr(self.aplikacja.agent, 'historia_uczenia') or len(self.aplikacja.agent.historia_uczenia) == 0:
            return

        historia = self.aplikacja.agent.historia_uczenia[-200:]
        epizody = [h[0] for h in historia]
        sukcesy = [h[1] for h in historia]
        kroki = [h[2] for h in historia]

        self.ax1.clear()
        self.ax1.plot(epizody, sukcesy, color='#3498db', linewidth=2, marker='o', markersize=3)
        self.ax1.set_title('Wskaźnik Sukcesu', fontsize=12, color='#ecf0f1')
        self.ax1.set_xlabel('Epizod', fontsize=10, color='#bdc3c7')
        self.ax1.set_ylabel('Sukces (%)', fontsize=10, color='#bdc3c7')
        self.ax1.grid(True, alpha=0.3, color='#34495e')
        self.ax1.set_facecolor('#2c3e50')
        self.ax1.tick_params(colors='#bdc3c7')

        self.ax2.clear()
        self.ax2.plot(epizody, kroki, color='#e74c3c', linewidth=2, marker='s', markersize=3)
        self.ax2.set_title('Średnia Liczba Kroków', fontsize=12, color='#ecf0f1')
        self.ax2.set_xlabel('Epizod', fontsize=10, color='#bdc3c7')
        self.ax2.set_ylabel('Kroki', fontsize=10, color='#bdc3c7')
        self.ax2.grid(True, alpha=0.3, color='#34495e')
        self.ax2.set_facecolor('#2c3e50')
        self.ax2.tick_params(colors='#bdc3c7')

        self.fig.tight_layout()
        self.canvas_wykres.draw()

    def aktualizuj_cyklicznie(self):
        if self.okno.winfo_exists():
            if hasattr(self.aplikacja, 'statystyki_trenowania'):
                stats = self.aplikacja.statystyki_trenowania
                if 'epizody' in stats:
                    self.aktualizuj_statystyki(
                        stats['epizody'],
                        stats.get('sukces', 0),
                        stats.get('srednie_kroki', 0),
                        stats.get('czas', 0),
                        int(self.aplikacja.pole_epizodow.get()) if hasattr(self.aplikacja, 'pole_epizodow') else 1000
                    )
            self.okno.after(2000, self.aktualizuj_cyklicznie)


class OknoRecznegoTrenowania:
    def __init__(self, rodzic, aplikacja):
        self.okno = tk.Toplevel(rodzic)
        self.okno.title("Ręczne Trenowanie Agent")
        self.okno.geometry("800x700")
        self.okno.configure(bg="#2c3e50")
        self.aplikacja = aplikacja
        self.tryb_nagrody = "pozytywna"
        self.aktywna_nagroda = 5

        tytul = tk.Label(self.okno, text="Ręczne Trenowanie - Steruj Agentem i Nadawaj Nagrody!", bg="#2c3e50",
                         fg="#3498db", font=("Segoe UI", 16, "bold"))
        tytul.pack(pady=10)

        instrukcje = tk.Label(self.okno,
                              text="Sterowanie: Strzałki ← ↑ → ↓ | Nagroda: + (pozytywna) / - (negatywna) | Reset: R",
                              bg="#2c3e50", fg="#f39c12", font=("Segoe UI", 10))
        instrukcje.pack(pady=5)

        ramka_kontrolna = ttk.Frame(self.okno)
        ramka_kontrolna.pack(pady=10)

        self.przycisk_pozytywna = ttk.Button(ramka_kontrolna, text="Nagroda +5",
                                             command=lambda: self.ustaw_tryb_nagrody("pozytywna", 5))
        self.przycisk_pozytywna.pack(side=tk.LEFT, padx=5)

        self.przycisk_negatywna = ttk.Button(ramka_kontrolna, text="Kara -10",
                                             command=lambda: self.ustaw_tryb_nagrody("negatywna", -10))
        self.przycisk_negatywna.pack(side=tk.LEFT, padx=5)

        self.przycisk_wskazowka = ttk.Button(ramka_kontrolna, text="Dodaj Wskazówkę", command=self.dodaj_wskazowke)
        self.przycisk_wskazowka.pack(side=tk.LEFT, padx=5)

        self.etykieta_statusu = tk.Label(self.okno, text="Gotowy do trenowania ręcznego", bg="#2c3e50", fg="#2ecc71",
                                         font=("Segoe UI", 11))
        self.etykieta_statusu.pack(pady=5)

        self.canvas = tk.Canvas(self.okno, width=600, height=450, bg="#34495e", relief="solid", bd=2)
        self.canvas.pack(pady=10)

        self.podglad_wskazowek = tk.Text(self.okno, height=6, width=80, bg="#34495e", fg="#ecf0f1",
                                         font=("Consolas", 9))
        self.podglad_wskazowek.pack(pady=10, padx=20)
        self.podglad_wskazowek.insert(tk.END, "Wskazówki dla agenta:\n- Brak aktywnych wskazówek\n")
        self.podglad_wskazowek.config(state=tk.DISABLED)

        self.okno.bind('<Left>', lambda e: self.ruch_reczny('lewo'))
        self.okno.bind('<Right>', lambda e: self.ruch_reczny('prawo'))
        self.okno.bind('<Up>', lambda e: self.ruch_reczny('gora'))
        self.okno.bind('<Down>', lambda e: self.ruch_reczny('dol'))
        self.okno.bind('<plus>', lambda e: self.zastosuj_nagrode(5))
        self.okno.bind('<minus>', lambda e: self.zastosuj_nagrode(-10))
        self.okno.bind('r', lambda e: self.resetuj_pozycje())
        self.okno.bind('R', lambda e: self.resetuj_pozycje())

        self.renderuj_labirynt_reczny()
        self.okno.focus_set()

    def ustaw_tryb_nagrody(self, tryb, wartosc):
        self.tryb_nagrody = tryb
        self.aktywna_nagroda = wartosc
        if tryb == "pozytywna":
            self.etykieta_statusu.config(text=f"Aktywna nagroda: +{wartosc}", fg="#2ecc71")
        else:
            self.etykieta_statusu.config(text=f"Aktywna kara: {wartosc}", fg="#e74c3c")

    def ruch_reczny(self, kierunek):
        if not hasattr(self.aplikacja, 'srodowisko') or not hasattr(self.aplikacja, 'agent'):
            return

        akcje_map = {'gora': 0, 'dol': 1, 'lewo': 2, 'prawo': 3}
        if kierunek not in akcje_map:
            return

        obserwacja = self.aplikacja.srodowisko.pobierz_obserwacje()
        akcja = akcje_map[kierunek]
        nastepna_obserwacja, nagroda, zakonczono, nowa_pozycja = self.aplikacja.srodowisko.krok(akcja)

        self.aplikacja.agent.ucz_sie(obserwacja, akcja, nagroda, nastepna_obserwacja, zakonczono)

        self.renderuj_labirynt_reczny()

        status = f"Ruch: {kierunek} | Nagroda: {nagroda} | Pozycja: {nowa_pozycja}"
        if zakonczono:
            status += " 🎯 CEL OSIĄGNIĘTY!"
            self.etykieta_statusu.config(text=status, fg="#2ecc71")
            self.aplikacja.srodowisko.reset()
            self.okno.after(1500, self.renderuj_labirynt_reczny)
        else:
            self.etykieta_statusu.config(text=status, fg="#3498db")

    def zastosuj_nagrode(self, wartosc):
        if not hasattr(self.aplikacja, 'srodowisko') or not hasattr(self.aplikacja, 'agent'):
            return

        obserwacja = self.aplikacja.srodowisko.pobierz_obserwacje()
        akcja = self.aplikacja.agent.najlepsza_akcja(obserwacja)
        nastepna_obserwacja = self.aplikacja.srodowisko.pobierz_obserwacje()

        if obserwacja not in self.aplikacja.agent.tablica_q:
            self.aplikacja.agent.tablica_q[obserwacja] = [0.0] * self.aplikacja.srodowisko.przestrzen_akcji

        self.aplikacja.agent.tablica_q[obserwacja][akcja] += wartosc * 0.5

        typ = "NAGRODA" if wartosc > 0 else "KARA"
        kolor = "#2ecc71" if wartosc > 0 else "#e74c3c"
        self.etykieta_statusu.config(text=f"{typ}: {wartosc} zastosowana dla bieżącego stanu!", fg=kolor)

    def dodaj_wskazowke(self):
        if not hasattr(self.aplikacja, 'srodowisko') or not hasattr(self.aplikacja, 'agent'):
            return

        obserwacja = self.aplikacja.srodowisko.pobierz_obserwacje()
        kierunki = ['góra', 'dół', 'lewo', 'prawo']

        okno_wskazowki = tk.Toplevel(self.okno)
        okno_wskazowki.title("Dodaj Wskazówkę")
        okno_wskazowki.geometry("300x200")
        okno_wskazowki.configure(bg="#2c3e50")

        ttk.Label(okno_wskazowki, text="Wybierz preferowany kierunek:", background="#2c3e50",
                  foreground="#ecf0f1").pack(pady=10)

        zmienna_kierunku = tk.StringVar(value=kierunki[0])
        menu_kierunkow = ttk.Combobox(okno_wskazowki, textvariable=zmienna_kierunku, values=kierunki, state="readonly")
        menu_kierunkow.pack(pady=5)

        ttk.Label(okno_wskazowki, text="Siła wskazówki (1-10):", background="#2c3e50", foreground="#ecf0f1").pack(
            pady=5)
        suwak_sily = ttk.Scale(okno_wskazowki, from_=1, to=10, orient=tk.HORIZONTAL)
        suwak_sily.set(5)
        suwak_sily.pack(pady=5)

        def zapisz_wskazowke():
            kierunek_idx = kierunki.index(zmienna_kierunku.get())
            sila = suwak_sily.get()
            self.aplikacja.agent.dodaj_wskazowke(obserwacja, kierunek_idx, sila)
            self.aktualizuj_podglad_wskazowek()
            okno_wskazowki.destroy()
            self.etykieta_statusu.config(text=f"Wskazówka dodana: {zmienna_kierunku.get()} (siła: {sila:.1f})",
                                         fg="#9b59b6")

        ttk.Button(okno_wskazowki, text="Zapisz Wskazówkę", command=zapisz_wskazowke).pack(pady=10)

    def aktualizuj_podglad_wskazowek(self):
        self.podglad_wskazowek.config(state=tk.NORMAL)
        self.podglad_wskazowek.delete(1.0, tk.END)

        if not self.aplikacja.agent.wskazowki:
            self.podglad_wskazowek.insert(tk.END, "Wskazówki dla agenta:\n- Brak aktywnych wskazówek\n")
        else:
            self.podglad_wskazowek.insert(tk.END, "Aktywne wskazówki:\n")
            for obs, wskazowki in self.aplikacja.agent.wskazowki.items():
                self.podglad_wskazowek.insert(tk.END, f"Stan {obs}:\n")
                for akcja, sila in wskazowki.items():
                    kierunek = ['góra', 'dół', 'lewo', 'prawo'][akcja]
                    self.podglad_wskazowek.insert(tk.END, f"  → {kierunek}: siła {sila:.1f}\n")

        self.podglad_wskazowek.config(state=tk.DISABLED)

    def resetuj_pozycje(self):
        if hasattr(self.aplikacja, 'srodowisko'):
            self.aplikacja.srodowisko.reset()
            self.renderuj_labirynt_reczny()
            self.etykieta_statusu.config(text="Pozycja zresetowana do startu", fg="#3498db")

    def renderuj_labirynt_reczny(self):
        if not hasattr(self.aplikacja, 'srodowisko'):
            return

        self.canvas.delete("all")
        wiersze = self.aplikacja.srodowisko.wiersze
        kolumny = self.aplikacja.srodowisko.kolumny
        max_w = 600
        max_h = 450

        rozmiar_x = max(10, min(40, max_w // kolumny))
        rozmiar_y = max(10, min(40, max_h // wiersze))
        rozmiar = min(rozmiar_x, rozmiar_y)

        for r in range(wiersze):
            for c in range(kolumny):
                x1 = c * rozmiar
                y1 = r * rozmiar
                x2 = x1 + rozmiar
                y2 = y1 + rozmiar
                if self.aplikacja.srodowisko.labirynt[r][c] == 1:
                    kolor = "#34495e"
                elif self.aplikacja.srodowisko.labirynt[r][c] == 9:
                    kolor = "#2ecc71"
                else:
                    kolor = "#3498db"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=kolor, outline="#2c3e50", width=1)

        r, c = self.aplikacja.srodowisko.pozycja_agenta
        x1 = c * rozmiar + 3
        y1 = r * rozmiar + 3
        x2 = x1 + rozmiar - 6
        y2 = y1 + rozmiar - 6
        self.canvas.create_oval(x1, y1, x2, y2, fill="#e74c3c", outline="#c0392b", width=2)

        obserwacja = self.aplikacja.srodowisko.pobierz_obserwacje()
        self.canvas.create_text(10, 10, text=f"Widok agenta: {obserwacja}",
                                anchor="nw", fill="#ecf0f1", font=("Consolas", 8))