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


def a_star_search(matrix, last_move, heuristic, max_depth):
    if is_final_state(matrix):
        return matrix, 0

    priority_queue = [(heuristic(matrix), matrix, last_move, 0)]  # Adding move_count to the tuple
    visited = set()

    while priority_queue:
        _, current_matrix, last_move, current_move_count = heapq.heappop(priority_queue)

        if tuple(map(tuple, current_matrix)) in visited:
            continue

        visited.add(tuple(map(tuple, current_matrix)))

        print("Intermediate state at move_count", current_move_count)
        for row in current_matrix:
            print(row)
        print("--------")

        if current_move_count >= max_depth:
            continue

        for direction in ['UP', 'DOWN', 'LEFT', 'RIGHT']:
            new_matrix, new_last_move = transition([row.copy() for row in current_matrix], last_move, direction)

            if tuple(map(tuple, new_matrix)) not in visited:
                if is_final_state(new_matrix):
                    return new_matrix, current_move_count + 1

                heapq.heappush(priority_queue, (
                heuristic(new_matrix) + current_move_count + 1, new_matrix, new_last_move, current_move_count + 1))

    return None


def Solve_A(init_state, last_move, max_depth, heuristic):
    return a_star_search(init_state, last_move, heuristic, max_depth)


instances = [
    #[8, 6, 7, 2, 5, 4, 0, 3, 1]
    #[2, 5, 3, 1, 0, 6, 4, 7, 8]
    [2, 7, 5, 0, 8, 4, 3, 1, 6]
]


for instance in instances:
    print("\nFor instance:", instance)

    initial_matrix, _ = initialize_state(instance)
    strategies = ["IDDFS", Manhattan.manhattan, Euclidean.euclid, Hamming.hamming]
    strategies2 = [Manhattan.manhattan, Euclidean.euclid, Hamming.hamming]

'''For IDDFS + GREEDY CU EURISTICI'''
'''
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
'''FOR A* cu euristici'''

for strategy in strategies2:
        start_time = time.time()
        solution, move_count = Solve_A(initial_matrix, "NONE", 30, strategy)
        end_time = time.time()
        if solution:
            print("Solution found for", strategy.__name__, " : ")
            for row in solution:
                print(row)
        else:
            print("No solution found within the maximum depth.")
        print("Elapsed time:", end_time - start_time, "seconds")