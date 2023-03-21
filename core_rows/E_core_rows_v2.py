"""
A program for building a set cover by the method of core rows.Improved version.
2023, VNTU, 6KN-22b, Ishchenko Gleb
Works with matrices (tables) of any size.
"""

# Matrix by condition
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

# The matrix that we will reduce. Also variables for its size.
matrix_copy = [Q[:], W[:], E[:], R[:], T[:], Y[:], U[:], I[:], O[:], P[:]]
m_c_rows = len(matrix_copy)
m_c_columns = (len(Q) - 2)
# Array of core rows
Core_rows_array = []
# The function of correcting the indices of the row numbers, for their correct removal from the matrix
def index_correction(index_array):
    for k in range(len(index_array)):
        if k != 0:
            index_array[k] -= k
# A function that counts the number of ones in a row of any size
def count_ones(row):
    counter = 0
    for element in range(len(row) - 2):
        if element == 1:
            counter += 1
    return counter

# Actually the method of core rows
changed = True
# While there are changes in the state of the matrix
while changed == True:
    changed = False
    core_columns = []
    core_rows = []
    # We are looking for core rows (and the columns affected by them). If there are any, we write their indexes in the core_rows (and core_columns) array
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
    # Transfer them from the original matrix to the array until the end of the program
    for core_row in core_rows:
        Core_rows_array.append(matrix[core_row])
    # Sort and correct indexes
    core_rows.sort()
    index_correction(core_columns)
    index_correction(core_rows)
    # Remove the core rows (and the columns affected by them) from the matrix. Record the new sizes of the matrix.
    for column_index in core_columns:
        for row_index in range(m_c_rows):
            del matrix_copy[row_index][column_index]
    for row_index in core_rows:
        del matrix_copy[row_index]
    m_c_rows = len(matrix_copy)
    m_c_columns = (len(matrix_copy[0]) - 2)
    # Look for anticore rows, remove them from the matrix, record its new sizes
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
    # Search for absorbed rows and write them in the absorbed_rows array
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
    # Correct the indices of these rows, remove them from the matrix, record the new size of the matrix
    index_correction(absorbed_rows)
    for row_index in absorbed_rows:
        del matrix_copy[row_index]
    m_c_rows = len(matrix_copy)

Cover = [1, 1, 1, 1, 1, 1 ,1 , 1, 1] # Coverage to check
Empty_row = [0, 0, 0, 0, 0, 0, 0 ,0, 0] # Temporary array for matrix row operations
for element in range(9 - m_c_columns): # Adjust the size of the rows according to the size of the matrix
    del Cover[0]
    del Empty_row[0]

# Build set cover by the method of border enumeration thanks to the recursive function find_cover
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
            
# Call the recursive function (find the coverage)
find_cover(0, 0, Empty_row)
# Change the indices of the rows in the composition of solutions for finding the coverage to the indices of these rows in the original matrix
for row in range(len(best_amount_row)):
    best_amount_row[row] = matrix_copy[best_amount_row[row]][-1]
for row in range(len(best_cost_row)):
    best_cost_row[row] = matrix_copy[best_cost_row[row]][-1]
# Combine rows from the best solutions for finding coverage with core rows
for core_row in Core_rows_array:
    best_amount += 1
    best_amount_row.append(core_row[-1])
    best_cost += core_row[-2]
    best_cost_row.append(core_row[-1])
best_amount_row.sort()
best_cost_row.sort()

print("The best solutions: ")
print(f"By the number of rows: FOR {best_amount} rows, or rather: ", end="")
for row in best_amount_row:
    if row != best_amount_row[-1]:
        print(f"{row + 1}, ", end="")
    else:
        print(f"{row + 1}.")
print("---------------------------------------------------------")
print(f"For the price: FOR THE PRICE {best_cost} by a combination of the following lines: ", end="")
for row in best_cost_row:
    if row != best_cost_row[-1]:
        print(f"{row + 1}, ", end="")
    else:
        print(f"{row + 1}.")
