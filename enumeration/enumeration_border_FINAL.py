"""
Програма для побудови покриття методом граничного перебору за допомогою рекурсивної функції.
6КН-22б, Іщенко Гліб
Працює з матрицями (таблицями) будь-якого розміру (потрібне налаштування масивів Cover та Empty_row)
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

Cover = [1, 1, 1, 1, 1, 1 ,1 , 1, 1] # Покриття для перевірки
Empty_row = [0, 0, 0, 0, 0, 0, 0 ,0, 0] # Тимчасовий масив для операцій з рядками матриці
# Лічильники
current_amount_row = []
best_amount_row = []
best_amount = 1000
current_cost_row = []
best_cost_row = []
best_cost = 1000
# Метод граничного перебору рекусривною функцією
def find_cover(last_cost_counter, last_row_counter, last_row_Temp):
    # Переводимо змінні у глобальний режим
    global best_amount, best_amount_row, best_cost, best_cost_row
    # Для рядка у цьому вимірі
    for row in range(last_row_counter, len(matrix)):
        # Тимчасовий масив дорівнює копії тимчасового масиву з минулого виміру методом зрізу
        Temp = last_row_Temp[:]
        # Лічильник рядків збільшується на 1, в порівнянні з лічильником з минулого виміру
        row_counter = last_row_counter + 1
        # Додаємо у масив використаних для поточного рішення рядків рядок з поточного виміру
        current_amount_row.append(row)
        current_cost_row.append(row)
        # Лічильник ціни збільшується на ціну рядку з поточного виміру (додається до значення ціни рядку з минулого виміру)
        cost = matrix[row][-1] + last_cost_counter
        # Копіюємо рядок поточного виміру у тимчасовий масив цієї комбінації рядків (комбінації вимірів)
        for element in range(len(matrix[0]) - 1):
            if Temp[element] == 0 and matrix[row][element] == 1:
                Temp[element] = 1
        # Якщо отримане покриття
        if Temp == Cover:
            # Перевіряємо на найкращі рішення та, якщо такі є, записуємо їх
            if row_counter < best_amount:
                best_amount = row_counter
                best_amount_row = current_amount_row[:]
            if cost < best_cost:
                best_cost = cost
                best_cost_row = current_cost_row[:]
            # Видаляємо записи о використанні рядку з цього виміру та переходимо на наступну ітерацію циклу
            current_amount_row.remove(row)
            current_cost_row.remove(row)
            continue
        # Якщо ні
        else:
            # Використовуємо цю функцію у цій функції (використовуємо рекурсію)
            find_cover(cost, row_counter, Temp)
            # Після повернення до поточного виміру, видаляємо записи о використанні рядку з цього виміру та переходимо на наступну ітерацію циклу
            current_amount_row.remove(row)
            current_cost_row.remove(row)
# Викликаємо рекурсивну фукнцію (знаходимо покриття)
find_cover(0, 0, Empty_row)

print("Найркащі рішення: ")
print(f"За кількістю рядків: ЗА {best_amount} рядки(ів), а саме: ", end="")
for row in best_amount_row:
    if row != best_amount_row[-1]:
        print(f"{row + 1}, ", end="")
    else:
        print(f"{row + 1}.")
print("---------------------------------------------------------")
print(f"За ціною: ЗА ЦІНУ {best_cost} комбінацією таких рядків: ", end="")
for row in best_cost_row:
    if row != best_cost_row[-1]:
        print(f"{row + 1}, ", end="")
    else:
        print(f"{row + 1}.")