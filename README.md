# AI Maze – Partially Observable Agent




[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![Status](https://img.shields.io/badge/status-complete-brightgreen.svg)](https://github.com/yourusername/maze-ai-pro)

**Zaawansowana aplikacja Python z Q-Learning, gdzie agent widzi TYLKO 4 sąsiednie komórki i musi nauczyć się strategii bez pełnej wizji labiryntu.**

<img width="1297" height="955" alt="Zrzut ekranu z 2026-02-01 23-02-23" src="https://github.com/user-attachments/assets/b7ad72df-b6e4-4c6d-a537-b739d3126d89" />

## 📋 Spis treści

- [Opis projektu](#opis-projektu)
- [Główne funkcje](#główne-funkcje)
- [Wymagania](#wymagania)
- [Instalacja](#instalacja)
- [Szybki start](#szybki-start)
- [Dokumentacja](#dokumentacja)
- [Struktura projektu](#struktura-projektu)
- [Przykłady użycia](#przykłady-użycia)
- [Technologie](#technologie)
- [Autor](#autor)
- [Licencja](#licencja)

## 📖 Opis projektu

**Labirynt AI Pro** to zaawansowana aplikacja edukacyjna demonstrująca uczenie ze wzmocnieniem (Reinforcement Learning) w trudnym środowisku z **częściową obserwowalnością**. W przeciwieństwie do tradycyjnych rozwiązań, gdzie agent widzi cały labirynt, nasz AI ma dostęp **TYLKO do 4 sąsiednich komórek** (góra, dół, lewo, prawo), co znacząco utrudnia proces uczenia się optymalnej strategii.

Projekt wykorzystuje algorytm **Q-Learning** z dynamicznym systemem nagród, eksploracją epsilon-greedy oraz zaawansowanymi technikami przyspieszania konwergencji. Aplikacja posiada profesjonalny interfejs graficzny z pełną kontrolą nad procesem uczenia.

## ✨ Główne funkcje

### 🎯 Agent z ograniczoną percepcją
- Agent widzi **TYLKO 4 sąsiednie komórki** (brak pełnej wizji labiryntu)
- System nagród za zbliżanie się do celu (+2 za każdy krok w kierunku celu)
- Inteligentna obsługa stagnacji i zapętleń

### 🗺️ Generator labiryntów
- **6 wbudowanych labiryntów** o rosnącej trudności (Prosty → Bardzo Duży)
- Generator własnych labiryntów **do 300×300 komórek**
- Regulowana trudność generowanych labiryntów
- Algorytm DFS z randomizacją dla unikalnych labiryntów

### 🤖 Zaawansowane uczenie
- **4 tryby trenowania**: Szybki, Standardowy, Dokładny, Eksploracyjny
- Dostosowywalne parametry: współczynnik uczenia, eksploracja, dyskont
- System wskazówek ręcznych dla przewodnictwa agenta
- Ręczne trenowanie z interaktywnym sterowaniem
- Historia uczenia z wykresami w czasie rzeczywistym

### 📊 Analiza i wizualizacja
- **Interaktywne wykresy** postępu uczenia (sukces, liczba kroków)
- Ranking modeli z porównaniem wydajności
- Statystyki w czasie rzeczywistym
- Podgląd widoku agenta podczas uczenia

### 💾 Zarządzanie modelami
- Zapisywanie i wczytywanie wytrenowanych modeli
- System wydajności z rankingiem najlepszych modeli
- Reset modelu do stanu początkowego

### 🎮 Interfejs użytkownika
- Profesjonalny, nowoczesny design z motywem ciemnym
- Intuicyjne sterowanie i nawigacja
- Wizualizacja ruchu agenta z płynną animacją
- System podpowiedzi i instrukcji

## 📦 Wymagania

- **Python 3.8+**
- **tkinter** (zazwyczaj wbudowany w Pythona)
- **matplotlib** (do wykresów uczenia)

## 🔧 Instalacja

### 1. Sklonuj repozytorium

```bash


https://github.com/filemon16/AI-Maze-Partially-Observable-Agent.git

cd maze-ai-pro
