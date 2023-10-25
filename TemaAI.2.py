import Manhattan
import Euclidean
import Hamming
import time
import heapq

def initialize_state(instance):
    initial_state = [instance[i:i + 3] for i in range(0, 9, 3)]
    last_zero_position = find_empty_slot(initial_state)
    return initial_state, last_zero_position


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


def Solve(init_state, last_move, max_depth, euristic):
    for depth in range(max_depth + 1):
        if euristic == "IDDFS":
            solution = depth_limited_DFS(init_state, last_move, depth)
        else:
            solution = depth_limited_Greedy(init_state, last_move, depth, euristic)
        if solution:
            return solution
    return None


def depth_limited_DFS(matrix, last_move, depth, move_count=0):
    if is_final_state(matrix):
        return matrix, move_count

    if depth == 0:
        return None

    for direction in ['UP', 'DOWN', 'LEFT', 'RIGHT']:
        new_matrix, new_last_move = transition([row.copy() for row in matrix], last_move, direction)
        if new_matrix != matrix:
            res = depth_limited_DFS(new_matrix, new_last_move, depth-1, move_count + 1)
            if res:
                return res
    return None


def depth_limited_Greedy(matrix, last_move, depth, euristic, move_count=0):
    if is_final_state(matrix):
        return matrix, move_count

    if depth == 0:
        return None

    possible_moves = []

    for direction in ['UP', 'DOWN', 'LEFT', 'RIGHT']:
        new_matrix, new_last_move = transition([row.copy() for row in matrix], last_move, direction)
        if new_matrix != matrix:
            heuristic_value = euristic(new_matrix)
            possible_moves.append((new_matrix, new_last_move, heuristic_value))

    possible_moves.sort(key=lambda move: move[2])

    for new_matrix, new_last_move, _ in possible_moves:
        res = depth_limited_Greedy(new_matrix, new_last_move, depth - 1, euristic, move_count + 1)
        if res is not None:  # Return the count, not None
            return res

    return None


###################################################################################################################

# Euristică: Distanța Manhattan
def h(state):
    return Manhattan.manhattan(state)

# Determină dacă o configurație este starea obiectiv
def is_final(state):
    return (state)

# Generează succesorii unei configurații
def neighbors(state):
    return get_successors(state)

def get_successors(configuration):
    successors = []
    i, j = None, None

    # 1. Găsirea spațiului gol (0)
    for row in range(3):
        for col in range(3):
            if configuration[row][col] == 0:
                i, j = row, col
                break

    # 2. Încercarea tuturor mișcărilor posibile

    # Mișcare sus
    if i > 0:
        new_config = [row[:] for row in configuration]  # Creează o copie a configurației
        new_config[i][j], new_config[i-1][j] = new_config[i-1][j], new_config[i][j]
        successors.append(new_config)

    # Mișcare jos
    if i < 2:
        new_config = [row[:] for row in configuration]
        new_config[i][j], new_config[i+1][j] = new_config[i+1][j], new_config[i][j]
        successors.append(new_config)

    # Mișcare stânga
    if j > 0:
        new_config = [row[:] for row in configuration]
        new_config[i][j], new_config[i][j-1] = new_config[i][j-1], new_config[i][j]
        successors.append(new_config)

    # Mișcare dreapta
    if j < 2:
        new_config = [row[:] for row in configuration]
        new_config[i][j], new_config[i][j+1] = new_config[i][j+1], new_config[i][j]
        successors.append(new_config)

    return successors

# Distanța dintre două stări consecutive. În cazul nostru, este întotdeauna 1 pentru puzzle-ul de alunecare.
def dist(neighbor, state):
    return 1  # Deoarece fiecare mutare este la o distanță de 1 în puzzle-ul de alunecare.

# Verifică validitatea unei stări (poți să adaugi orice regulă suplimentară aici)
def is_valid(neighbor):
    return True  # În acest exemplu, orice succesor generat este valid.

# Reconstructează calea de la stare la stare inițială
def reconstruct_path(state, came_from):
    path = []
    while state in came_from:
        path.append(state)
        state = came_from[state]
    path.reverse()
    return path

# Implementarea algoritmului A*
def A_star(init_state):
    came_from = {}
    d = {}
    d[init_state] = 0
    f = {}
    f[init_state] = h(init_state)

    # Utilizez o listă pentru a simula PriorityQueue.
    pq = [(f[init_state], init_state)]

    while pq:
        _, state = heapq.heappop(pq)  # Extrag starea cu cea mai mică valoare f.

        if is_final(state):
            return reconstruct_path(state, came_from)

        for neighbor in neighbors(state):
            if is_valid(neighbor) and (neighbor not in d or d[neighbor] > d[state] + dist(neighbor, state)):
                d[neighbor] = d[state] + dist(neighbor, state)
                f[neighbor] = d[neighbor] + h(neighbor)
                came_from[neighbor] = state
                heapq.heappush(pq, (f[neighbor], neighbor))

    return None
#####################################################################################################################



instances = [
    #[8, 6, 7, 2, 5, 4, 0, 3, 1],
    [2, 5, 3, 1, 0, 6, 4, 7, 8]
    #[2, 7, 5, 0, 8, 4, 3, 1, 6]
]

solution = A_star(tuple(map(tuple, instances)))  # Convertesc lista de liste în tuple de tuple pentru a putea fi folosită ca cheie în dicționare.
print(solution)


'''
for instance in instances:
    print("\nFor instance:", instance)

    initial_matrix, _ = initialize_state(instance)
    strategies = ["IDDFS", Manhattan.manhattan, Euclidean.euclid, Hamming.hamming]

    for strategy in strategies:
        start_time = time.time()
        solution = Solve(initial_matrix, "NONE", 30, strategy)
        end_time = time.time()
        if solution:
            print("Solution found for", strategy, " : ")
            for row in solution:
                print(row)
        else:
            print("No solution found within the maximum depth.")
        print("Elapsed time:", end_time - start_time, "seconds")
'''



