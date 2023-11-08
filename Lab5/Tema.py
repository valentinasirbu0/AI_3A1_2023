def is_valid_choice(instance, number):
    if number not in instance:
        return False
    return True


def assign_number_to_player(instance, player, number):
    player.append(number)
    instance.remove(number)


def find_winner(player1, player2):
    if len(player1) == 3 and sum(player1) == 15:
            return "Player1"
    if len(player2) == 3 and sum(player2) == 15:
            return "Player2"
    elif len(player1) + len(player2) == 9:
        return "Remiza"
    return "Continue"


def game():
    player1 = []  # player 0
    player2 = []  # player 1
    instance = list(number for number in range(1, 10))
    current_player = 0

    while find_winner(player1, player2) == "Continue":
        player_input = input(f"Player{current_player + 1}: ")
        if is_valid_choice(instance, int(player_input)):
            if current_player:
                assign_number_to_player(instance, player2, int(player_input))
                print(player2)
            else:
                assign_number_to_player(instance, player1, int(player_input))
                print(player1)
            current_player = not current_player
        else:
            print("Make another choice")

    return find_winner(player1, player2)


print("The winner is: ", game())
