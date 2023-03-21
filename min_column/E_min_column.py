"""
A program for building a set cover by the method of minimum column - maximum row.
2023, VNTU, 6KN-22b, Ishchenko Gleb
Works only with matrices (tables) of 7 rows and 10 columns (the 10th - prices)!
"""

# Matrix by condition
I = [1, 0, 0, 1, 0, 0, 0, 0, 1, 2] #1
O = [1, 0, 0, 0, 0, 0, 1, 0, 1, 1] #2
P = [1, 0, 1, 0, 0, 1, 0, 1, 0, 3] #3
A = [0, 0, 0, 0, 1, 0, 1, 1, 0, 2] #4
S = [0, 1, 0, 1, 1, 0, 1, 0, 1, 4] #5
D = [0, 1, 1, 1, 0, 0, 0, 0, 0, 1] #6
F = [1, 0, 0, 0, 1, 1, 0, 0, 0, 1] #7
matrix = [I, O, P, A, S, D, F]

matrix_ad = [I[:], O[:], P[:], A[:], S[:], D[:], F[:]] # 2nd matrix. A copy of the original matrix for copying rows into the array of the coating formation
matrix_ed = [I[:], O[:], P[:], A[:], S[:], D[:], F[:]] # 3rd matrix. A copy of the original matrix to remove columns from it

Cover = [1, 1, 1, 1, 1, 1 ,1 , 1, 1] # Coverage to check
Temp = [0, 0, 0, 0, 0, 0, 0 ,0, 0] # Temporary array for matrix row operations

total_cost = 0 # Spent cost counter
used_rows = [] # Counter of lines used to form the cover
columns = 9 # Column counter of the 3rd matrix
ones_indexes = [] # Counter of columns that were deleted in the 3rd matrix

# Loop of the minimum column - maximum row algorithm
# Until the temporary coverage array is not equal to coverage
while Temp != Cover:
    # We update the number of columns of the 3rd matrix according to the number of ones in the row obtained at the end of the last iteration of the loop
    columns -= len(ones_indexes)
    # We update the counters
    top_ones = 10
    cur_ones = 0
    top_column = 0
    column_rows_with_ones = []
    top_row = 0

    # We find the column with the smallest number of ones from the columns of the 3rd matrix
    for i in range(columns):
        cur_ones = 0
        for j in range(7):
            cur_ones += matrix_ed[j][i]
        if cur_ones < top_ones:
            top_ones = cur_ones
            top_column = i

    # We write out in a separate array the numbers of the rows that have a one in the column we just received
    for j in range(7):
        if matrix_ed[j][top_column] == 1:
            column_rows_with_ones.append(j)

    # We find from these rows in the 2nd matrix the one with the largest number of ones
    top_ones = 0
    for row_num in column_rows_with_ones:
        cur_ones = 0
        for i in range(9):
            cur_ones += matrix_ad[row_num][i]
        if cur_ones > top_ones:
            top_ones = cur_ones
            top_row = row_num

    # We copy the ones from the received line into a temporary array, and also record the number of this line and its price
    for i in range(9):
        if matrix_ad[top_row][i] == 1:
            Temp[i] = 1
            if i not in ones_indexes:
                ones_indexes.append(i)
    total_cost += matrix_ad[top_row][9]
    used_rows.append(top_row)

    # We correct the indices of the columns to be deleted, since the indices will change after they are deleted
    for k in range(len(ones_indexes)):
        if k != 0:
            ones_indexes[k] -= k

    # We return the 3rd matrix to its original state, and then delete the necessary columns
    matrix_ed = [I[:], O[:], P[:], A[:], S[:], D[:], F[:]]
    for column_index in ones_indexes:
        for j in range(7):
            del matrix_ed[j][column_index]

print(f"Coverage found for PRICE {total_cost} for {len(used_rows)} ROWS, specifically: ", end="")
for row in used_rows:
    if row != used_rows[-1]:
        print(f"{row + 1}, ", end="")
    else:
        print(f"{row + 1}.")
