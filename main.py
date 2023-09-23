import algorithm_operations
import matplotlib.pyplot as plt


def handle_input(file_object):
    matrix_size = file_object.readline()
    matrix = algorithm_operations.build_game_matrix(int(matrix_size))
    number_of_given_digits = file_object.readline()
    # putting the given digits of the board
    given_digits_place = []
    for i in range(0, int(number_of_given_digits)):
        value_and_coordinates = file_object.readline()
        array_values = value_and_coordinates.split()
        matrix[int(array_values[0]) - 1][int(array_values[1]) - 1] = int(array_values[2])
        given_digits_place.append((int(array_values[0]) - 1, int(array_values[1]) - 1))
    # putting the signs
    number_of_given_signs = file_object.readline()
    signs_dict = {}
    for i in range(0, int(number_of_given_signs)):
        coordinates = file_object.readline()
        array_values = coordinates.split()
        if signs_dict.get((int(array_values[0]) - 1, int(array_values[1]) - 1)) is None:
            signs_dict[(int(array_values[0]) - 1, int(array_values[1]) - 1)] = [
                (int(array_values[2]) - 1, int(array_values[3]) - 1)]
        else:
            signs_dict[(int(array_values[0]) - 1, int(array_values[1]) - 1)].append(
                (int(array_values[2]) - 1, int(array_values[3]) - 1))

    return matrix, signs_dict, given_digits_place


# at the end we will print the best of all solutions to console
def print_solution_to_console(solution_matrix, sign_dict, min_grade, generation):
    print("best solution:")
    # printing the solution
    for i in range(0, len(solution_matrix)):
        for j in range(0, len(solution_matrix)):
            print('|' + str(solution_matrix[i][j]) + '|', end="")
            if (i, j) in sign_dict and (i, j + 1) in sign_dict[(i, j)]:
                print(' > ', end="")
            elif (i, j + 1) in sign_dict and (i, j) in sign_dict[(i, j + 1)]:
                print(' < ', end="")
            else:
                print('   ', end="")
        print("")
        for j in range(0, len(solution_matrix)):
            if (i, j) in sign_dict and (i + 1, j) in sign_dict[(i, j)]:
                print(" v ", end="")
            elif (i + 1, j) in sign_dict and (i, j) in sign_dict[(i + 1, j)]:
                print(" ^ ", end="")
            else:
                print("   ", end="")
            print("   ", end="")
        print("")
    # fitness grade and generation
    print("fitness grade: " + str(min_grade))
    print("solution was in generation: " + str(generation))


# in each generation we will print the best solution
def print_solution_to_file(number_of_generation, solution_matrix, sign_dict, min_grade, average_grade):
    # opening the solution file we want to write to
    if number_of_generation == 0:
        f = open("solutions.txt", "w")
    else:
        f = open("solutions.txt", "a")
    f.write("number of generation: " + str(number_of_generation) + "\n\n")
    f.write("best solution:\n")
    # printing the solution
    for i in range(0, len(solution_matrix)):
        for j in range(0, len(solution_matrix)):
            f.write('|' + str(solution_matrix[i][j]) + '|')
            if (i, j) in sign_dict and (i, j + 1) in sign_dict[(i, j)]:
                f.write(' > ')
            elif (i, j + 1) in sign_dict and (i, j) in sign_dict[(i, j + 1)]:
                f.write(' < ')
            else:
                f.write('   ')
        f.write('\n')
        for j in range(0, len(solution_matrix)):
            if (i, j) in sign_dict and (i + 1, j) in sign_dict[(i, j)]:
                f.write(" v ")
            elif (i + 1, j) in sign_dict and (i, j) in sign_dict[(i + 1, j)]:
                f.write(" ^ ")
            else:
                f.write("   ")
            f.write("   ")
        f.write('\n')
        # fitness grade and generation
    f.write("best fitness grade: " + str(min_grade) + "\n")
    f.write("average fitness grade: " + str(average_grade) + "\n")

    f.write("\n")
    f.close()


def add_to_list(list_average, list_best, list_generation, average, min, number):
    list_average.append(average)
    list_best.append(min)
    list_generation.append(number)


"""
the three algorithms we want to execute - 
darvin, lamark and the regular algorithm.
"""

