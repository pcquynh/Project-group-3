import random
def display_menu():
    # todo: need to add the game rules
    print("Welcome to NL Casino")
    print("BlackJack game rule: ")


def get_player_list():
    player_list = []
    player_number = int(input("How many player? "))
    while True:
        player = []
        bet = 0
        player_hand = []
        name = input("Enter player name: ")
        balance = float(input("Enter balance amount: "))
        player.append(name)
        player.append(balance)
        player.append(bet)
        player.append(player_hand)
        player_list.append(player)
        if len(player_list) > player_number - 1:
            break
    return player_list


def give_card(deck):
    hand = []
    for i in range(2):
        random.shuffle(deck)
        card = deck.pop(0)
        if card == 11: card = "J"
        if card == 12: card = "Q"
        if card == 13: card = "K"
        if card == 14: card = "A"
        hand.append(card)
    return hand


def show_card(hand):
    s = ""
    for card in hand:
        s = s + " " + str(card)
    print("[" + s + " ]")


# todo: need to add exception handling for bet input
def place_bet(player):
    player_balance = player[1]
    while True:
        bet = float(input("Enter amount of bet (min 5, max 500) for " + player[0] + "\t"))
        if bet > player_balance:
            print("The bet should be smaller than the balance")
            continue
        else:
            return bet


def stand_card(hand):
    return hand


def hit_card(deck, hand, role):
    random.shuffle(deck)
    card = deck.pop(0)
    if card == 11: card = "J"
    if card == 12: card = "Q"
    if card == 13: card = "K"
    if card == 14: card = "A"
    hand.append(card)
    print(role, " got", card)
    return hand


def count_score_without_ace(hand):
    score = 0
    for card in hand:
        if card == "J" or card == "Q" or card == "K":
            score += 10
        elif card != "A":
            score += card
    return score


def count_score(hand):
    score = count_score_without_ace(hand)
    for card in hand:
        if card == "A":
            if score >= 11:
                score += 1
            else:
                score += 11
    return score


def is_back_jack(hand):
    if len(hand) == 2:
        if count_score(hand) == 21:
            return True
    return False


def print_result(player,dealer_hand):
    player_balance = player[1]
    bet = player[2]
    player_hand = player[3]

    if is_back_jack(dealer_hand):
        if is_back_jack(player_hand):
            print(player[0] + " and Dealer all have Blackjack")
            print(player[0] + " balance is: "+ player_balance)
        else:
            player_balance -= bet
            print("Dealer has Blackjack." + player[0] + " lost bet.")
            print(player[0] + " balance is: "+ player_balance)
            player[1] = player_balance
    elif is_back_jack(player_hand):
        show_card(player_hand)
        player_balance += 1.5 * bet
        print(player[0] + " has Blackjack. " + player[0] + " win bet.")
        print(player[0] + " balance is: " + player_balance)
        player[1] = player_balance
    elif count_score(dealer_hand) == count_score(player_hand) <= 21:
        print(player[0] + " and Dealer have the same score.")
        print(player[0] + " balance is: " + player_balance)
    elif count_score(dealer_hand) < count_score(player_hand) <= 21:
        player_balance += bet
        print(player[0] + " win bet.")
        print(player[0] + " balance is: " + player_balance)
        player[1] = player_balance
    elif count_score(player_hand) < count_score(dealer_hand) <= 21:
        player_balance -= bet
        print(player[0] + " lost bet.")
        print(player[0] + " balance is: " + player_balance)
        player[1] = player_balance
    elif count_score(dealer_hand) > 21 and count_score(player_hand) <= 21:
        player_balance += bet
        print("Dealer is bust. "+ player[0] + " win bet.")
        print(player[0] + " balance is: " + player_balance)
        player[1] = player_balance
    elif count_score(player_hand) > 21 and count_score(dealer_hand) <= 21:
        player_balance -= bet
        print(player[0] + " is bust. " + player[0] + " lost bet.")
        print(player[0] + " balance is: " + player_balance)
        player[1] = player_balance
    else:
        print("Player and Dealer are bust.")
        print(player[0] + " balance is: " + player_balance)


def reset_player_list(player_list):
    for player in player_list:
        player[2] = 0
        player[3] = []


def play_game(player_list):
    choice = "y"
    while choice.lower() == "y":
        reset_player_list(player_list)
        dealer_hand = []
        deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14] * 4
        for player in player_list:
            player_balance = player[1]
            if player_balance < 5:
                print("Your balance is not enough. Bye!")
                break
            # todo: add suite to the deck
            bet = place_bet(player)
            player[2] = bet
            player_hand = give_card(deck)
            player[3] = player_hand
            print(player[0] + " cards are:")
            show_card(player_hand)
            player_score = count_score(player_hand)
            dealer_hand = give_card(deck)
            dealer_score = count_score(dealer_hand)

            if is_back_jack(player_hand):
                continue
            else:
                # PLAYER
                while player_score <= 21:
                    choice = input("Do you want to stand or hit ? (S or H): ")
                    if choice.upper() == "S":
                        stand_card(player_hand)
                        print(player[0] + " cards are:")
                        show_card(player_hand)
                        player[3] = player_hand
                        break
                    else:
                        hit_card(deck, player_hand, player[0])
                        player_score = count_score(player_hand)
                        print(player[0] + " cards are:")
                        show_card(player_hand)
                        player[3] = player_hand
                # DEALER
        print("Dealer cards are:")
        print(dealer_hand[0])
        print("?")
        if dealer_score >= 16:
            show_card(dealer_hand)
        else:
            while dealer_score < 16:
                hit_card(deck, dealer_hand, "Dealer")
                print("Dealer cards are:")
                show_card(dealer_hand)
                dealer_score = count_score(dealer_hand)
        for player in player_list:
            print_result(player, dealer_hand)

        print()
        choice = input("Do you want to play again? (y/n) : ")

    print("Bye!")


def main():
    player_list = get_player_list()
    play_game(player_list)


if __name__ == '__main__':
    main()
