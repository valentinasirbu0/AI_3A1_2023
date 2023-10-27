import math


def euclidean_distance_for_target(board, target):
    distance = 0
    for i in range(3):
        for j in range(3):
            value = board[i][j]
            if value != 0:  # Skip the empty cell
                target_i, target_j = divmod(value - 1, 3)
                distance += math.sqrt((i - target_i) ** 2 + (j - target_j) ** 2)
    return distance


def generate_all_targets():
    lst = list(range(1, 9))
    all_inserted = []
    for i in range(len(lst) + 1):
        new_lst = lst[:i] + [0] + lst[i:]
        all_inserted.append(new_lst)
    all_targets = [[new_lst[i:i + 3] for i in range(0, 9, 3)] for new_lst in all_inserted]
    return all_targets


def euclid(board):
    return min(euclidean_distance_for_target(board, target) for target in generate_all_targets())




#print(euclidean_distance(matrix))
