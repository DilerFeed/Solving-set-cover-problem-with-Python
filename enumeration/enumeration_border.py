"""
Програма для побудови покриття методом граничного перебору.
2023, ВНТУ, 6КН-22б, Іщенко Гліб
Працює тільки з матрицями (таблицями) на 7 рядків
"""

# Матриця за умовою (матричне представлення)
i = [1, 0, 0, 1, 0, 0, 0, 0, 1, 2] #1
o = [1, 0, 0, 0, 0, 0, 1, 0, 1, 1] #2
p = [1, 0, 1, 0, 0, 1, 0, 1, 0, 3] #3
a = [0, 0, 0, 0, 1, 0, 1, 1, 0, 2] #4
s = [0, 1, 0, 1, 1, 0, 1, 0, 1, 4] #5
d = [0, 1, 1, 1, 0, 0, 0, 0, 0, 1] #6
f = [1, 0, 0, 0, 1, 1, 0, 0, 0, 1] #7
matrix = [i, o, p, a, s, d, f]

# Лінійне представлення (не рекомендовано)
#matrix = [[1, 0, 0, 1, 0, 0, 0, 0, 1, 2], [1, 0, 0, 0, 0, 0, 1, 0, 1, 1], [1, 0, 1, 0, 0, 1, 0, 1, 0, 3], [0, 0, 0, 0, 1, 0, 1, 1, 0, 2], [0, 1, 0, 1, 1, 0, 1, 0, 1, 4], [0, 1, 1, 1, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 1, 1, 0, 0, 0, 1]]

Cover = [1, 1, 1, 1, 1, 1 ,1 , 1, 1] # Покриття для перевірки
Temp = [0, 0, 0, 0, 0, 0, 0 ,0, 0] # Тимчасовий масив для операцій з рядками матриці
Temp_additional = [0, 0, 0, 0, 0, 0, 0 ,0, 0] # Тимчасовий допоміжний масив для запамʼятовування вигляду тимчасового масиву на минулому вимірі
# Лічильники
best_amount = 1000
best_amount_row = []
best_cost = 1000
best_cost_row = []
row_counter = 0
cost = 0

