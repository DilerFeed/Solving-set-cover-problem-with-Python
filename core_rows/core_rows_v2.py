"""
Програма для побудови покриття методом ядерних рядків. Покращена версія.
6КН-22б, Іщенко Гліб
Працює з матрицями (таблицями) будь-якого розміру.
"""

# Матриця за умовою
#   |         matrix             | row number
Q = [1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1] #1
W = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2] #2
E = [1, 0, 1, 0, 0, 1, 0, 1, 0, 3, 3] #3
R = [0, 0, 0, 0, 1, 0, 1, 1, 0, 2, 4] #4
T = [1, 1, 0, 0, 1, 0, 1, 0, 0, 4, 5] #5
Y = [0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 6] #6
U = [0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 7] #7
I = [1, 0, 0, 0, 1, 1, 0, 0, 0, 4, 8] #8
O = [1, 0, 0, 0, 1, 1, 0, 1, 0, 3, 9] #9
P = [1, 0, 0, 0, 0, 1, 0, 0, 0, 2, 10] #10
matrix = [Q, W, E, R, T, Y, U, I, O, P]

# Матриця, яку будемо скорочувати. Також змінні для її розміру.
matrix_copy = [Q[:], W[:], E[:], R[:], T[:], Y[:], U[:], I[:], O[:], P[:]]
m_c_rows = len(matrix_copy)
m_c_columns = (len(Q) - 2)
# Масив ядерних рядків
Core_rows_array = []
# Функція коректировки індексів номерів рядків, для їх коректного видалення з матриці
def index_correction(index_array):
    for k in range(len(index_array)):
        if k != 0:
            index_array[k] -= k
# Функція, яка рахує кількість одиниць в рядку будь-якого розміру
def count_ones(row):
    counter = 0
    for element in range(len(row) - 2):
        if element == 1:
            counter += 1
    return counter

# Власне метод ядерних рядків
changed = True
# Поки є зміни в стані матриці
while changed == True:
    changed = False
    core_columns = []
    core_rows = []
    # Шукаємо ядерні рядки (та затронуті їми стовпці). Якщо такі є, записуємо їх індекси в масив core_rows (та core_columns)
    for column_index in range(m_c_columns):
        ones_counter = 0
        for row_index in range(m_c_rows):
            if matrix_copy[row_index][column_index] == 1:
                ones_counter += 1
                one_index = row_index
        if ones_counter == 1:
            core_columns.append(column_index)
            core_rows.append(one_index)
            changed = True
    # Переносимо їх з оригінальної матриці в масив до кінця програми
    for core_row in core_rows:
        Core_rows_array.append(matrix[core_row])
    # Сортуємо та коректуємо індекси
    core_rows.sort()
    index_correction(core_columns)
    index_correction(core_rows)
    # Видаляємо ядерні рядки (та затронуті їми стовпці) з матриці. Записуємо нові розміри матриці.
    for column_index in core_columns:
        for row_index in range(m_c_rows):
            del matrix_copy[row_index][column_index]
    for row_index in core_rows:
        del matrix_copy[row_index]
    m_c_rows = len(matrix_copy)
    m_c_columns = (len(matrix_copy[0]) - 2)
    # Шукаємо антиядерні рядки, видаляємо їх з матриці, записуємо нові її розміри
    anticore_rows = []
    for row_index in range(m_c_rows):
        if count_ones(matrix_copy[row_index]) == 0:
            anticore_rows.append(row_index)
            changed = True
    anticore_rows.sort()
    index_correction(anticore_rows)
    for row_index in anticore_rows:
        del matrix_copy[row_index]
    m_c_rows = len(matrix_copy)
    # Шукаємо рядки, які поглинаються, та записуємо їх у масив absorbed_rows
    absorbed_rows = []
    for main_row_index in range(m_c_rows):
        for secondary_row_index in range(m_c_rows):
            break_out_flag = False
            if main_row_index != secondary_row_index:
                for column_index in range(m_c_columns):
                    if matrix_copy[main_row_index][column_index] == 1 and matrix_copy[main_row_index][column_index] != matrix_copy[secondary_row_index][column_index]:
                        break_out_flag = True
                        break
                if break_out_flag:
                    continue
                if count_ones(matrix_copy[main_row_index]) <= count_ones(matrix_copy[secondary_row_index]) and main_row_index not in absorbed_rows and matrix_copy[main_row_index][-2] >= matrix_copy[secondary_row_index][-2]:
                    absorbed_rows.append(main_row_index)
                    changed = True
    # Коректуємо індекси цих рядків, видаляємо їх з матриці, записуємо новий розмір матриці
    index_correction(absorbed_rows)
    for row_index in absorbed_rows:
        del matrix_copy[row_index]
    m_c_rows = len(matrix_copy)

Cover = [1, 1, 1, 1, 1, 1 ,1 , 1, 1] # Покриття для перевірки
Empty_row = [0, 0, 0, 0, 0, 0, 0 ,0, 0] # Тимчасовий масив для операцій з рядками матриці
for element in range(9 - m_c_columns): # Коректуємо розміри рядків згідно розміру матриці
    del Cover[0]
    del Empty_row[0]

# Будуємо покриття методом перебору завдяки рекурсивній функції find_cover
current_amount_row = []
best_amount_row = []
best_amount = 1000
current_cost_row = []
best_cost_row = []
best_cost = 1000
def find_cover(last_cost_counter, last_row_counter, last_row_Temp):
    global best_amount, best_amount_row, best_cost, best_cost_row
    for row in range(last_row_counter, m_c_rows):
        Temp = last_row_Temp[:]
        row_counter = last_row_counter + 1
        current_amount_row.append(row)
        current_cost_row.append(row)
        cost = matrix_copy[row][-2] + last_cost_counter
        for element in range(m_c_columns):
            if Temp[element] == 0 and matrix_copy[row][element] == 1:
                Temp[element] = 1
        if Temp == Cover:
            if row_counter < best_amount:
                best_amount = row_counter
                best_amount_row = current_amount_row[:]
            if cost < best_cost:
                best_cost = cost
                best_cost_row = current_cost_row[:]
            current_amount_row.remove(row)
            current_cost_row.remove(row)
            continue
        else:
            find_cover(cost, row_counter, Temp)
            current_amount_row.remove(row)
            current_cost_row.remove(row)
            
# Викликаємо рекурсивну фукнцію (знаходимо покриття)
find_cover(0, 0, Empty_row)
# Змінуюємо індекси рядків у складі рішень знаходження покриття на індекси цих рядків у оригінальній матриці
for row in range(len(best_amount_row)):
    best_amount_row[row] = matrix_copy[best_amount_row[row]][-1]
for row in range(len(best_cost_row)):
    best_cost_row[row] = matrix_copy[best_cost_row[row]][-1]
# Обʼєднуємо рядки з найкращих рішень знаходження покриття з ядерними рдками
for core_row in Core_rows_array:
    best_amount += 1
    best_amount_row.append(core_row[-1])
    best_cost += core_row[-2]
    best_cost_row.append(core_row[-1])
best_amount_row.sort()
best_cost_row.sort()

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
