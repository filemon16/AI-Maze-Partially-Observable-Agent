import random


class GeneratorLabiryntu:
    @staticmethod
    def wygeneruj_labirynt(szerokosc, wysokosc, trudnosc=0.3):
        if szerokosc < 5 or wysokosc < 5:
            szerokosc = max(5, szerokosc)
            wysokosc = max(5, wysokosc)

        labirynt = [[1 for _ in range(szerokosc)] for _ in range(wysokosc)]

        start_x, start_y = 1, 1
        labirynt[start_y][start_x] = 0

        stos = [(start_x, start_y)]
        kierunki = [(0, 2), (2, 0), (0, -2), (-2, 0)]

        while stos:
            x, y = stos[-1]
            sasiedzi = []

            for dx, dy in kierunki:
                nx, ny = x + dx, y + dy
                if 0 < nx < szerokosc - 1 and 0 < ny < wysokosc - 1 and labirynt[ny][nx] == 1:
                    sasiedzi.append((nx, ny))

            if sasiedzi:
                nx, ny = random.choice(sasiedzi)
                labirynt[ny][nx] = 0
                labirynt[y + (ny - y) // 2][x + (nx - x) // 2] = 0
                stos.append((nx, ny))
            else:
                stos.pop()

        cel_x, cel_y = szerokosc - 2, wysokosc - 2
        proby = 0
        while labirynt[cel_y][cel_x] == 1 and proby < 100:
            cel_x = random.randint(max(1, szerokosc // 2), szerokosc - 2)
            cel_y = random.randint(max(1, wysokosc // 2), wysokosc - 2)
            proby += 1

        if labirynt[cel_y][cel_x] == 1:
            for r in range(wysokosc - 2, 0, -1):
                for c in range(szerokosc - 2, 0, -1):
                    if labirynt[r][c] == 0:
                        cel_y, cel_x = r, c
                        break
                else:
                    continue
                break

        labirynt[cel_y][cel_x] = 9

        return labirynt