def set_initial_domains(instance):
    domains = {}
    for i in range(9):
        for j in range(9):
            if instance[i][j] == 0:
                domains[(i, j)] = set(range(1, 10))
            elif instance[i][j] == -1:
                domains[(i, j)] = set([2, 4, 6, 8])
            else:
                domains[(i, j)] = set([instance[i][j]])
    return domains


def is_completed(state):
    for i in range(9):
        for j in range(9):
            if state[i][j] == 0:
                return False
    return True


def next_empty_cell(state):
    for i in range(9):
        for j in range(9):
            if state[i][j] == 0 or state[i][j] == -1:
                return (i, j)
    return None


def is_valid(state, cell, value):
    row, col = cell

    if state[row][col] == -1 and value % 2 == 1:
        return False

    for i in range(9):
        if state[i][col] == value:
            return False

    for j in range(9):
        if state[row][j] == value:
            return False

    start_row = row - row % 3
    start_column = col - col % 3
    for i in range(3):
        for j in range(3):
            if state[i + start_row][j + start_column] == value:
                return False

    return True


def update_domains(domains, var, value):
    new_domains = domains.copy()

    row, col = var
    for i in range(9):
        new_domains[(row, i)].discard(value)
        new_domains[(i, col)].discard(value)

    box_row, box_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            if (i, j) != var:
                new_domains[(i, j)].discard(value)

    return new_domains


def bkt_with_fc(state, domains):
    if is_completed(state):
        return state

    cell = next_empty_cell(state)
    if cell is None:
        return None

    row, col = cell
    for value in range(1, 10):
        if is_valid(state, cell, value):
            new_state = [row[:] for row in state]
            new_state[row][col] = value
            new_domains = update_domains(domains, cell, value)

            if all(new_domain for new_domain in new_domains):
                res = bkt_with_fc(new_state, new_domains)
                if res is not None:
                    return res

    return None


def get_empty_cells(state):
    empty_cells = []
    for i in range(9):
        for j in range(9):
            if state[i][j] == 0 or state[i][j] == -1:
                empty_cells.append((i, j))
    return empty_cells


def next_cell_mrv(state, domains):
    empty_cells = get_empty_cells(state)

    if not empty_cells:
        return None

    min_cell = None
    min_values = float('inf')

    for cell in empty_cells:
        values = domains[cell]
        if len(values) < min_values:
            min_cell = cell
            min_values = len(values)

    return min_cell


def bkt_with_fc_mrv(state, domains):
    if is_completed(state):
        return state

    cell = next_cell_mrv(state, domains)
    if cell is None:
        return None

    row, col = cell
    for value in range(1, 10):
        if is_valid(state, cell, value):
            new_state = [row[:] for row in state]
            new_state[row][col] = value
            new_domains = update_domains(domains, cell, value)

            if all(new_domain for new_domain in new_domains):
                res = bkt_with_fc_mrv(new_state, new_domains)
                if res is not None:
                    return res

    return None


def print_solution(solution):
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("-" * 21)
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")
            print(solution[i][j], end=" ")
        print()


instance = [
        [8, 4, 0, 0, 5, 0, -1, 0, 0],
        [3, 0, 0, 6, 0, 8, 0, 4, 0],
        [0, 0, -1, 4, 0, 9, 0, 0, -1],
        [0, 2, 3, 0, -1, 0, 9, 8, 0],
        [1, 0, 0, -1, 0, -1, 0, 0, 4],
        [0, 9, 8, 0, -1, 0, 1, 6, 0],
        [-1, 0, 0, 5, 0, 3, -1, 0, 0],
        [0, 3, 0, 1, 0, 6, 0, 0, 7],
        [0, 0, -1, 0, 2, 0, 0, 1, 3]
    ]

initial_domains = set_initial_domains(instance)

solution_fc = bkt_with_fc(instance, initial_domains)
solution_fc_mrv = bkt_with_fc_mrv(instance, initial_domains)

print("Forward Checking:" )
if solution_fc:
    print_solution(solution_fc)
else:
    print("No solution found.")

print("\nMRV:")
if solution_fc_mrv:
    print_solution(solution_fc)
else:
    print("No solution found.")














