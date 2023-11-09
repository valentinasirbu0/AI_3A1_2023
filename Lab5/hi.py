def add_numbers_to_set_to_sum_to_15(numbers_set, max_number_to_add):
    possibilities = set()

    def find_combinations_recursive(current_combination, remaining_list, target_sum):
        if sum(current_combination) == target_sum:
            possibilities.add(tuple(sorted(current_combination)))

        if sum(current_combination) >= target_sum:
            return

        for number in remaining_list:
            new_combination = current_combination + [number]
            new_remaining = [x for x in remaining_list if x >= number]
            find_combinations_recursive(new_combination, new_remaining, target_sum)

    target_sum = 15
    find_combinations_recursive(list(numbers_set), list(range(1, max_number_to_add + 1)), target_sum)
    return possibilities

# Example usage:
input_set = {5, 4}
max_number_to_add = 10  # You can change this to any desired maximum number to add
possibilities = add_numbers_to_set_to_sum_to_15(input_set, max_number_to_add)

for possibility in possibilities:
    print(possibility)