# executing the regular algorithm
def execute_regular_algorithm(solutions_dict, sign_dict, given_digits_place, list_average, list_best, list_generation):
    # initialize the parameters
    fitness_grade_list = algorithm_operations.calculate_fitness_grade(solutions_dict, sign_dict)
    min_fitness_grade = min(fitness_grade_list)
    number_of_generation = 0
    min_fitness_index = fitness_grade_list.index(min_fitness_grade)
    average_grade = algorithm_operations.calculate_average_grade(fitness_grade_list)
    print_solution_to_file(number_of_generation, solutions_dict[min_fitness_index], sign_dict, min_fitness_grade,
                           average_grade)
    # for saving the best solution
    best_solution = solutions_dict[min_fitness_index]
    best_min = min_fitness_grade
    best_generation = 0
    add_to_list(list_average, list_best, list_generation, average_grade, min_fitness_grade, number_of_generation)
    # while we did not find a solution or we did not get to the max iterations
    while min_fitness_grade != 0 and number_of_generation < 2000:
        # the next generation
        solutions_dict = algorithm_operations.create_next_generation(min_fitness_index, fitness_grade_list,
                                                                     solutions_dict,
                                                                     given_digits_place)
        fitness_grade_list = algorithm_operations.calculate_fitness_grade(solutions_dict, sign_dict)
        number_of_generation += 1
        min_fitness_grade = min(fitness_grade_list)
        min_fitness_index = fitness_grade_list.index(min_fitness_grade)
        # defining the best solution
        if min_fitness_grade < best_min:
            best_min = min_fitness_grade
            best_solution = solutions_dict[min_fitness_index]
            best_generation = number_of_generation
        # calculate and print solution
        average_grade = algorithm_operations.calculate_average_grade(fitness_grade_list)
        print_solution_to_file(number_of_generation, solutions_dict[min_fitness_index], sign_dict, min_fitness_grade,
                               average_grade)
        algorithm_operations.handle_and_check_early_gathering(fitness_grade_list, min_fitness_grade, 3, 7)
        add_to_list(list_average, list_best, list_generation, average_grade, min_fitness_grade, number_of_generation)
    return best_solution, best_min, best_generation


# executing the darvin algorithm
def execute_darvin_algorithm(solutions_dict, sign_dict, given_digits_place, list_average, list_best, list_generation):
    # cloning the solution so we could calculate the fitness by the optimize solution and
    # still use the old one
    new_dict = algorithm_operations.clone_dict(solutions_dict)
    algorithm_operations.optimize_solution(new_dict, sign_dict, given_digits_place)
    fitness_grade_list = algorithm_operations.calculate_fitness_grade(new_dict, sign_dict)
    min_fitness_grade = min(fitness_grade_list)
    number_of_generation = 0
    min_fitness_index = fitness_grade_list.index(min_fitness_grade)
    best_solution = solutions_dict[min_fitness_index]
    best_min = min_fitness_grade
    best_generation = 0
    average_grade = algorithm_operations.calculate_average_grade(fitness_grade_list)
    print_solution_to_file(number_of_generation, solutions_dict[min_fitness_index], sign_dict, min_fitness_grade,
                           average_grade)
    add_to_list(list_average, list_best, list_generation, average_grade, min_fitness_grade, number_of_generation)
    # while we did not find a solution or we did not get to the max iterations
    while min_fitness_grade != 0 and number_of_generation < 2000:
        # picking the next generation by the not optimized solution
        solutions_dict = algorithm_operations.create_next_generation(min_fitness_index, fitness_grade_list,
                                                                     solutions_dict,
                                                                     given_digits_place)
        # cloning the solutions dict so we wont destroy the older dict - we still want to use it.
        new_dict = algorithm_operations.clone_dict(solutions_dict)
        # optimize the solution and calculate the fitness grade by the optimized solutions
        algorithm_operations.optimize_solution(new_dict, sign_dict, given_digits_place)
        fitness_grade_list = algorithm_operations.calculate_fitness_grade(new_dict, sign_dict)
        # the next generation
        number_of_generation += 1
        min_fitness_grade = min(fitness_grade_list)
        min_fitness_index = fitness_grade_list.index(min_fitness_grade)
        if min_fitness_grade < best_min:
            best_min = min_fitness_grade
            best_solution = solutions_dict[min_fitness_index]
            best_generation = number_of_generation
        average_grade = algorithm_operations.calculate_average_grade(fitness_grade_list)
        print_solution_to_file(number_of_generation, solutions_dict[min_fitness_index], sign_dict, min_fitness_grade,
                               average_grade)
        algorithm_operations.handle_and_check_early_gathering(fitness_grade_list, min_fitness_grade, 3, 7)
        add_to_list(list_average, list_best, list_generation, average_grade, min_fitness_grade, number_of_generation)
    return best_solution, best_min, best_generation


