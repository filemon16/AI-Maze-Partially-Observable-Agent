import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import random
import pickle
import time  # DODANO: niezbędny import
import threading
import os
import sys

from maze_generator import GeneratorLabiryntu
from environment import SrodowiskoLabiryntu, AgentQUCZENIE, TrackerWydajnosci
from ui_components import OknoPostepuUczenia, OknoRecznegoTrenowania


class AplikacjaLabiryntu:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Rozwiązujący Labirynty Pro - Agent z Częściową Obserwowalnością")
        self.root.geometry("1300x950")
        self.root.configure(bg="#2c3e50")
        self.root.protocol("WM_DELETE_WINDOW", self.zamknij_aplikacje)

        self.tracker_wydajnosci = TrackerWydajnosci()
        self.okno_postepu = None
        self.okno_recznego_trenowania = None

        self.labirynty = {
            "Prosty": [
                [1, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 0, 1],
                [1, 1, 1, 1, 0, 1],
                [1, 0, 0, 0, 0, 1],
                [1, 0, 1, 1, 1, 1],
                [1, 0, 0, 0, 9, 1],
                [1, 1, 1, 1, 1, 1]
            ],
            "Średni": [
                [1, 1, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 0, 0, 1],
                [1, 0, 1, 1, 1, 0, 1],
                [1, 0, 0, 0, 1, 0, 1],
                [1, 1, 1, 0, 1, 0, 1],
                [1, 0, 0, 0, 0, 0, 1],
                [1, 1, 1, 1, 1, 9, 1]
            ],
            "Trudny": [
                [1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 1, 0, 0, 0, 1],
                [1, 0, 1, 0, 1, 0, 1, 0, 1],
                [1, 0, 1, 0, 0, 0, 1, 0, 1],
                [1, 0, 1, 1, 1, 1, 1, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 1, 1, 1, 1, 1, 1, 9, 1]
            ],
            "Ekspert": [
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
                [1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1],
                [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1],
                [1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1],
                [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
                [1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 9, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
            ],
            "Duży": [
                [1] * 15,
                [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1],
                [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
                [1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
                [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1],
                [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1],
                [1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1],
                [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9, 1],
                [1] * 15
            ],
            "Bardzo Duży": [
                [1] * 25,
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
                [1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1],
                [1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1],
                [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1],
                [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
                [1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
                [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
                [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
                [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
                [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
                [1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
                [1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
                [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
                [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1],
                [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 9, 1],
                [1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1],
                [1] * 25
            ]
        }

        self.obecna_nazwa_labiryntu = "Prosty"
        self.srodowisko = SrodowiskoLabiryntu(self.labirynty[self.obecna_nazwa_labiryntu])
        self.agent = AgentQUCZENIE(self.srodowisko.przestrzen_akcji)
        self.watek_trenowania = None
        self.anuluj_trenowanie = False
        self.statystyki_trenowania = {"epizody": 0, "sukces": 0, "srednie_kroki": 0, "czas": 0}

        self.zainicjuj_interfejs()

    def zamknij_aplikacje(self):
        if self.watek_trenowania and self.watek_trenowania.is_alive():
            self.anuluj_trenowanie = True
            self.watek_trenowania.join(timeout=1.0)
        self.root.destroy()

    def zainicjuj_interfejs(self):
        styl = ttk.Style()
        styl.theme_use("clam")
        styl.configure("TFrame", background="#2c3e50")
        styl.configure("TLabel", background="#2c3e50", foreground="#ecf0f1", font=("Segoe UI", 10))
        styl.configure("TButton", background="#3498db", foreground="#ecf0f1", font=("Segoe UI", 10, "bold"), padding=6)
        styl.map("TButton", background=[("active", "#2980b9")])
        styl.configure("Accent.TButton", background="#2ecc71", foreground="#ecf0f1")
        styl.map("Accent.TButton", background=[("active", "#27ae60")])
        styl.configure("Danger.TButton", background="#e74c3c", foreground="#ecf0f1")
        styl.map("Danger.TButton", background=[("active", "#c0392b")])
        styl.configure("TEntry", fieldbackground="#34495e", foreground="#ecf0f1", insertcolor="#ecf0f1")
        styl.configure("TCombobox", fieldbackground="#34495e", foreground="#ecf0f1")
        styl.map("TCombobox", fieldbackground=[("readonly", "#34495e")])
        styl.configure("TNotebook", background="#2c3e50")
        styl.configure("TNotebook.Tab", background="#34495e", foreground="#ecf0f1")
        styl.map("TNotebook.Tab", background=[("selected", "#3498db")], foreground=[("selected", "#ffffff")])

        glowna_ramka = ttk.Frame(self.root)
        glowna_ramka.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        tytul_ramka = ttk.Frame(glowna_ramka)
        tytul_ramka.pack(fill=tk.X, pady=(0, 15))

        etykieta_tytul = tk.Label(tytul_ramka, text="🧠 AI ROZWIĄZUJĄCY LABIRYNTY PRO", bg="#2c3e50", fg="#3498db",
                                  font=("Segoe UI", 22, "bold"))
        etykieta_tytul.pack(side=tk.LEFT)

        etykieta_opis = tk.Label(tytul_ramka,
                                 text="Agent widzi TYLKO 4 sąsiednie komórki - musi nauczyć się strategii bez pełnej wizji!",
                                 bg="#2c3e50", fg="#f39c12", font=("Segoe UI", 11, "italic"))
        etykieta_opis.pack(side=tk.LEFT, padx=20)

        notebook = ttk.Notebook(glowna_ramka)
        notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

        ramka_labiryntu = ttk.Frame(notebook)
        ramka_parametrow = ttk.Frame(notebook)
        ramka_modelu = ttk.Frame(notebook)

        notebook.add(ramka_labiryntu, text=" 🗺️ Labirynt ")
        notebook.add(ramka_parametrow, text=" ⚙️ Parametry ")
        notebook.add(ramka_modelu, text=" 🤖 Model ")

        self.zainicjuj_ramke_labiryntu(ramka_labiryntu)
        self.zainicjuj_ramke_parametrow(ramka_parametrow)
        self.zainicjuj_ramke_modelu(ramka_modelu)

        ramka_statystyk = ttk.Frame(glowna_ramka)
        ramka_statystyk.pack(fill=tk.X)

        self.etykieta_statusu = tk.Label(ramka_statystyk,
                                         text="Gotowy do pracy - Agent ma ograniczoną percepcję świata!",
                                         bg="#2c3e50", fg="#2ecc71", font=("Segoe UI", 12, "bold"))
        self.etykieta_statusu.pack(side=tk.LEFT, padx=10)

        self.tekst_statystyk = tk.Text(ramka_statystyk, height=5, width=75, bg="#34495e", fg="#ecf0f1",
                                       font=("Consolas", 10))
        self.tekst_statystyk.pack(side=tk.RIGHT, padx=(15, 0))
        self.tekst_statystyk.insert(tk.END,
                                    "📊 STATYSTYKI UCZENIA:\n- Epizody: 0\n- Sukces: 0.00%\n- Śr. Kroki: 0.0\n- Czas: 0.00s")
        self.tekst_statystyk.config(state=tk.DISABLED)

        self.renderuj_labirynt()

    def zainicjuj_ramke_labiryntu(self, ramka):
        ramka_gorna = ttk.Frame(ramka)
        ramka_gorna.pack(fill=tk.X, pady=(0, 15))

        lewa_kontrola = ttk.Frame(ramka_gorna)
        lewa_kontrola.pack(side=tk.LEFT)

        ttk.Label(lewa_kontrola, text="Wybierz Labirynt:").grid(row=0, column=0, padx=(0, 5), sticky="w")
        self.zmienna_labiryntu = tk.StringVar(value=self.obecna_nazwa_labiryntu)
        menu_labiryntow = ttk.Combobox(lewa_kontrola, textvariable=self.zmienna_labiryntu,
                                       values=list(self.labirynty.keys()), state="readonly", width=15)
        menu_labiryntow.grid(row=0, column=1, padx=(0, 15))
        menu_labiryntow.bind('<<ComboboxSelected>>', lambda e: self.zmien_labirynt())

        prawa_kontrola = ttk.Frame(ramka_gorna)
        prawa_kontrola.pack(side=tk.RIGHT)

        ttk.Label(prawa_kontrola, text="Własny Labirynt:").grid(row=0, column=0, padx=(0, 5), sticky="w")

        ttk.Label(prawa_kontrola, text="Szerokość:").grid(row=0, column=1, padx=(0, 5))
        self.pole_szerokosci = ttk.Entry(prawa_kontrola, width=6)
        self.pole_szerokosci.insert(0, "25")
        self.pole_szerokosci.grid(row=0, column=2, padx=(0, 5))

        ttk.Label(prawa_kontrola, text="Wysokość:").grid(row=0, column=3, padx=(0, 5))
        self.pole_wysokosci = ttk.Entry(prawa_kontrola, width=6)
        self.pole_wysokosci.insert(0, "25")
        self.pole_wysokosci.grid(row=0, column=4, padx=(0, 5))

        ttk.Label(prawa_kontrola, text="Trudność:").grid(row=0, column=5, padx=(0, 5))
        self.zmienna_trudnosci = tk.DoubleVar(value=0.35)
        suwak_trudnosci = ttk.Scale(prawa_kontrola, from_=0.1, to=0.6, variable=self.zmienna_trudnosci, length=100)
        suwak_trudnosci.grid(row=0, column=6, padx=(0, 5))

        self.przycisk_generuj = ttk.Button(prawa_kontrola, text="🚀 Wygeneruj", command=self.wygeneruj_wlasny_labirynt)
        self.przycisk_generuj.grid(row=0, column=7, padx=(0, 15))

        ramka_canvas = ttk.Frame(ramka)
        ramka_canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(ramka_canvas, bg="#34495e", relief="solid", bd=2)
        pasek_pionowy = ttk.Scrollbar(ramka_canvas, orient="vertical", command=self.canvas.yview)
        pasek_poziomy = ttk.Scrollbar(ramka_canvas, orient="horizontal", command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=pasek_pionowy.set, xscrollcommand=pasek_poziomy.set)

        self.canvas.grid(row=0, column=0, sticky="nsew")
        pasek_pionowy.grid(row=0, column=1, sticky="ns")
        pasek_poziomy.grid(row=1, column=0, sticky="ew")

        ramka_canvas.grid_rowconfigure(0, weight=1)
        ramka_canvas.grid_columnconfigure(0, weight=1)

    def zainicjuj_ramke_parametrow(self, ramka):
        instrukcja = tk.Label(ramka,
                              text="Dostosuj parametry uczenia - wyższe wartości przyspieszają naukę, ale mogą zmniejszyć stabilność",
                              bg="#2c3e50", fg="#f39c12", font=("Segoe UI", 10, "italic"), wraplength=800)
        instrukcja.pack(pady=(0, 15))

        parametry_grid = ttk.Frame(ramka)
        parametry_grid.pack(fill=tk.X, padx=20)

        # Tworzymy widgety przed przypisaniem do atrybutów
        self.pole_epizodow = ttk.Entry(parametry_grid, width=12)
        self.pole_wsp_uczenia = ttk.Entry(parametry_grid, width=12)
        self.pole_epsilon = ttk.Entry(parametry_grid, width=12)
        self.pole_dyskont = ttk.Entry(parametry_grid, width=12)
        self.pole_min_epsilon = ttk.Entry(parametry_grid, width=12)
        self.pole_zanik_epsilon = ttk.Entry(parametry_grid, width=12)

        parametry = [
            ("Epizody", "2000", self.pole_epizodow),
            ("Wsp. Uczenia (α)", "0.45", self.pole_wsp_uczenia),
            ("Eksploracja (ε)", "1.0", self.pole_epsilon),
            ("Wsp. Dyskont (γ)", "0.97", self.pole_dyskont),
            ("Min. Eksploracja", "0.05", self.pole_min_epsilon),
            ("Zanik Eksploracji", "0.9985", self.pole_zanik_epsilon)
        ]

        for i, (etykieta, domyslna, widget) in enumerate(parametry):
            ttk.Label(parametry_grid, text=etykieta + ":").grid(row=i // 2, column=(i % 2) * 2, padx=(0, 5), pady=5,
                                                                sticky="e")
            widget.insert(0, domyslna)
            widget.grid(row=i // 2, column=(i % 2) * 2 + 1, padx=(0, 15), pady=5, sticky="w")

        ramka_trybow = ttk.Frame(ramka)
        ramka_trybow.pack(fill=tk.X, pady=15)

        ttk.Label(ramka_trybow, text="Tryb Trenowania:").pack(side=tk.LEFT, padx=(0, 10))

        self.zmienna_trybu = tk.StringVar(value="Dokładny")
        for tryb in ["Szybki", "Standardowy", "Dokładny", "Eksploracyjny"]:
            rb = ttk.Radiobutton(ramka_trybow, text=tryb, variable=self.zmienna_trybu, value=tryb)
            rb.pack(side=tk.LEFT, padx=10)

        ttk.Label(ramka_trybow, text="  |  Maks. Kroki:").pack(side=tk.LEFT, padx=(20, 5))
        self.pole_maks_krokow = ttk.Entry(ramka_trybow, width=8)
        self.pole_maks_krokow.insert(0, "1000")
        self.pole_maks_krokow.pack(side=tk.LEFT)

    def zainicjuj_ramke_modelu(self, ramka):
        instrukcja = tk.Label(ramka, text="Zaawansowana kontrola modelu - dostosuj architekturę i zachowanie agenta",
                              bg="#2c3e50", fg="#9b59b6", font=("Segoe UI", 10, "italic"), wraplength=800)
        instrukcja.pack(pady=(0, 15))

        przyciski_model = ttk.Frame(ramka)
        przyciski_model.pack(fill=tk.X, pady=10)

        przyciski = [
            ("📈 Wykresy Uczenia", self.pokaz_wykresy_uczenia),
            ("🎮 Ręczne Trenowanie", self.otworz_reczne_trenowanie),
            ("💡 System Wskazówek", self.otworz_system_wskazowek),
            ("💾 Zapisz Model", self.zapisz_model),
            ("📂 Wczytaj Model", self.wczytaj_model),
            ("🔄 Reset Modelu", self.reset_modelu)
        ]

        for tekst, komenda in przyciski:
            btn = ttk.Button(przyciski_model, text=tekst, command=komenda)
            btn.pack(side=tk.LEFT, padx=5)

        info_model = tk.Label(ramka,
                              text="ℹ️ Model używa Q-Learning z częściową obserwowalnością. Agent uczy się na podstawie 4 wartości reprezentujących ściany/ścieżki wokół niego.",
                              bg="#2c3e50", fg="#bdc3c7", font=("Segoe UI", 9), wraplength=850, justify=tk.LEFT)
        info_model.pack(pady=(20, 0), padx=20)

        self.info_rozmiar_modelu = tk.Label(ramka, text="📊 Aktualny rozmiar modelu: 0 stanów", bg="#2c3e50",
                                            fg="#3498db", font=("Segoe UI", 10))
        self.info_rozmiar_modelu.pack(pady=5)

    def zmien_labirynt(self):
        self.obecna_nazwa_labiryntu = self.zmienna_labiryntu.get()
        self.srodowisko = SrodowiskoLabiryntu(self.labirynty[self.obecna_nazwa_labiryntu])
        self.renderuj_labirynt()
        self.etykieta_statusu.config(text=f"Labirynt zmieniony na: {self.obecna_nazwa_labiryntu}", fg="#3498db")

    def renderuj_labirynt(self):
        self.canvas.delete("all")

        wiersze = self.srodowisko.wiersze
        kolumny = self.srodowisko.kolumny
        max_szerokosc = 1000
        max_wysokosc = 550

        if wiersze > 40 or kolumny > 40:
            rozmiar_x = max(3, min(18, max_szerokosc // kolumny))
            rozmiar_y = max(3, min(18, max_wysokosc // wiersze))
        else:
            rozmiar_x = max(10, min(30, max_szerokosc // kolumny))
            rozmiar_y = max(10, min(30, max_wysokosc // wiersze))

        self.rozmiar_komorki = min(rozmiar_x, rozmiar_y)

        szerokosc_canvas = kolumny * self.rozmiar_komorki
        wysokosc_canvas = wiersze * self.rozmiar_komorki

        self.canvas.config(scrollregion=(0, 0, szerokosc_canvas, wysokosc_canvas))

        for r in range(wiersze):
            for c in range(kolumny):
                x1 = c * self.rozmiar_komorki
                y1 = r * self.rozmiar_komorki
                x2 = x1 + self.rozmiar_komorki
                y2 = y1 + self.rozmiar_komorki
                if self.srodowisko.labirynt[r][c] == 1:
                    kolor = "#34495e"
                elif self.srodowisko.labirynt[r][c] == 9:
                    kolor = "#27ae60"
                else:
                    kolor = "#3498db"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=kolor, outline="#2c3e50", width=1)

                if [r, c] == self.srodowisko.pozycja_start:
                    self.canvas.create_text(x1 + self.rozmiar_komorki / 2, y1 + self.rozmiar_komorki / 2,
                                            text="S", fill="#f1c40f",
                                            font=("Arial", max(8, int(self.rozmiar_komorki / 2)), "bold"))
                elif self.srodowisko.labirynt[r][c] == 9:
                    self.canvas.create_text(x1 + self.rozmiar_komorki / 2, y1 + self.rozmiar_komorki / 2,
                                            text="C", fill="#ecf0f1",
                                            font=("Arial", max(8, int(self.rozmiar_komorki / 2)), "bold"))

        self.pokaz_agenta()
        self.aktualizuj_info_modelu()

    def pokaz_agenta(self):
        r, c = self.srodowisko.pozycja_agenta
        x1 = c * self.rozmiar_komorki + 2
        y1 = r * self.rozmiar_komorki + 2
        x2 = x1 + self.rozmiar_komorki - 4
        y2 = y1 + self.rozmiar_komorki - 4
        self.canvas.delete("agent")
        self.canvas.create_oval(x1, y1, x2, y2, fill="#e74c3c", tags="agent", outline="#c0392b", width=2)

    def wygeneruj_wlasny_labirynt(self):
        try:
            szerokosc = int(self.pole_szerokosci.get())
            wysokosc = int(self.pole_wysokosci.get())
            trudnosc = self.zmienna_trudnosci.get()

            if szerokosc < 5 or szerokosc > 300 or wysokosc < 5 or wysokosc > 300:
                messagebox.showerror("Błąd", "Szerokość i wysokość muszą być między 5 a 300")
                return

            self.etykieta_statusu.config(text=f"Generowanie labiryntu {szerokosc}x{wysokosc}... Proszę czekać.",
                                         fg="#f39c12")
            self.root.update()

            labirynt = GeneratorLabiryntu.wygeneruj_labirynt(szerokosc, wysokosc, trudnosc)
            nazwa = f"Własny {szerokosc}x{wysokosc}"
            self.labirynty[nazwa] = labirynt
            self.zmienna_labiryntu.set(nazwa)
            self.obecna_nazwa_labiryntu = nazwa
            self.srodowisko = SrodowiskoLabiryntu(labirynt)
            self.renderuj_labirynt()
            self.etykieta_statusu.config(text=f"Własny labirynt {szerokosc}x{wysokosc} wygenerowany!", fg="#2ecc71")

        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się wygenerować labiryntu:\n{str(e)}")

    def trenuj_ai(self):
        if self.watek_trenowania and self.watek_trenowania.is_alive():
            self.anuluj_trenowanie = True
            self.przycisk_trenuj.config(text="Trenuj AI")
            self.etykieta_statusu.config(text="Trenowanie anulowane przez użytkownika", fg="#e74c3c")
            return

        nazwa_modelu = simpledialog.askstring("Nazwa Modelu", "Wprowadź unikalną nazwę dla modelu:", parent=self.root)
        if not nazwa_modelu:
            return

        self.nazwa_modelu = nazwa_modelu
        self.anuluj_trenowanie = False
        self.przycisk_trenuj.config(text="🛑 Anuluj Trenowanie")
        self.etykieta_statusu.config(text="🚀 Rozpoczęto intensywne trenowanie AI...", fg="#3498db")

        self.watek_trenowania = threading.Thread(target=self._proces_trenowania)
        self.watek_trenowania.daemon = True
        self.watek_trenowania.start()

    def _proces_trenowania(self):
        komunikat_bledu = None
        try:
            czas_start = time.time()  # time jest teraz zdefiniowane
            self.obecna_nazwa_labiryntu = self.zmienna_labiryntu.get()
            self.srodowisko = SrodowiskoLabiryntu(self.labirynty[self.obecna_nazwa_labiryntu])

            epizody = int(self.pole_epizodow.get())
            wsp_uczenia = float(self.pole_wsp_uczenia.get())
            epsilon = float(self.pole_epsilon.get())
            wsp_dyskont = float(self.pole_dyskont.get())
            min_epsilon = float(self.pole_min_epsilon.get())
            zanik_epsilon = float(self.pole_zanik_epsilon.get())
            tryb = self.zmienna_trybu.get()
            maks_krokow = int(self.pole_maks_krokow.get())

            if tryb == "Szybki":
                wsp_uczenia = min(wsp_uczenia * 1.4, 0.6)
                epsilon = max(epsilon * 0.7, 0.1)
                epizody = max(epizody // 2, 300)
                zanik_epsilon = max(zanik_epsilon * 0.98, 0.97)
            elif tryb == "Dokładny":
                wsp_uczenia = max(wsp_uczenia * 0.85, 0.2)
                epsilon = min(epsilon * 1.15, 1.0)
                epizody = int(epizody * 1.8)
                zanik_epsilon = min(zanik_epsilon * 1.002, 0.9995)
                min_epsilon = max(min_epsilon * 0.8, 0.01)
            elif tryb == "Eksploracyjny":
                epsilon = 1.0
                zanik_epsilon = 0.9998
                min_epsilon = 0.1
                wsp_uczenia = max(wsp_uczenia * 0.9, 0.25)

            if epizody <= 0 or wsp_uczenia <= 0 or epsilon < 0 or wsp_dyskont <= 0 or wsp_dyskont >= 1:
                raise ValueError("Nieprawidłowe parametry uczenia")

            self.agent = AgentQUCZENIE(
                self.srodowisko.przestrzen_akcji,
                wsp_uczenia=wsp_uczenia,
                wsp_dyskont=wsp_dyskont,
                epsilon=epsilon,
                zanik_epsilon=zanik_epsilon,
                min_epsilon=min_epsilon
            )

            liczba_sukcesow = 0
            laczna_liczba_krokow = 0
            historia_sukcesow = []
            interwal_aktualizacji = max(1, epizody // 150)

            for epizod in range(epizody):
                if self.anuluj_trenowanie:
                    break

                obserwacja = self.srodowisko.reset()
                kroki = 0
                rzeczywiste_maks_kroki = maks_krokow if maks_krokow > 0 else self.srodowisko.wiersze * self.srodowisko.kolumny * 5
                zakonczono = False

                while kroki < rzeczywiste_maks_kroki and not zakonczono:
                    akcja = self.agent.wybierz_akcje(obserwacja)
                    nastepna_obserwacja, nagroda, zakonczono, _ = self.srodowisko.krok(akcja)
                    self.agent.ucz_sie(obserwacja, akcja, nagroda, nastepna_obserwacja, zakonczono)
                    obserwacja = nastepna_obserwacja
                    kroki += 1

                    if zakonczono and nagroda > 0:
                        liczba_sukcesow += 1

                laczna_liczba_krokow += kroki
                historia_sukcesow.append(1 if zakonczono and nagroda > 0 else 0)
                if len(historia_sukcesow) > 50:
                    historia_sukcesow.pop(0)

                if epizod % interwal_aktualizacji == 0 or epizod == epizody - 1:
                    uplynelo = time.time() - czas_start  # time jest teraz zdefiniowane
                    wspolczynnik_sukcesu = (
                                sum(historia_sukcesow) / len(historia_sukcesow) * 100) if historia_sukcesow else 0
                    srednie_kroki = laczna_liczba_krokow / (epizod + 1)

                    self.statystyki_trenowania = {
                        "epizody": epizod + 1,
                        "sukces": wspolczynnik_sukcesu,
                        "srednie_kroki": srednie_kroki,
                        "czas": uplynelo,
                        "tryb": tryb
                    }

                    self.agent.historia_uczenia.append((epizod + 1, wspolczynnik_sukcesu, srednie_kroki))

                    self.root.after(0, self.aktualizuj_wyswietlane_statystyki)
                    self.root.after(0, self.aktualizuj_info_modelu)
                    self.root.after(0, self.root.update_idletasks)

            if not self.anuluj_trenowanie:
                czas_koncowy = time.time() - czas_start  # time jest teraz zdefiniowane
                koncowy_sukces = (liczba_sukcesow / epizody) * 100 if epizody > 0 else 0
                self.statystyki_trenowania["czas"] = czas_koncowy
                self.statystyki_trenowania["sukces"] = koncowy_sukces

                self.tracker_wydajnosci.zaktualizuj_wydajnosc(
                    self.nazwa_modelu,
                    self.obecna_nazwa_labiryntu,
                    czas_koncowy,
                    epizody,
                    koncowy_sukces
                )

                self.root.after(0, lambda: self.etykieta_statusu.config(
                    text=f"✅ Trenowanie zakończone! Sukces: {koncowy_sukces:.1f}%", fg="#2ecc71"))
                self.root.after(0, self.aktualizuj_wyswietlane_statystyki)
                self.root.after(0, lambda: messagebox.showinfo("Sukces",
                                                               f"Model '{self.nazwa_modelu}' zakończył trenowanie!\n"
                                                               f"Czas: {czas_koncowy:.2f}s | Sukces: {koncowy_sukces:.1f}%\n"
                                                               f"Epizody: {epizody:,} | Stanów: {len(self.agent.tablica_q):,}"))
            else:
                self.root.after(0, lambda: self.etykieta_statusu.config(text="⚠️ Trenowanie anulowane", fg="#e74c3c"))

        except Exception as e:
            komunikat_bledu = str(e)
            self.root.after(0, lambda: self.etykieta_statusu.config(text="❌ Błąd podczas trenowania", fg="#e74c3c"))
            self.root.after(0, lambda msg=komunikat_bledu: messagebox.showerror("Błąd",
                                                                                f"Trenowanie nie powiodło się:\n{msg}"))
        finally:
            self.root.after(0, lambda: self.przycisk_trenuj.config(text="🚀 Trenuj AI"))

    def aktualizuj_wyswietlane_statystyki(self):
        self.tekst_statystyk.config(state=tk.NORMAL)
        self.tekst_statystyk.delete(1.0, tk.END)
        self.tekst_statystyk.insert(tk.END, f"📊 STATYSTYKI UCZENIA:\n")
        self.tekst_statystyk.insert(tk.END, f"- Epizody: {self.statystyki_trenowania['epizody']:,}\n")
        self.tekst_statystyk.insert(tk.END, f"- Sukces: {self.statystyki_trenowania['sukces']:.2f}%\n")
        self.tekst_statystyk.insert(tk.END, f"- Śr. Kroki: {self.statystyki_trenowania['srednie_kroki']:.1f}\n")
        self.tekst_statystyk.insert(tk.END, f"- Czas: {self.statystyki_trenowania['czas']:.2f}s\n")
        self.tekst_statystyk.insert(tk.END, f"- Tryb: {self.statystyki_trenowania.get('tryb', 'Standardowy')}")
        self.tekst_statystyk.config(state=tk.DISABLED)

    def aktualizuj_info_modelu(self):
        if hasattr(self, 'agent') and hasattr(self.agent, 'tablica_q'):
            rozmiar = len(self.agent.tablica_q)
            self.info_rozmiar_modelu.config(
                text=f"📊 Aktualny rozmiar modelu: {rozmiar:,} stanów | Epsilon: {self.agent.epsilon:.4f}")

    def uruchom_najlepsza_sciezke(self):
        try:
            if not hasattr(self, 'agent') or not self.agent.tablica_q:
                messagebox.showwarning("Uwaga", "Najpierw wytrenuj model AI!")
                return

            self.etykieta_statusu.config(text="▶️ Uruchamianie najlepszej ścieżki...", fg="#3498db")
            self.root.update()

            self.obecna_nazwa_labiryntu = self.zmienna_labiryntu.get()
            self.srodowisko = SrodowiskoLabiryntu(self.labirynty[self.obecna_nazwa_labiryntu])
            obserwacja = self.srodowisko.reset()
            self.renderuj_labirynt()
            self.root.update()

            kroki = 0
            maks_krokow = min(self.srodowisko.wiersze * self.srodowisko.kolumny * 8, 50000)
            odwiedzone = set()
            stagnacja = 0
            max_stagnacja = 30

            while kroki < maks_krokow:
                akcja = self.agent.najlepsza_akcja(obserwacja)
                nastepna_obserwacja, nagroda, zakonczono, pozycja = self.srodowisko.krok(akcja)
                obserwacja = nastepna_obserwacja
                self.pokaz_agenta()
                self.root.update()

                if self.srodowisko.wiersze <= 40 and self.srodowisko.kolumny <= 40:
                    self.root.after(35)
                else:
                    self.root.after(8)

                if zakonczono:
                    self.etykieta_statusu.config(text=f"🎉 Sukces! Cel osiągnięty w {kroki + 1} krokach!", fg="#2ecc71")
                    return

                pozycja_klucz = (pozycja[0], pozycja[1])
                if pozycja_klucz in odwiedzone:
                    stagnacja += 1
                else:
                    stagnacja = 0
                    odwiedzone.add(pozycja_klucz)

                if stagnacja > max_stagnacja:
                    akcja = random.randrange(self.srodowisko.przestrzen_akcji)
                    nastepna_obserwacja, nagroda, zakonczono, pozycja = self.srodowisko.krok(akcja)
                    obserwacja = nastepna_obserwacja
                    self.pokaz_agenta()
                    self.root.update()
                    if self.srodowisko.wiersze <= 40 and self.srodowisko.kolumny <= 40:
                        self.root.after(35)
                    else:
                        self.root.after(8)
                    stagnacja = 0

                kroki += 1

            self.etykieta_statusu.config(text=f"⚠️ Limit kroków osiągnięty ({kroki}). Cel nie został znaleziony.",
                                         fg="#e74c3c")
        except Exception as e:
            self.etykieta_statusu.config(text="❌ Błąd podczas uruchamiania ścieżki", fg="#e74c3c")
            messagebox.showerror("Błąd", f"Uruchamianie ścieżki nie powiodło się:\n{str(e)}")

    def zapisz_model(self):
        try:
            sciezka_pliku = filedialog.asksaveasfilename(
                defaultextension=".pkl",
                filetypes=[("Pickle files", "*.pkl"), ("All files", "*.*")],
                initialfile=f"model_{self.nazwa_modelu if hasattr(self, 'nazwa_modelu') else 'ai'}"
            )
            if sciezka_pliku:
                with open(sciezka_pliku, 'wb') as f:
                    pickle.dump({
                        'tablica_q': self.agent.tablica_q,
                        'wskazowki': self.agent.wskazowki,
                        'labirynt': self.labirynty[self.obecna_nazwa_labiryntu],
                        'nazwa_labiryntu': self.obecna_nazwa_labiryntu,
                        'parametry': {
                            'wsp_uczenia': self.agent.wsp_uczenia,
                            'wsp_dyskont': self.agent.wsp_dyskont,
                            'epsilon': self.agent.epsilon,
                            'zanik_epsilon': self.agent.zanik_epsilon,
                            'min_epsilon': self.agent.min_epsilon
                        }
                    }, f)
                self.etykieta_statusu.config(text=f"✅ Model zapisany: {os.path.basename(sciezka_pliku)}", fg="#2ecc71")
                messagebox.showinfo("Sukces", "Model został pomyślnie zapisany!")
        except Exception as e:
            self.etykieta_statusu.config(text="❌ Nie udało się zapisać modelu", fg="#e74c3c")
            messagebox.showerror("Błąd", f"Zapis modelu nie powiódł się:\n{str(e)}")

    def wczytaj_model(self):
        try:
            sciezka_pliku = filedialog.askopenfilename(
                filetypes=[("Pickle files", "*.pkl"), ("All files", "*.*")]
            )
            if sciezka_pliku:
                self.etykieta_statusu.config(text="📥 Wczytywanie modelu... Proszę czekać.", fg="#f39c12")
                self.root.update()

                with open(sciezka_pliku, 'rb') as f:
                    dane = pickle.load(f)
                    self.agent.tablica_q = dane['tablica_q']
                    self.agent.wskazowki = dane.get('wskazowki', {})
                    wczytany_labirynt = dane['labirynt']
                    nazwa_labiryntu = dane.get('nazwa_labiryntu', 'Wczytany')
                    parametry = dane.get('parametry', {})

                    if parametry:
                        self.agent.wsp_uczenia = parametry.get('wsp_uczenia', 0.1)
                        self.agent.wsp_dyskont = parametry.get('wsp_dyskont', 0.95)
                        self.agent.epsilon = parametry.get('epsilon', 1.0)
                        self.agent.zanik_epsilon = parametry.get('zanik_epsilon', 0.995)
                        self.agent.min_epsilon = parametry.get('min_epsilon', 0.01)

                    self.labirynty[nazwa_labiryntu] = wczytany_labirynt
                    self.zmienna_labiryntu.set(nazwa_labiryntu)
                    self.obecna_nazwa_labiryntu = nazwa_labiryntu
                    self.srodowisko = SrodowiskoLabiryntu(wczytany_labirynt)
                    self.renderuj_labirynt()

                self.etykieta_statusu.config(text=f"✅ Model wczytany: {os.path.basename(sciezka_pliku)}", fg="#2ecc71")
                messagebox.showinfo("Sukces", f"Model wczytany pomyślnie!\nStanów: {len(self.agent.tablica_q):,}")
        except FileNotFoundError:
            self.etykieta_statusu.config(text="❌ Nie znaleziono pliku modelu", fg="#e74c3c")
            messagebox.showwarning("Błąd", "Nie znaleziono wybranego pliku modelu.")
        except Exception as e:
            self.etykieta_statusu.config(text="❌ Nie udało się wczytać modelu", fg="#e74c3c")
            messagebox.showerror("Błąd", f"Wczytywanie modelu nie powiodło się:\n{str(e)}")

    def reset_modelu(self):
        if messagebox.askyesno("Potwierdzenie",
                               "Czy na pewno chcesz zresetować model? Utracisz wszystkie nauczone wagi."):
            self.agent = AgentQUCZENIE(self.srodowisko.przestrzen_akcji)
            self.etykieta_statusu.config(text="🔄 Model zresetowany do stanu początkowego", fg="#3498db")
            self.aktualizuj_info_modelu()

    def reset_aplikacji(self):
        self.obecna_nazwa_labiryntu = self.zmienna_labiryntu.get()
        self.srodowisko = SrodowiskoLabiryntu(self.labirynty[self.obecna_nazwa_labiryntu])
        self.agent = AgentQUCZENIE(self.srodowisko.przestrzen_akcji)
        self.renderuj_labirynt()
        self.etykieta_statusu.config(text="🔄 Aplikacja zresetowana", fg="#3498db")
        self.tekst_statystyk.config(state=tk.NORMAL)
        self.tekst_statystyk.delete(1.0, tk.END)
        self.tekst_statystyk.insert(tk.END,
                                    "📊 STATYSTYKI UCZENIA:\n- Epizody: 0\n- Sukces: 0.00%\n- Śr. Kroki: 0.0\n- Czas: 0.00s")
        self.tekst_statystyk.config(state=tk.DISABLED)
        self.aktualizuj_info_modelu()

    def pokaz_ranking(self):
        ranking = self.tracker_wydajnosci.pobierz_ranking()
        if not ranking:
            messagebox.showinfo("Ranking", "Brak zapisanych wyników trenowania.")
            return

        okno_rankingu = tk.Toplevel(self.root)
        okno_rankingu.title("🏆 Ranking Modeli")
        okno_rankingu.geometry("700x600")
        okno_rankingu.configure(bg="#2c3e50")

        tekst = tk.Text(okno_rankingu, width=80, height=35, bg="#34495e", fg="#ecf0f1", font=("Consolas", 10))
        tekst.pack(padx=20, pady=20)

        tekst.insert(tk.END, "🏆 RANKING MODELI (wg skuteczności i czasu)\n")
        tekst.insert(tk.END, "=" * 65 + "\n\n")

        for i, wpis in enumerate(ranking, 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "  "
            tekst.insert(tk.END, f"{medal} #{i} {wpis['model']}\n")
            tekst.insert(tk.END, f"   Labirynt: {wpis['labirynt']}\n")
            tekst.insert(tk.END, f"   Sukces: {wpis['sukces']:>6.2f}% | Czas: {wpis['czas']:>6.2f}s\n")
            tekst.insert(tk.END, f"   Epizody: {wpis['epizody']:,}\n")
            tekst.insert(tk.END, "-" * 65 + "\n\n")

        tekst.config(state=tk.DISABLED)

    def pokaz_wykresy_uczenia(self):
        try:
            import matplotlib
            matplotlib.use('TkAgg')
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
            from matplotlib.figure import Figure

            if not hasattr(self.agent, 'historia_uczenia') or len(self.agent.historia_uczenia) < 5:
                messagebox.showinfo("Brak danych",
                                    "Brak wystarczającej ilości danych do wyświetlenia wykresów. Najpierw wytrenuj model.")
                return

            okno_wykresow = tk.Toplevel(self.root)
            okno_wykresow.title("📈 Wykresy Postępu Uczenia")
            okno_wykresow.geometry("1000x600")
            okno_wykresow.configure(bg="#2c3e50")

            historia = self.agent.historia_uczenia
            epizody = [h[0] for h in historia]
            sukcesy = [h[1] for h in historia]
            kroki = [h[2] for h in historia]

            fig = Figure(figsize=(10, 5), dpi=100)
            ax1 = fig.add_subplot(121)
            ax2 = fig.add_subplot(122)

            ax1.plot(epizody, sukcesy, color='#3498db', linewidth=2.5)
            ax1.fill_between(epizody, sukcesy, alpha=0.3, color='#3498db')
            ax1.set_title('Wskaźnik Sukcesu w Czasie', fontsize=14, color='#ecf0f1', weight='bold')
            ax1.set_xlabel('Epizod', fontsize=11, color='#bdc3c7')
            ax1.set_ylabel('Sukces (%)', fontsize=11, color='#bdc3c7')
            ax1.grid(True, alpha=0.3, color='#34495e')
            ax1.set_facecolor('#2c3e50')
            ax1.tick_params(colors='#bdc3c7')

            ax2.plot(epizody, kroki, color='#e74c3c', linewidth=2.5)
            ax2.fill_between(epizody, kroki, alpha=0.3, color='#e74c3c')
            ax2.set_title('Średnia Liczba Kroków', fontsize=14, color='#ecf0f1', weight='bold')
            ax2.set_xlabel('Epizod', fontsize=11, color='#bdc3c7')
            ax2.set_ylabel('Kroki', fontsize=11, color='#bdc3c7')
            ax2.grid(True, alpha=0.3, color='#34495e')
            ax2.set_facecolor('#2c3e50')
            ax2.tick_params(colors='#bdc3c7')

            fig.tight_layout()
            canvas = FigureCanvasTkAgg(fig, master=okno_wykresow)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        except ImportError:
            messagebox.showwarning("Brak biblioteki",
                                   "Matplotlib nie jest zainstalowany. Zainstaluj go komendą: pip install matplotlib")

    def otworz_reczne_trenowanie(self):
        if self.okno_recznego_trenowania is None or not self.okno_recznego_trenowania.okno.winfo_exists():
            self.okno_recznego_trenowania = OknoRecznegoTrenowania(self.root, self)
        else:
            self.okno_recznego_trenowania.okno.lift()
            self.okno_recznego_trenowania.okno.focus_force()

    def otworz_system_wskazowek(self):
        okno_wskazowek = tk.Toplevel(self.root)
        okno_wskazowek.title("💡 System Wskazówek")
        okno_wskazowek.geometry("650x550")
        okno_wskazowek.configure(bg="#2c3e50")

        info = tk.Label(okno_wskazowek, text="System Wskazówek - przewodnik po zaawansowanych funkcjach",
                        bg="#2c3e50", fg="#9b59b6", font=("Segoe UI", 14, "bold"))
        info.pack(pady=15)

        opis = tk.Text(okno_wskazowek, height=20, width=75, bg="#34495e", fg="#ecf0f1", font=("Segoe UI", 10),
                       wrap=tk.WORD)
        opis.pack(padx=20, pady=10)

        tresc = """
🧠 JAK DZIAŁA UCZENIE Z CZĘŚCIOWĄ OBserwowalnościĄ?
Agent widzi TYLKO 4 komórki wokół siebie (góra, dół, lewo, prawo). 
Nie zna całej mapy! Musi nauczyć się rozpoznawać wzorce, które prowadzą do celu.

🎯 STRATEGIE SKUTECZNEGO UCZENIA:
1. Użyj TRYBU "Dokładny" dla trudnych labiryntów (>20x20)
2. Zwiększ liczbę epizodów (min. 2000 dla dużych labiryntów)
3. Dostosuj wsp. uczenia: 0.35-0.5 dla szybkiego startu, 0.2-0.3 dla stabilności
4. Użyj systemu WSKAZÓWEK dla kluczowych punktów decyzyjnych

💡 JAK DODAWAĆ WSKAZÓWKI?
1. Otwórz "Ręczne Trenowanie"
2. Przeprowadź agenta do punktu decyzyjnego (np. skrzyżowanie)
3. Kliknij "Dodaj Wskazówkę" i wskaż preferowany kierunek
4. Ustaw siłę wskazówki (1-10) - wyższa = silniejszy wpływ na decyzje

⚡ ZAAWANSOWANE TECHNIKI:
- "Eksploracyjny" tryb: utrzymuje wysoką eksplorację (ε>0.1) dla odkrywania nowych ścieżek
- Nagrody za zbliżanie się do celu: agent dostaje +2 za każdy krok w kierunku celu
- System anty-stagnacji: automatycznie wyrywa agenta z zapętlenia

📊 INTERPRETACJA WYKRESÓW:
- Niebieski wykres: stabilny wzrost = dobry progres uczenia
- Czerwony wykres: spadająca liczba kroków = agent znajduje krótsze ścieżki
- Gwałtowne spadki sukcesu: zbyt szybkie zmniejszanie eksploracji (zwiększ min_epsilon)

🔧 OPTYMALNE PARAMETRY DLA RÓŻNYCH LABIRYNTÓW:
- Prosty (6x7): epizody=500, α=0.4, γ=0.95
- Średni (7x7): epizody=1200, α=0.35, γ=0.96
- Trudny (9x9): epizody=2500, α=0.3, γ=0.97
- Duży (15x15+): epizody=5000+, α=0.25, γ=0.98, min_epsilon=0.05
"""
        opis.insert(tk.END, tresc)
        opis.config(state=tk.DISABLED)

        zamknij = ttk.Button(okno_wskazowek, text="Zamknij", command=okno_wskazowek.destroy)
        zamknij.pack(pady=15)


if __name__ == "__main__":
    root = tk.Tk()
    aplikacja = AplikacjaLabiryntu(root)

    ramka_przyciskow = ttk.Frame(root)
    ramka_przyciskow.pack(side=tk.BOTTOM, fill=tk.X, padx=15, pady=(0, 15))

    aplikacja.przycisk_trenuj = ttk.Button(ramka_przyciskow, text="🚀 Trenuj AI", command=aplikacja.trenuj_ai)
    aplikacja.przycisk_trenuj.pack(side=tk.LEFT, padx=5)

    aplikacja.przycisk_uruchom = ttk.Button(ramka_przyciskow, text="▶️ Uruchom Ścieżkę",
                                            command=aplikacja.uruchom_najlepsza_sciezke)
    aplikacja.przycisk_uruchom.pack(side=tk.LEFT, padx=5)

    aplikacja.przycisk_reset = ttk.Button(ramka_przyciskow, text="🔄 Reset", command=aplikacja.reset_aplikacji)
    aplikacja.przycisk_reset.pack(side=tk.LEFT, padx=5)

    aplikacja.przycisk_ranking = ttk.Button(ramka_przyciskow, text="🏆 Ranking", command=aplikacja.pokaz_ranking)
    aplikacja.przycisk_ranking.pack(side=tk.LEFT, padx=5)

    aplikacja.przycisk_postep = ttk.Button(ramka_przyciskow, text="📈 Postęp Uczenia",
                                           command=lambda: OknoPostepuUczenia(root, aplikacja))
    aplikacja.przycisk_postep.pack(side=tk.LEFT, padx=5)

    root.mainloop()