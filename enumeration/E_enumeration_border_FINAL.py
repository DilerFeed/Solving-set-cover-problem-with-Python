"""
A program for building a set cover by the method of border enumeration.
2023, VNTU, 6KN-22b, Ishchenko Gleb
Works with matrices (tables) of any size (Cover and Empty_row arrays must be configured)
"""

# Matrix by condition (matrix representation)
i = [1, 0, 0, 1, 0, 0, 0, 0, 1, 2] #1
o = [1, 0, 0, 0, 0, 0, 1, 0, 1, 1] #2
p = [1, 0, 1, 0, 0, 1, 0, 1, 0, 3] #3
a = [0, 0, 0, 0, 1, 0, 1, 1, 0, 2] #4
s = [0, 1, 0, 1, 1, 0, 1, 0, 1, 4] #5
d = [0, 1, 1, 1, 0, 0, 0, 0, 0, 1] #6
f = [1, 0, 0, 0, 1, 1, 0, 0, 0, 1] #7
matrix = [i, o, p, a, s, d, f]

Cover = [1, 1, 1, 1, 1, 1 ,1 , 1, 1] # Coverage to check
Empty_row = [0, 0, 0, 0, 0, 0, 0 ,0, 0] # Temporary array for matrix row operations
# Counters
current_amount_row = []
best_amount_row = []
best_amount = 1000
current_cost_row = []
best_cost_row = []
best_cost = 1000

# The method of border enumeration by recursive function
def find_cover(last_cost_counter, last_row_counter, last_row_Temp):
    # We transfer variables to global mode
    global best_amount, best_amount_row, best_cost, best_cost_row
    # For a row in this dimension
    for row in range(last_row_counter, len(matrix)):
        # The temporary array is equal to a copy of the temporary array from the previous dimension by the slice method
        Temp = last_row_Temp[:]
        # The row counter is increased by 1, compared to the counter from the last dimension
        row_counter = last_row_counter + 1
        # Add a row from the current dimension to the array of rows used for the current solution
        current_amount_row.append(row)
        current_cost_row.append(row)
        # The cost counter is increased by the cost of the row from the current dimension (added to the value of the cost of the row from the previous dimension)
        cost = matrix[row][-1] + last_cost_counter
        # We copy the row of the current dimension into the temporary array of this combination of rows (combination of measurements)
        for element in range(len(matrix[0]) - 1):
            if Temp[element] == 0 and matrix[row][element] == 1:
                Temp[element] = 1
        # If received coverage
        if Temp == Cover:
            # We check for the best solutions and, if there are any, write them down
            if row_counter < best_amount:
                best_amount = row_counter
                best_amount_row = current_amount_row[:]
            if cost < best_cost:
                best_cost = cost
                best_cost_row = current_cost_row[:]
            # We delete records about the use of a row from this dimension and move to the next iteration of the loop
            current_amount_row.remove(row)
            current_cost_row.remove(row)
            continue
        # If not
        else:
            # Use this function in this function (use recursion)
            find_cover(cost, row_counter, Temp)
            # After returning to the current dimension, we delete records about the use of the row from this dimension and go to the next iteration of the loop
            current_amount_row.remove(row)
            current_cost_row.remove(row)
# Call the recursive function (find the coverage)
find_cover(0, 0, Empty_row)

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
