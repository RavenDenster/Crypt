def rotate_positions(holes, angle):
    """
    Поворот координат свободных клеток на angle градусов по часовой.
    holes — список (r, c) с 1-индексацией.
    Возвращает отсортированный сверху вниз список.
    """
    res = []
    for r, c in holes:
        if angle == 0:
            res.append((r, c))
        elif angle == 90:
            res.append((c, 5 - r))
        elif angle == 180:
            res.append((5 - r, 5 - c))
        elif angle == 270:
            res.append((5 - c, r))
    res.sort(key=lambda x: (x[0], x[1]))
    return res


def encrypt_cardano(P, K1):
    """
    Шифрование методом «Решётка Кардано».
    P  — список байт (целых чисел).
    K1 — матрица-трафарет 4×4 (список строк, '0' — свободная клетка, '#' — занятая).
    Возвращает шифртекст C (список байт).
    """
    holes = []
    for i in range(4):
        for j in range(4):
            if K1[i][j] == '0':
                holes.append((i + 1, j + 1))

    C = []
    for start in range(0, len(P), 16):
        block = P[start:start + 16]
        matrix = [[None] * 4 for _ in range(4)]
        idx = 0

        for angle in (0, 90, 180, 270):
            positions = rotate_positions(holes, angle)
            for (r, c) in positions:
                if idx < len(block):
                    matrix[r - 1][c - 1] = block[idx]
                    idx += 1

        for row in matrix:
            for val in row:
                if val is not None:
                    C.append(val)

    return C


P = [75, 73, 76, 73, 77, 81, 74, 78, 77, 75, 77]

K1 = [
    "#0##",
    "0###",
    "##0#",
    "###0"
]

expected = [77, 75, 77, 73, 75, 81, 74, 76, 77, 78, 73]

C = encrypt_cardano(P, K1)

print("Открытый текст P =", P)
print("Шифртекст     C =", C)
print("Ожидается       =", expected)
print("Результат совпадает:", C == expected)