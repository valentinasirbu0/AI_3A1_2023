
#Etapa 1:
#-Matricea: Fiecare stare a puzzle-ului poate fi reprezentată ca o matrice 3x3. 0 va reprezenta celula goala.
#-Coordonatele celulei goale: Poziția celulei goale poate fi reprezentată prin coordonatele sale (i, j), unde i reprezintă rândul și j reprezintă coloana
#-last_zero_position: Valoarea efectivă a ultimei pozitii a celului goale.

#Etapa 2:
#Starea initiala reprezinta matricea initiala 3x3 creata din instanta(vector)
#Starea finala reprezinta vectorul aranjat crescator in intervalul 1-8
#Pentru verificarea starii finale, in urma etapelor algoritmului, matricea este tranformata in vector, se elimina zeroul si se verifica ordinea corecta a numerelor


# Functia de initializare: Primeste ca parametru instanta problemei si va returna starea initiala, aceasta
# constand in matricea obtinuta din lista primita ca parametru si pozitia celulei goale din matrice

def initialize_state(instance):
    initial_state = [instance[i:i + 3] for i in range(0, 9, 3)]
    last_zero_position = find_empty_slot(initial_state)
    return initial_state, last_zero_position

# Functia care verifica daca starea este finala: va adauga intr-o lista elementele din matrice, pe rand, exceptandu-l pe 0
# si va verifica daca aceasta este ordonata crescator

def is_final_state(matrix):
    numbers = [element for row in matrix for element in row if element != 0]
    return numbers == list(range(1, 9))


def find_empty_slot(matrix):
    zero_position = (100,100)
    for row_index, row in enumerate(matrix):
        for col_index, value in enumerate(row):
            if value == 0:
                zero_position = (row_index, col_index)
                break

    return zero_position


def is_valid_up(matrix, last_move):
    if last_move == 'DOWN':
        return False
    row, col = find_empty_slot(matrix)
    return row > 0


def is_valid_down(matrix, last_move):
    if last_move == 'UP':
        return False
    row, col = find_empty_slot(matrix)
    return row < 2


def is_valid_left(matrix, last_move):
    if last_move == 'RIGHT':
        return False
    row, col = find_empty_slot(matrix)
    return col > 0


def is_valid_right(matrix, last_move):
    if last_move == 'LEFT':
        return False
    row, col = find_empty_slot(matrix)
    return col < 2


# Mutarile casutei goale:

def move_up(matrix):
    row, col = find_empty_slot(matrix)
    matrix[row][col], matrix[row-1][col] = matrix[row-1][col], matrix[row][col]
    return matrix


def move_down(matrix):
    row, col = find_empty_slot(matrix)
    matrix[row][col], matrix[row+1][col] = matrix[row+1][col], matrix[row][col]
    return matrix


def move_left(matrix):
    row, col = find_empty_slot(matrix)
    matrix[row][col], matrix[row][col-1] = matrix[row][col-1], matrix[row][col]
    return matrix


def move_right(matrix):
    row, col = find_empty_slot(matrix)
    matrix[row][col], matrix[row][col+1] = matrix[row][col+1], matrix[row][col]
    return matrix


def transition(state, last_move, direction):
    if direction == "UP" and is_valid_up(state, last_move):
        move_up(state)
        new_last_move = "UP"
    elif direction == "DOWN" and is_valid_down(state, last_move):
        move_down(state)
        new_last_move = "DOWN"
    elif direction == "LEFT" and is_valid_left(state, last_move):
        move_left(state)
        new_last_move = "LEFT"
    elif direction == "RIGHT" and is_valid_right(state, last_move):
        move_right(state)
        new_last_move = "RIGHT"
    else:
        new_last_move = last_move

    return state, new_last_move


def IDDFS(init_state, last_move, max_depth):
    for depth in range(max_depth + 1):
        visited = set()
        solution = depth_limited_DFS(init_state, last_move, depth, visited)
        if solution:
            return solution
    return None


def depth_limited_DFS(matrix, last_move, depth, visited):
    matrix_str = str(matrix)
    if matrix_str in visited:
        return None

    if is_final_state(matrix):
        return matrix

    if depth == 0:
        return None

    visited.add(matrix_str)

    for direction in ['UP', 'DOWN', 'LEFT', 'RIGHT']:
        new_matrix, new_last_move = transition([row.copy() for row in matrix], last_move, direction)
        if new_matrix != matrix:
            res = depth_limited_DFS(new_matrix, new_last_move, depth-1, visited)
            if res:
                return res
    return None


instances = [
    [8, 6, 7, 2, 5, 4, 0, 3, 1],
    [2, 5, 3, 1, 0, 6, 4, 7, 8],
    [2, 7, 5, 0, 8, 4, 3, 1, 6]
]

for instance in instances:
    print("\nFor instance:", instance)

    initial_matrix, _ = initialize_state(instance)
    solution = IDDFS(initial_matrix, "NONE", 30)

    if solution:
        print("Solution found:")
        for row in solution:
            print(row)
    else:
        print("No solution found within the maximum depth.")
