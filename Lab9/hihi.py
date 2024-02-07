import numpy as np


def initialize():
    return np.zeros((rows, columns, 4))


def next_state(initial_state, action):
    initial_row, initial_column = initial_state
    wind_impact = [0, 0, 0, 1, 1, 1, 2, 2, 1, 0]

    if action == 0:  # up
        final_row = max(0, initial_row - 1 - wind_impact[initial_column])
        final_column = initial_column
    elif action == 1:  # down
        final_row = min(rows - 1, initial_row + 1 - wind_impact[initial_column])
        final_column = initial_column
    elif action == 2:  # left
        final_row = max(0, initial_row - wind_impact[initial_column])
        final_column = max(0, initial_column - 1)
    elif action == 3:  # right
        final_row = max(0, initial_row - wind_impact[initial_column])
        final_column = min(columns - 1, initial_column + 1)
    return (final_row, final_column)


def choose_action(q_table, state, epsilon=0.1):
    if np.random.uniform(0, 1) < epsilon:
        return np.random.choice(4)
    else:
        return np.argmax(q_table[state[0], state[1]])


def train(episodes, epsilon, alpha, gamma, q_table, current_state):
    for episode in range(episodes):
        while current_state != goal:
            action = choose_action(q_table, current_state, epsilon)
            next_state_val = next_state(current_state, action)
            reward = -1
            q_table[current_state[0], current_state[1], action] += alpha * (
                    reward + gamma * np.max(q_table[next_state_val[0], next_state_val[1]]) - q_table[
                current_state[0], current_state[1], action])

            current_state = next_state_val


def print_policy(Q):
    print(" ")
    policy = np.argmax(Q, axis=2)
    actions_map = {0: '↑', 1: '↓', 2: '←', 3: '→'}

    for row in range(rows):
        for col in range(columns):
            if (row, col) == goal:
                print(' G ', end='')
            elif (row, col) == start:
                print(' S ', end='')
            else:
                action = actions_map[policy[row, col]]
                print(f' {action} ', end='')
        print()


def main():
    alpha = 0.9
    gamma = 0.9
    epsilon = 0.1
    num_episodes = 200

    q_table = initialize()
    print("Q-table:")

    train(num_episodes, epsilon, alpha, gamma, q_table, start)

    i = rows - 1
    for row in q_table:
        print("Randul ", i)
        i -= 1
        print(row)

    print_policy(q_table)


if __name__ == "__main__":
    rows = 7
    columns = 10
    start = (3, 0)
    goal = (3, 7)
    main()
