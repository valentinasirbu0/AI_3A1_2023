import numpy as np
import matplotlib.pyplot as plt


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


def plot_rewards(episode_numbers, rewards):
    plt.figure(figsize=(10, 5))
    plt.bar(episode_numbers, rewards, color='blue', alpha=0.7, label='Total Reward per Episode')
    plt.axhline(np.mean(rewards), color='red', linestyle='dashed', linewidth=2, label='Mean Reward')

    plt.title('Convergence of Q-learning Algorithm')
    plt.xlabel('Episode')
    plt.ylabel('Total Reward')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.show()


def train(episodes, epsilon, alpha, gamma, q_table, initial_state):
    rewards = []

    for episode in range(episodes):
        total_reward = 0

        current_state = initial_state

        while current_state != goal:
            action = choose_action(q_table, current_state, epsilon)
            next_state_val = next_state(current_state, action)
            if next_state_val == goal:
                reward = 100
            else:
                reward = -1
            total_reward += reward

            q_table[current_state[0], current_state[1], action] += alpha * (
                    reward + gamma * np.max(q_table[
                                                max(min(next_state_val[0], rows - 1), 0),
                                                max(min(next_state_val[1], columns - 1), 0)
                                            ]) - q_table[current_state[0], current_state[1], action])

            current_state = next_state_val

        rewards.append(total_reward)

    print(rewards)
    return rewards


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

    rewards = train(num_episodes, epsilon, alpha, gamma, q_table, start)

    i = rows - 1
    for row in q_table:
        print("Randul ", i)
        i -= 1
        print(row)

    print_policy(q_table)

    episode_numbers = np.arange(1, num_episodes + 1)
    plot_rewards(episode_numbers, rewards)


if __name__ == "__main__":
    rows = 7
    columns = 10
    start = (3, 0)
    goal = (3, 7)
    main()
