import random

# mapping from fitness value to the probability the matrix will be chosen
fitness_to_probability = {
    0: 100,
    1: 97,
    2: 94,
    3: 94,
    4: 92,
    5: 90,
    6: 85,
    7: 85,
    8: 80,
    9: 70,
    10: 60,
    11: 40,
    12: 40,
    13: 40,
    14: 40,
    15: 40
}

number_of_mutations = 1
percent_of_mutations = 35


# building the board all solutions will be chosen by
def build_game_matrix(size):
    cell_rows = []
    for i in range(0, size):
        cell_col = [0] * size
        cell_rows.append(cell_col)
    return cell_rows


# copy the matrix to another one
def clone_matrix(my_matrix):
    cell_rows = []
    for i in range(0, len(my_matrix)):
        cell_cols = []
        for j in range(0, len(my_matrix[i])):
            cell_cols.append(my_matrix[i][j])
        cell_rows.append(cell_cols)
    return cell_rows


# randomly choosing the first generation - every row will be a premutation
def generate_generation_0(population_size, startMatrix):
    solutions_dictionary = {}
    all_numbers_list = []
    for i in range(1, len(startMatrix) + 1):
        all_numbers_list.append(i)
    for index in range(0, population_size):
        # coping the matrix in order to add it to the dictionary
        newMatrix = clone_matrix(startMatrix)
        for row in range(0, len(newMatrix)):
            my_list = []
            my_list.extend(all_numbers_list)
            for col in range(0, len(newMatrix[row])):
                # if the number is already in the game board
                if newMatrix[row][col] != 0:
                    my_list.remove(newMatrix[row][col])
            for col in range(0, len(newMatrix[row])):
                # choosing a number to put in this place in the matrix and removing it from the list
                if newMatrix[row][col] == 0:
                    newMatrix[row][col] = random.choice(my_list)
                    my_list.remove(newMatrix[row][col])
        solutions_dictionary[index] = newMatrix
    # print(solutions_dictionary)
    return solutions_dictionary


# each grade will be calculated by number of mismatch for the game roles in the matrix
def calculate_matrix_grade(my_matrix, sign_dict):
    grade = 0
    seen_numbers = []
    # going over the columns of the matrix and counting the number of values missing to have a permutation
    for col in range(0, len(my_matrix)):
        for row in range(0, len(my_matrix)):
            if my_matrix[row][col] not in seen_numbers:
                seen_numbers.append(my_matrix[row][col])
            # checking if there is not a match by the sign
            if sign_dict.get((row, col)) is not None:
                for value in sign_dict.get((row, col)):
                    if my_matrix[row][col] < my_matrix[value[0]][value[1]]:
                        grade = grade + 1
        grade = grade + len(my_matrix) - len(seen_numbers)
        seen_numbers.clear()

    return grade


# going over al the matrix and fot each matrix calculating the fitness grade.
def calculate_fitness_grade(solutions_dictionary, sign_dict):
    fitness_grade_list = []
    for key in solutions_dictionary:
        my_matrix = solutions_dictionary[key]
        fitness_grade_list.append(calculate_matrix_grade(my_matrix, sign_dict))
    return fitness_grade_list


"""
how the crossover works?
we are doing a crossover between the rows of the matrix - 
randomly choosing which row to take from which matrix.
"""
def crossover(matrix1, matrix2):
    new_matrix = []
    for i in range(0, len(matrix1)):
        row_in = random.randint(1, 2)
        if row_in == 1:
            new_matrix.append(matrix1[i].copy())
        else:
            new_matrix.append(matrix2[i].copy())
    return new_matrix


"""
for mutation - we randomly chose a line and two places in the line (of numbers that are not 
preset) and switching between the numbers.
"""
def mutations(matrix, digits_places):
    for i in range(0, number_of_mutations):
        row = random.randint(0, len(matrix) - 1)
        col_to_chose = [x for x in range(len(matrix[row]))]
        col = random.choice(col_to_chose)
        while (row, col) in digits_places:
            col_to_chose.remove(col)
            col = random.choice(col_to_chose)
        col_to_chose.remove(col)
        col2 = random.choice(col_to_chose)
        while (row, col2) in digits_places:
            col_to_chose.remove(col2)
            col2 = random.choice(col_to_chose)
        # swap
        temp = matrix[row][col2]
        matrix[row][col2] = matrix[row][col]
        matrix[row][col] = temp


"""
for creating a next generation - 
the best solution will automaticly continue to the next generation.
than from all the solutions we will randomly chose 2 matrix to do cross over between them
giving priority for those with lower fitness grade
"""

