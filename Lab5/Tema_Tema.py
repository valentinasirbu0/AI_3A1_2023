magic_square = [
    [8, 1, 6],
    [3, 5, 7],
    [4, 9, 2],
]


def initialize_game():
    return [8, 1, 6, 3, 5, 7, 4, 9, 2, 'A']


def is_game_over(matrix):
    def check_winner(player):
        for i in range(3):
            if matrix[i * 3: i * 3 + 3].count(player) == 3 or matrix[i:9:3].count(player) == 3:
                return True, player
        if matrix[0:9:4].count(player) == 3 or matrix[2:7:2].count(player) == 3:
            return True, player
        return False, None

    for player in ['A', 'B']:
        result, winner = check_winner(player)
        if result:
            return True, winner

    if all(isinstance(cell, int) for cell in matrix):
        return True, 'remiza'

    return False, None


def is_valid_move(matrix, number):
    return number in matrix


def make_move(matrix, number):
    if not is_valid_move(matrix, number):
        return None
    pos = matrix.index(number)
    new_matrix = matrix.copy()
    new_matrix[pos] = matrix[9]
    new_matrix[9] = 'A' if matrix[9] == 'B' else 'B'
    return new_matrix


def evaluate_board(matrix):
    if is_game_over(matrix)[0]:
        if is_game_over(matrix)[1] == 'A':
            return 100
        elif is_game_over(matrix)[1] == 'B':
            return -100
        else:
            return 0
    value = 0
    for i in range(3):
        if matrix[i * 3: i * 3 + 3].count('A') > 0 and matrix[i * 3: i * 3 + 3].count('B') == 0:
            value += matrix[i * 3: i * 3 + 3].count('A') ** 2
        if matrix[i * 3: i * 3 + 3].count('B') > 0 and matrix[i * 3: i * 3 + 3].count('A') == 0:
            value -= matrix[i * 3: i * 3 + 3].count('B') ** 2
        if matrix[i:9:3].count('A') > 0 and matrix[i:9:3].count('B') == 0:
            value += matrix[i:9:3].count('A') ** 2
        if matrix[i:9:3].count('B') > 0 and matrix[i:9:3].count('A') == 0:
            value -= matrix[i:9:3].count('B') ** 2
    if matrix[0:9:4].count('A') > 0 and matrix[0:9:4].count('B') == 0:
        value += matrix[0:9:4].count('A') ** 2
    if matrix[0:9:4].count('B') > 0 and matrix[0:9:4].count('A') == 0:
        value -= matrix[0:9:4].count('B') ** 2
    if matrix[2:7:2].count('A') > 0 and matrix[2:7:2].count('B') == 0:
        value += matrix[2:7:2].count('A') ** 2
    if matrix[2:7:2].count('B') > 0 and matrix[2:7:2].count('A') == 0:
        value -= matrix[2:7:2].count('B') ** 2
    return value


def generate_possible_moves(matrix):
    return [make_move(matrix, i + 1) for i in range(9) if is_valid_move(matrix, i + 1)]


def minimax(depth, matrix):
    if is_game_over(matrix)[0] or depth == 0:
        return matrix, evaluate_board(matrix)

    if matrix[9] == 'B':
        possible_moves = generate_possible_moves(matrix)
        best_value = float('inf')
        best_matrix = matrix
        for move in possible_moves:
            _, value = minimax(depth - 1, move)
            if value < best_value:
                best_value = value
                best_matrix = move
        return best_matrix, best_value

    if matrix[9] == 'A':
        possible_moves = generate_possible_moves(matrix)
        best_value = float('-inf')
        best_matrix = matrix
        for move in possible_moves:
            _, value = minimax(depth - 1, move)
            if value > best_value:
                best_value = value
                best_matrix = move
        return best_matrix, best_value


def display_board(matrix):
    if matrix is not None:
        player = 'Player B: ' if matrix[9] == 'B' else 'Player A: '
        print(player)
        for i in range(3):
            row = matrix[i * 3: i * 3 + 3]
            print(" | ".join(str(cell) if isinstance(cell, int) else cell for cell in row))
            if i < 2:
                print("-" * 9)


def play_game():
    matrix = initialize_game()
    for i in range(3):
        row = matrix[i * 3: i * 3 + 3]
        print(" | ".join(str(cell) if isinstance(cell, int) else cell for cell in row))
        if i < 2:
            print("-" * 9)
    while not is_game_over(matrix)[0]:
        if matrix[9] == 'A':
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
