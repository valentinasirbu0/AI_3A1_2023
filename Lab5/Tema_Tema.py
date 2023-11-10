magic_square = [
    [8, 1, 6],
    [3, 5, 7],
    [4, 9, 2],
]


def initialize_game():
    return [8, 1, 6, 3, 5, 7, 4, 9, 2, 'A']


def get_current_player(state):
    return 'A' if state[9] == 'A' else 'B'


def check_winner(matrix, player):
    for i in range(3):
        if matrix[i * 3: i * 3 + 3].count(player) == 3 or matrix[i:9:3].count(player) == 3:
            return True, player
    if matrix[0:9:4].count(player) == 3 or matrix[2:7:2].count(player) == 3:
        return True, player
    return False, None


def is_game_over(matrix):

    for player in ['A', 'B']:
        result, winner = check_winner(matrix, player)
        if result:
            return True, winner

    if all(isinstance(cell, int) for cell in matrix):
        return True, 'Draw'

    return False, None


def is_valid_move(matrix, number):
    return number in matrix


def make_move(state, number):
    player = get_current_player(state)
    if not is_valid_move(state, number):
        return None
    index_of_num = state.index(number)
    new_state = state.copy()
    new_state[index_of_num] = player
    new_state[9] = 'A' if player == 'B' else 'B'
    return new_state


def evaluate_board(state):
    def count_value(symbol, opponent_symbol, line):
        count_symbol = line.count(symbol)
        count_opponent = line.count(opponent_symbol)
        return count_symbol ** 2 - count_opponent ** 2 if count_symbol > 0 and count_opponent == 0 else 0

    def check_final_state():
        is_final, winner = is_game_over(state)
        return 100 if is_final and winner == 'A' else -100 if is_final and winner == 'B' else 0

    value = check_final_state()

    for i in range(3):
        value_row = count_value('A', 'B', state[i * 3: i * 3 + 3])
        value_col = count_value('A', 'B', state[i:9:3])

        # Adaugă scorul pentru jucătorul 'A'
        value += value_row + value_col

        # Scade scorul pentru jucătorul 'B'
        value_row_opponent = count_value('B', 'A', state[i * 3: i * 3 + 3])
        value_col_opponent = count_value('B', 'A', state[i:9:3])
        value -= value_row_opponent + value_col_opponent

    value_diag1 = count_value('A', 'B', state[0:9:4])
    value_diag2 = count_value('A', 'B', state[2:7:2])

    # Adaugă scorul pentru jucătorul 'A'
    value += value_diag1 + value_diag2

    # Scade scorul pentru jucătorul 'B'
    value_diag1_opponent = count_value('B', 'A', state[0:9:4])
    value_diag2_opponent = count_value('B', 'A', state[2:7:2])
    value -= value_diag1_opponent + value_diag2_opponent

    return value


def generate_possible_moves(matrix):
    return [make_move(matrix, i + 1) for i in range(9) if is_valid_move(matrix, i + 1)]


def minimax(depth, matrix):
    if is_game_over(matrix)[0] or depth == 0:
        return matrix, evaluate_board(matrix)

    player = get_current_player(matrix)
    possible_moves = generate_possible_moves(matrix)
    best_value = float('-inf') if player == 'A' else float('inf')
    best_matrix = matrix

    for move in possible_moves:
        _, value = minimax(depth - 1, move)
        if (player == 'A' and value > best_value) or (player == 'B' and value < best_value):
            best_value = value
            best_matrix = move

    return best_matrix, best_value


def display_board(matrix):
    if matrix is not None:
        player = get_current_player(matrix)
        print(f'Player {player}: ')
        for i in range(3):
            row = matrix[i * 3: i * 3 + 3]
            print(" | ".join(str(cell) if isinstance(cell, int) else cell for cell in row))
            if i < 2:
                print("-" * 9)


def play_game():
    matrix = initialize_game()
    display_board(matrix)

    while not is_game_over(matrix)[0]:
        player = get_current_player(matrix)
        if player == 'A':
            number = int(input("Your move: "))
            new_matrix = make_move(matrix, number)
            display_board(new_matrix)
            if new_matrix is None:
                print("Invalid number!")
                continue
            matrix = new_matrix
        else:
            new_matrix, _ = minimax(3, matrix)
            matrix = new_matrix
            display_board(matrix)

    print(is_game_over(matrix))


play_game()