def create_next_generation(min_index, fitness_gr, solution_dict, digits_places):
    new_generation_dict = {}
    # taking the best solution for the next generation
    new_generation_dict[0] = solution_dict[min_index]
    mutations(new_generation_dict[0], digits_places)
    solution_to_chose = [x for x in range(100)]
    probability_to_chose = []
    # creating the probability of matrix to be chosen list by the matrix grade
    for grade in fitness_gr:
        if grade > 15:
            probability_to_chose.append(30)
        else:
            probability_to_chose.append(fitness_to_probability[grade])
    # crossover
    for i in range(1, 100):
        matrix_chosen = random.choices(solution_to_chose, weights=probability_to_chose, k=2)
        while matrix_chosen[0] == matrix_chosen[1]:
            matrix_chosen = random.choices(solution_to_chose, weights=probability_to_chose, k=2)
        new_generation_dict[i] = crossover(solution_dict[matrix_chosen[0]], solution_dict[matrix_chosen[1]])
    # mutations on the new generation - for 20% of the population
    # by the percent of mutations we will now how much mutations to do
    index_todo_mutations = random.choices(solution_to_chose, weights=probability_to_chose, k=percent_of_mutations)
    for index in index_todo_mutations:
        mutations(new_generation_dict[index], digits_places)

    return new_generation_dict


"""
early gathering - 
it the highest difference from the minimum value is smaller than a trashhold than we are
in early gathering. In this case we will do a lot of mutations on the solutions
"""
def handle_and_check_early_gathering(fitness_list, min_fitness, treshold, number_of_bigger_numbers):
    global number_of_mutations
    global percent_of_mutations
    count = 0

    for grade in fitness_list:
        # if we found a difference bigger than the treshold than we are not in early gathering
        if grade - min_fitness > treshold:
            count += 1
            if count > number_of_bigger_numbers:
                number_of_mutations = 1
                percent_of_mutations = 35
                return
    percent_of_mutations = 70
    number_of_mutations = 2


def calculate_average_grade(fitness_grades):
    sum = 0
    for grade in fitness_grades:
        sum += grade
    return sum / len(fitness_grades)


def optimize_solution(solution_dict, sign_dict, given_digits_place):
    count = 0
    for key in solution_dict:
        matrix = solution_dict[key]
        for row in range(0, len(matrix)):
            for col in range(0, len(matrix)):
                # grade_before_change = calculate_matrix_grade(matrix, sign_dict)
                # copy_matrix = clone_matrix(matrix)
                if (row, col) in sign_dict and (row, col + 1) in sign_dict[(row, col)] and (
                        row, col) not in given_digits_place and (row, col + 1) not in given_digits_place:
                    # if the numbers don't respect the sign we will switch them
                    # we wat to do only one change in every row
                    if matrix[row][col] < matrix[row][col + 1]:
                        temp = matrix[row][col + 1]
                        matrix[row][col + 1] = matrix[row][col]
                        matrix[row][col] = temp
                        count += 1
                # if the number in the col near me do not respect the sign
                elif (row, col) in sign_dict and (row, col - 1) in sign_dict[(row, col)] and (
                        row, col) not in given_digits_place and (row, col - 1) not in given_digits_place:
                    if matrix[row][col] < matrix[row][col - 1]:
                        temp = matrix[row][col - 1]
                        matrix[row][col - 1] = matrix[row][col]
                        matrix[row][col] = temp
                        count += 1
                # if the number in the line below me do not respect the sign
                elif (row, col) in sign_dict and (row + 1, col) in sign_dict[(row, col)] and (
                        row, col) not in given_digits_place and (row + 1, col) not in given_digits_place:
                    if matrix[row][col] < matrix[row + 1][col]:
                        index1 = matrix[row].index(matrix[row + 1][col])
                        index2 = matrix[row + 1].index(matrix[row][col])
                        if (row, index1) not in given_digits_place and (row + 1, index2) not in given_digits_place:
                            temp = matrix[row + 1][col]
                            matrix[row + 1][col] = matrix[row][col]
                            matrix[row][col] = temp
                            temp = matrix[row + 1][index2]
                            matrix[row + 1][index2] = matrix[row][index1]
                            matrix[row][index1] = temp
                            count += 1
                # if the number in the row above me do not respect the sign
                elif (row, col) in sign_dict and (row - 1, col) in sign_dict[(row, col)] and (
                        row, col) not in given_digits_place and (row - 1, col) not in given_digits_place:
                    if matrix[row][col] < matrix[row - 1][col]:
                        index1 = matrix[row].index(matrix[row - 1][col])
                        index2 = matrix[row - 1].index(matrix[row][col])
                        if (row, index1) not in given_digits_place and (row - 1, index2) not in given_digits_place:
                            temp = matrix[row - 1][col]
                            matrix[row - 1][col] = matrix[row][col]
                            matrix[row][col] = temp
                            temp = matrix[row - 1][index2]
                            matrix[row - 1][index2] = matrix[row][index1]
                            matrix[row][index1] = temp
                            count += 1
                if count == len(matrix):
                    return


# cloning all the matrix dict
def clone_dict(solution_dict):
    solution_dict2 = {}
    for key in solution_dict:
        for row in solution_dict[key]:
            if solution_dict2.get(key) is None:
                solution_dict2[key] = [row.copy()]
            else:
                solution_dict2[key].append(row.copy())
    return solution_dict2
