def is_valid_matrix(matrix_in):
    # If the first element of the matrix is a list (greater than 1-D matrix), make sure all other
    # elements are lists
    if type(matrix_in[0]) == list:
        row_length = len(matrix_in[0])
        for row in matrix_in:
            if type(row) != list:
                return False
            # Make sure all rows are same length
            if len(row) != row_length:
                return False
            # Make sure all elements are numbers
            for elem in row:
                if type(elem) == int or type(elem) == float:
                    continue
                else:
                    return False
    # if first element is not a list, make sure this is 1-D matrix with numbers
    else:
        for elem in matrix_in:
            if type(elem) == int or type(elem) == float:
                continue
            else:
                return False
    return True


def multiply_rows(left_row, right_row):
    output = 0
    for i in range(len(left_row)):
        output += left_row[i] * right_row[i]
    return output


def multiply_matrices(left_matrix, right_matrix):
    if not is_valid_matrix(left_matrix) or not is_valid_matrix(right_matrix):
        if not is_valid_matrix(left_matrix):
            print(left_matrix, " is not a valid matrix.")
        if not is_valid_matrix(right_matrix):
            print(right_matrix, " is not a valid matrix.")
        raise TypeError
    if len(left_matrix) != len(right_matrix[0]) or len(left_matrix[0]) != len(right_matrix):
        print("Left matrix must have rows and columns equal of equal length to right matrix's columns and rows.")
        raise ValueError
    matrix_product = []
    multiplier = transpose_matrix(right_matrix)
    for left_row in left_matrix:
        output_row = []
        for right_row in multiplier:
            output_row.append(multiply_rows(left_row, right_row))
        matrix_product.append(output_row)
    return matrix_product


def transpose_matrix(matrix_in):
    if not is_valid_matrix(matrix_in):
        print(matrix_in, " is not a valid matrix.")
        raise TypeError
    matrix_out = []
    for i in range(len(matrix_in[0])):
        matrix_out.append([])
    for row in matrix_out:
        for i in range(len(matrix_in)):
            row.append(0)
    for i in range(len(matrix_in)):
        for j in range(len(matrix_in[i])):
            matrix_out[j][i] = matrix_in[i][j]
    return matrix_out




def format_matrix(matrix_in):
    output_str = ''
    if not is_valid_matrix(matrix_in):
        print(matrix_in, " is not a valid matrix.")
        raise TypeError
    if type(matrix_in) != list:
        for num in matrix_in:
            output_str += str(num)
            output_str += ' '
    else:
        for row in matrix_in:
            for num in row:
                output_str += str(num)
                output_str += ' '
            output_str += '\n'
    return output_str

