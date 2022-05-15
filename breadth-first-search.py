import numpy as np
from scipy.sparse import random

# Input: random, sparse matrix
matrix = random(11, 9, density=0.1).A
matrix = np.ceil(matrix * 10)

# Output 1: new sequence for a block-diagonal matrix
new_row_order = []
new_column_order = []
# Output 2: list of blocks in the block-diagonal matrix
list_of_svd_blocks = []
# list of already searched rows / columns
searched_row = [False for i in range(np.shape(matrix)[0])]
searched_column = [False for i in range(np.shape(matrix)[1])]
# queue for next rows/columns to be searched
next_row = []
next_column = []

for start_column in range(np.shape(matrix)[1]):  # search all columns once
    if not searched_column[start_column]:  # not yet searched
        svd_block = []  # Output 2
        # add column to next_column queue
        next_column.append(start_column)

        while next_column or next_row:  # if not empty

            # step 1
            for column in next_column:
                # search column
                for row, entry in enumerate(matrix[:, column]):
                    if (entry != 0.) and (not searched_row[row]):
                        svd_block.append([row, column])  # Output 2
                        # add row to next_row queue
                        next_row.append(row)
                new_column_order.append(column)  # Output 1
                # add column to searched_columns
                searched_column[column] = True
                # delete column from next_column queue
                next_column.pop(0)

            # step 2
            for row in next_row:
                # search row
                for column, entry in enumerate(matrix[row, :]):
                    if (entry != 0.) and (not searched_column[column]):
                        svd_block.append([row, column])  # Output 2
                        # add column to next_column queue
                        next_column.append(column)
                new_row_order.append(row)  # Output 1
                # add row to searched_rows
                searched_row[row] = True
                # delete row from next_row queue
                next_row.pop(0)

        # Output 2: add block to list_of_blocks
        list_of_svd_blocks.append(svd_block)

# print reordered, block-diagonal matrix
print('Input matrix before reordering\n', matrix)
print('After reordering')
reordered_matrix = np.zeros(np.shape(matrix))
for new_row, old_row in enumerate(new_row_order):
    for new_column, old_column in enumerate(new_column_order):
        reordered_matrix[new_row, new_column] = matrix[old_row, old_column]
print(reordered_matrix)