# Для кожного рядка
for i in range(7):
    # Для першого виміру
    # Оновлюємо значення тимчасового масиву
    Temp = [0, 0, 0, 0, 0, 0, 0 ,0, 0]
    # Записуємо значення лічильників для знаходження найркащих варіантів
    row_counter = 1
    cost = matrix[i][9]
    # Для кожного елемента рядку
    for m in range(10):
        # Окрім останнього (ціни)
        if m == 9:
            break
        # Скопіювати значення у тимчасовий масив
        Temp[m] = matrix[i][m]
    # Якщо тимчасовий масив = покриття
    if Temp == Cover:
        # Зберігаємо результати
        # На першому вимірі завжди ставиться рекорд по кількості рядків - 1
        best_amount = row_counter
        best_amount_row.clear()
        best_amount_row.append(i+1)
        # Якщо ціна менш ніж зафіксована рекордна
        if cost < best_cost:
            # Записуємо на якому рядку вона була зафіксована
            best_cost = cost
            best_cost_row.clear()
            best_cost_row.append(i+1)
        # Переходимо на інший рядок, щоб уникнути надлишкових покриттів (ГРАНИЧНИЙ ПЕРЕБОР)
        continue
    # Інакше: записуємо значення тимчасового масиву на 1-у вимірі у допоміжний
    Temp_additional = Temp
    # Для другого  виміру
    for o in range(1, 7):
        # Записуємо значення лічильників для знаходження найркащих варіантів
        row_counter = 2
        cost = matrix[i][9] + matrix[o][9]
        # Оновлюємо значення тимчасового масиву методом зрізу з допоміжного масиву 1-го виміру
        Temp = Temp_additional[:]
        # Для всіх рядків окрім рядка з минулого виміру
        if o != i:
            # Для кожного елемента рядку
            for m in range(10):
                # Окрім останнього (ціни)
                if m == 9:
                    break
                # Якщо значення поточного елементу у тимчасовому масиві не 1, а поточного елементу у поточному рядку матриці 1
                if Temp[m] != 1 and matrix[o][m] == 1:
                    # Скопіювати значення у тимчасовий масив
                    Temp[m] = matrix[o][m]
            # Якщо тимчасовий масив = покриття
            if Temp == Cover:
                # Зберігаємо результати
                # Якщо поставлен рекорд по кількості рядків для покриття
                if row_counter < best_amount:
                    best_amount = row_counter
                    best_amount_row = [i+1, o+1]
                # Якщо поставлен рекорд по ціні для покриття
                if cost < best_cost:
                    best_cost = cost
                    best_cost_row = [i+1, o+1]
                # Переходимо на інший рядок, щоб уникнути надлишкових покриттів (ГРАНИЧНИЙ ПЕРЕБОР)
                continue
            # Інакше: записуємо значення тимчасового масиву на 2-у вимірі у допоміжний
            Temp_additional_B = Temp
            # Продовжуємо подібні дії для глибших вимірів
            for p in range(2, 7):
                row_counter = 3
                cost = matrix[i][9] + matrix[o][9] + matrix[p][9]
                Temp = Temp_additional_B[:]
                if p not in [i, o]:
                    for m in range(10):
                        if m == 9:
                            break
                        if Temp[m] != 1 and matrix[p][m] == 1:
                            Temp[m] = matrix[p][m]
                    if Temp == Cover:
                        if row_counter < best_amount:
                            best_amount = row_counter
                            best_amount_row = [i+1, o+1, p+1]
                        if cost < best_cost:
                            best_cost = cost
                            best_cost_row = [i+1, o+1, p+1]
                        continue
                    Temp_additional_C = Temp
                    for a in range(3, 7):
                        row_counter = 4
                        cost = matrix[i][9] + matrix[o][9] + matrix[p][9] + matrix[a][9]
                        Temp = Temp_additional_C[:]
                        if a not in [i, o, p]:
                            for m in range(10):
                                if m == 9:
                                    break
                                if Temp[m] != 1 and matrix[a][m] == 1:
                                    Temp[m] = matrix[a][m]
                            if Temp == Cover:
                                if row_counter < best_amount:
                                    best_amount = row_counter
                                    best_amount_row = [i+1, o+1, p+1, a+1]
                                if cost < best_cost:
                                    best_cost = cost
                                    best_cost_row = [i+1, o+1, p+1, a+1]
                                continue
                            Temp_additional_D = Temp
                            for s in range(4, 7):
                                row_counter = 5
                                cost = matrix[i][9] + matrix[o][9] + matrix[p][9] + matrix[a][9] + matrix[s][9]
                                Temp = Temp_additional_D[:]
                                if s not in [i, o, p, a]:
                                    for m in range(10):
                                        if m == 9:
                                            break
                                        if Temp[m] != 1 and matrix[s][m] == 1:
                                            Temp[m] = matrix[s][m]
                                    if Temp == Cover:
                                        if row_counter < best_amount:
                                            best_amount = row_counter
                                            best_amount_row = [i+1, o+1, p+1, a+1, s+1]
                                        if cost < best_cost:
                                            best_cost = cost
                                            best_cost_row = [i+1, o+1, p+1, a+1, s+1]
                                        continue
                                    Temp_additional_E = Temp
                                    for d in range(5, 7):
                                        row_counter = 6
                                        cost = matrix[i][9] + matrix[o][9] + matrix[p][9] + matrix[a][9] + matrix[s][9] + matrix[d][9]
                                        Temp = Temp_additional_E[:]
                                        if d not in [i, o, p, a, s]:
                                            for m in range(10):
                                                if m == 9:
                                                    break
                                                if Temp[m] != 1 and matrix[d][m] == 1:
                                                    Temp[m] = matrix[d][m]
                                            if Temp == Cover:
                                                if row_counter < best_amount:
                                                    best_amount = row_counter
                                                    best_amount_row = [i+1, o+1, p+1, a+1, s+1, d+1]
                                                if cost < best_cost:
                                                    best_cost = cost
                                                    best_cost_row = [i+1, o+1, p+1, a+1, s+1, d+1]
                                                continue
                                            Temp_additional_F = Temp
                                            for f in range(6, 7):
                                                row_counter = 7
                                                cost = matrix[i][9] + matrix[o][9] + matrix[p][9] + matrix[a][9] + matrix[s][9] + matrix[d][9] + matrix[f][9]
                                                Temp = Temp_additional_F[:]
                                                if f not in [i, o, p, a, s, d]:
                                                    for m in range(10):
                                                        if m == 9:
                                                            break
                                                        if Temp[m] != 1 and matrix[f][m] == 1:
                                                            Temp[m] = matrix[f][m]
                                                    if Temp == Cover:
                                                        if row_counter < best_amount:
                                                            best_amount = row_counter
                                                            best_amount_row = [i+1, o+1, p+1, a+1, s+1, d+1, f+1]
                                                        if cost < best_cost:
                                                            best_cost = cost
                                                            best_cost_row = [i+1, o+1, p+1, a+1, s+1, d+1, f+1]
                                                        continue

# Вивід результатів (Динамічний - працює з довільною кількість рядків результату)
print("Найркащі рішення: ")
print(f"За кількістю рядків: ЗА {best_amount} рядки(ів), а саме: ", end="")
for row in best_amount_row:
    if row != best_amount_row[-1]:
        print(f"{row}, ", end="")
    else:
        print(f"{row}.")
print("---------------------------------------------------------")
print(f"За ціною: ЗА ЦІНУ {best_cost} комбінацією таких рядків: ", end="")
for row in best_cost_row:
    if row != best_cost_row[-1]:
        print(f"{row}, ", end="")
    else:
        print(f"{row}.")
