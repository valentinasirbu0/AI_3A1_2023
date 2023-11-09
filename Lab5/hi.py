def add_numbers_to_set_to_sum_to_15(numbers_set, max_number):
    possibilities = set()

    def find_combinations_recursive(current_combination, remaining_list):
        if len(current_combination) >= 3:
            if sum(current_combination) == 15:
                possibilities.add(tuple(current_combination))
            return

        for number in range(1, max_number + 1):
            if number not in current_combination and number not in numbers_set:
                new_combination = current_combination + [number]
                find_combinations_recursive(new_combination, remaining_list)

    find_combinations_recursive(list(numbers_set), list(numbers_set))
    return possibilities

# Example usage:
input_set = {5 , 4}
max_number_to_add = 10  # You can change this to any desired maximum number to add
possibilities = add_numbers_to_set_to_sum_to_15(input_set, max_number_to_add)

for possibility in possibilities:
    print(possibility)