# executing the darvin algorithm
def execute_lamark_algorithm(solutions_dict, sign_dict, given_digits_place, list_average, list_best, list_generation):
    algorithm_operations.optimize_solution(solutions_dict, sign_dict, given_digits_place)
    fitness_grade_list = algorithm_operations.calculate_fitness_grade(solutions_dict, sign_dict)
    min_fitness_grade = min(fitness_grade_list)
    number_of_generation = 0
    min_fitness_index = fitness_grade_list.index(min_fitness_grade)
    average_grade = algorithm_operations.calculate_average_grade(fitness_grade_list)
    print_solution_to_file(number_of_generation, solutions_dict[min_fitness_index], sign_dict, min_fitness_grade,
                           average_grade)
    best_solution = solutions_dict[min_fitness_index]
    best_min = min_fitness_grade
    best_generation = 0
    add_to_list(list_average, list_best, list_generation, average_grade, min_fitness_grade, number_of_generation)
    # while we did not find a solution or we did not get to the max iterations
    while min_fitness_grade != 0 and number_of_generation < 2000:
        # create the next generation by the optimized solution
        solutions_dict = algorithm_operations.create_next_generation(min_fitness_index, fitness_grade_list,
                                                                     solutions_dict,
                                                                     given_digits_place)
        algorithm_operations.optimize_solution(solutions_dict, sign_dict, given_digits_place)
        fitness_grade_list = algorithm_operations.calculate_fitness_grade(solutions_dict, sign_dict)
        number_of_generation += 1
        min_fitness_grade = min(fitness_grade_list)
        min_fitness_index = fitness_grade_list.index(min_fitness_grade)
        if min_fitness_grade < best_min:
            best_min = min_fitness_grade
            best_solution = solutions_dict[min_fitness_index]
            best_generation = number_of_generation
        average_grade = algorithm_operations.calculate_average_grade(fitness_grade_list)
        print_solution_to_file(number_of_generation, solutions_dict[min_fitness_index], sign_dict, min_fitness_grade,
                               average_grade)
        algorithm_operations.handle_and_check_early_gathering(fitness_grade_list, min_fitness_grade, 3, 7)
        add_to_list(list_average, list_best, list_generation, average_grade, min_fitness_grade, number_of_generation)
    return best_solution, best_min, best_generation


# the graph of the grades in each generation
def show_graph(list_average, list_best, list_generation):
    plt.xlabel('number of generation')
    plt.ylabel('fitness grade')
    plt.plot(list_generation, list_best, label="best fitness grade")
    plt.plot(list_generation, list_average, label="average fitness grade")
    plt.title('fitness grade per generation')
    plt.legend()
    plt.show()


if __name__ == "__main__":
    get_file = True
    file_path = input("insert the file path: ")
    while get_file:
        try:
            file = open(file_path, 'r')
            get_file = False
        except:
            file_path = input("wrong path, try again: ")

    matrix, signs_dict, given_digits_places = handle_input(file)
    solutions_dictionary = algorithm_operations.generate_generation_0(100, matrix)
    average_grade_list = []
    best_grade_list = []
    generation_list = []

    continue_to_get_input = True

    while continue_to_get_input:
        print("chose a number of algorithm to run: (insert 1 , 2 or 3)")
        print("1. lamark algorithm")
        print("2. dervin algorithm")
        print("3. regular algorithm")
        case = input()

        # chosing a case by the user input
        if case == '1':
            print("algorithm is running...")
            solution, min, generation = execute_lamark_algorithm(solutions_dictionary, signs_dict, given_digits_places,
                                                                 average_grade_list, best_grade_list, generation_list)
            print_solution_to_console(solution, signs_dict, min, generation)
            continue_to_get_input = False
        elif case == '2':
            print("algorithm is running...")
            solution, min, generation = execute_darvin_algorithm(solutions_dictionary, signs_dict, given_digits_places,
                                                                 average_grade_list, best_grade_list, generation_list)
            print_solution_to_console(solution, signs_dict, min, generation)
            continue_to_get_input = False
        elif case == '3':
            print("algorithm is running...")
            solution, min, generation = execute_regular_algorithm(solutions_dictionary, signs_dict, given_digits_places,
                                                                  average_grade_list, best_grade_list, generation_list)
            print_solution_to_console(solution, signs_dict, min, generation)
            continue_to_get_input = False

    show_graph(average_grade_list, best_grade_list, generation_list)
