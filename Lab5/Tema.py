def is_valid_choice(instance, number):
    if number not in instance:
        return False
    return True


def assign_number_to_player(instance, player, number):
    player.append(number)
    instance.remove(number)


def find_winner(player1, player2):
    combinations = find_combinations(list(number for number in range(1, 10)))
    for comb in combinations:
        if set(comb) <= set(player1):
            return "Human"
        if set(comb) <= set(player2):
            return "Algo"

    if len(player1) + len(player2) == 9:
        return "Remiza"
    else:
        return "Continue"


def find_combinations(numbers, partial=[]):
    if len(partial) == 3 and sum(partial) == 15:
        yield partial
    if len(partial) >= 3 or sum(partial) >= 15:
        return
    for i in range(len(numbers)):
        remaining = numbers[i+1:]
        yield from find_combinations(remaining, partial + [numbers[i]])


def two_moves_ahead(instance, player_chosen):
    acceptable = []
    possibilities = add_numbers_to_set_to_sum_to_15(player_chosen, 9)
    for pos in possibilities:
        if (set(pos) - set(player_chosen)) <= set(instance):
            acceptable.append(pos)
    return acceptable


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


def find_heuristic_number(instance, algo_choices, human_choices):
    if is_valid_choice(instance, 5):
        return 5

    human_posibilities = two_moves_ahead(instance, human_choices)
    print("Human can choose between: ", human_posibilities)

    algo_posibilities = two_moves_ahead(instance, algo_choices)
    print("Algo can choose from: ", algo_posibilities)

    for algo_set in algo_posibilities:
        if set(algo_choices) <= set(algo_set) and len(algo_choices) + 1 == len(algo_set):
            print("One move until win")
            print("Algo has: ", algo_choices)
            print("Algo wants: ", algo_set)
            diff = int(''.join(map(str, set(algo_set) - set(algo_choices))))
            print("Algo needs: ", diff)
            print("Instance: ", instance)
            if is_valid_choice(instance, diff):
                return diff

    for hum_set in human_posibilities:
        if set(algo_choices) <= set(hum_set) and len(algo_choices) + 1 == len(hum_set):
            print("One move until win")
            print("We have: ", algo_choices)
            print("We want: ", hum_set)
            diff = int(''.join(map(str, set(hum_set) - set(algo_choices))))
            print("We need: ", diff)
            print("Instance: ", instance)
            if is_valid_choice(instance, diff):
                return diff

    a = {}
    for h_choice in human_posibilities:
        for a_choice in algo_posibilities:
            h_choice_set = set(h_choice)
            a_choice_set = set(a_choice)

            intersection = h_choice_set.intersection(a_choice_set)
            if intersection:
                for number in intersection:
                    if number in a:
                        a[number] += 1
                    else:
                        a[number] = 1
    if len(a) > 0:
        print("Possible choices for algo solution length ", len(a), "are ", a)
        sorted_choices = sorted(a, key=lambda k: (-a[k], k)) #sortam dupa valoare

        for key in sorted_choices:
            if is_valid_choice(instance, key):
                return key
    else:
        for i in range(1, 10):
            if is_valid_choice(instance, i):
                return i


def game():
    player1 = []  # player 0 alg
    player2 = []  # player 1 om
    instance = list(number for number in range(1, 10))
    current_player = 0

    while find_winner(player1, player2) == "Continue":
        if not current_player:
            player_input = input("Human choose : ")
            if is_valid_choice(instance, int(player_input)):
                assign_number_to_player(instance, player1, int(player_input))
                print("Human choices: ", player1)
                current_player = not current_player
            else:
                print("Make another choice")
        else:
            number = find_heuristic_number(instance, player2, player1)
            assign_number_to_player(instance, player2, number)
            print("Algo chose :", number)
            print("Algo choices : ", player2)
            current_player = not current_player

    return find_winner(player1, player2)


print("The winner is: ", game())

