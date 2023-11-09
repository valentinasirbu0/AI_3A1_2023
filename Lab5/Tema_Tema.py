magic_square = [
    [8, 1, 6],
    [3, 5, 7],
    [4, 9, 2],
]


def initialize_game():
    return [8, 1, 6, 3, 5, 7, 4, 9, 2, 'A']


def is_game_over(state):
    def check_winner(player):
        for i in range(3):
            if state[i * 3: i * 3 + 3].count(player) == 3 or state[i:9:3].count(player) == 3:
                return True, player
        if state[0:9:4].count(player) == 3 or state[2:7:2].count(player) == 3:
            return True, player
        return False, None

    for player in ['A', 'B']:
        result, winner = check_winner(player)
        if result:
            return True, winner

    if all(isinstance(cell, int) for cell in state):
        return True, 'remiza'

    return False, None


def is_valid_move(state, number):
    return number in state


def make_move(state, number):
    if not is_valid_move(state, number):
        return None
    pos = state.index(number)
    new_state = state.copy()
    new_state[pos] = state[9]
    new_state[9] = 'A' if state[9] == 'B' else 'B'
    return new_state


def evaluate_board(state):
    if is_game_over(state)[0]:
        if is_game_over(state)[1] == 'A':
            return 100
        elif is_game_over(state)[1] == 'B':
            return -100
        else:
            return 0
    value = 0
    for i in range(3):
        if state[i * 3: i * 3 + 3].count('A') > 0 and state[i * 3: i * 3 + 3].count('B') == 0:
            value += state[i * 3: i * 3 + 3].count('A') ** 2
        if state[i * 3: i * 3 + 3].count('B') > 0 and state[i * 3: i * 3 + 3].count('A') == 0:
            value -= state[i * 3: i * 3 + 3].count('B') ** 2
        if state[i:9:3].count('A') > 0 and state[i:9:3].count('B') == 0:
            value += state[i:9:3].count('A') ** 2
        if state[i:9:3].count('B') > 0 and state[i:9:3].count('A') == 0:
            value -= state[i:9:3].count('B') ** 2
    if state[0:9:4].count('A') > 0 and state[0:9:4].count('B') == 0:
        value += state[0:9:4].count('A') ** 2
    if state[0:9:4].count('B') > 0 and state[0:9:4].count('A') == 0:
        value -= state[0:9:4].count('B') ** 2
    if state[2:7:2].count('A') > 0 and state[2:7:2].count('B') == 0:
        value += state[2:7:2].count('A') ** 2
    if state[2:7:2].count('B') > 0 and state[2:7:2].count('A') == 0:
        value -= state[2:7:2].count('B') ** 2
    return value


def generate_possible_moves(state):
    return [make_move(state, i + 1) for i in range(9) if is_valid_move(state, i + 1)]


def minimax(depth, state):
    if is_game_over(state)[0] or depth == 0:
        return state, evaluate_board(state)

    if state[9] == 'B':
        possible_moves = generate_possible_moves(state)
        best_value = float('inf')
        best_state = state
        for move in possible_moves:
            _, value = minimax(depth - 1, move)
            if value < best_value:
                best_value = value
                best_state = move
        return best_state, best_value

    if state[9] == 'A':
        possible_moves = generate_possible_moves(state)
        best_value = float('-inf')
        best_state = state
        for move in possible_moves:
            _, value = minimax(depth - 1, move)
            if value > best_value:
                best_value = value
                best_state = move
        return best_state, best_value


def display_board(state):
    if state is not None:
        player = 'Player B: ' if state[9] == 'B' else 'Player A: '
        print(player)
        for i in range(3):
            row = state[i * 3: i * 3 + 3]
            print(" | ".join(str(cell) if isinstance(cell, int) else cell for cell in row))
            if i < 2:
                print("-" * 9)


def play_game():
    state = initialize_game()
    for i in range(3):
        row = state[i * 3: i * 3 + 3]
        print(" | ".join(str(cell) if isinstance(cell, int) else cell for cell in row))
        if i < 2:
            print("-" * 9)
    while not is_game_over(state)[0]:
        if state[9] == 'A':
            number = int(input("Your move: "))
            new_state = make_move(state, number)
            display_board(new_state)
            if new_state is None:
                print("Invalid number!")
                continue
            state = new_state
        else:
            new_state, _ = minimax(3, state)
            state = new_state
            display_board(state)
    print(is_game_over(state))

play_game()
