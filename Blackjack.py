import random
def display_menu():
    # todo: need to add the game rules
    print("Welcome to NL Casino")
    print("BlackJack game rule: ")


def player_info():
    player = []
    name = input("Enter player name: ")
    balance = float(input("Enter balance amount: "))
    while True:
        try:
            age = int(input("Enter player age: "))
        except ValueError:
            print("Invalid age. Please enter again.")
            continue
        if age < 18:
            print("You are not allowed to play this game.")
        else:
            player.append(name)
            player.append(balance)
            player.append(age)
            break
    return player


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
def place_bet():
    while True:
        bet = float(input("Enter amount of bet (min 5, max 500): "))
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
            if score > 11:
                score += 1
            else:
                score += 11
    return score


def is_back_jack(hand):
    if len(hand) == 2:
        if count_score(hand) == 21:
            return True
    return False


def print_result(player_hand, dealer_hand, bet):
    global player_balance
    if is_back_jack(dealer_hand):
        if is_back_jack(player_hand):
            print("Player and Dealer all have Blackjack")
            print("Player balance is: ", player_balance)
        else:
            player_balance -= bet
            print("Dealer has Blackjack. Player lost bet.")
            print("Player balance is: ", player_balance)
    elif is_back_jack(player_hand):
        player_balance += 1.5 * bet
        print("Player has Blackjack. Player win bet.")
        print("Player balance is: ", player_balance)
    elif count_score(dealer_hand) == count_score(player_hand) <= 21:
        print("Player and Dealer have the same score.")
        print("Player balance is: ", player_balance)
    elif count_score(dealer_hand) < count_score(player_hand) <= 21:
        player_balance += bet
        print("Player win bet.")
        print("Player balance is: ", player_balance)
    elif count_score(player_hand) < count_score(dealer_hand) <= 21:
        player_balance -= bet
        print("Player lost bet.")
        print("Player balance is: ", player_balance)
    elif count_score(dealer_hand) > 21 and count_score(player_hand) <= 21:
        player_balance += bet
        print("Dealer is bust. Player win bet.")
        print("Player balance is: ", player_balance)
    elif count_score(player_hand) > 21 and count_score(dealer_hand) <= 21:
        player_balance -= bet
        print("Player is bust. Player lost bet.")
        print("Player balance is: ", player_balance)
    else:
        print("Player and Dealer are bust.")
        print("Player balance is: ", player_balance)


def play_game():
    choice = "y"
    while choice.lower() == "y":
        if player_balance < 5:
            print("Your balance is not enough. Bye!")
            break
        # todo: add suite to the deck
        deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14] * 4
        bet = place_bet()
        player_hand = give_card(deck)
        print("Player cards are:")
        show_card(player_hand)
        dealer_hand = give_card(deck)
        print("Dealer cards are:")
        print(dealer_hand[0])
        print("?")
        player_score = count_score(player_hand)
        dealer_score = count_score(dealer_hand)

        if is_back_jack(player_hand) or is_back_jack(dealer_hand):
            print_result(player_hand, dealer_hand, bet)
            choice = input("Do you want to play again? (y/n) : ")
            if choice.lower() != "y":
                print("Bye!")
        else:
            # PLAYER
            # todo: modify player function related to score
            while player_score <= 21:
                if player_score < 16:
                    hit_card(deck, player_hand, "Player")
                    print("Player cards are:")
                    show_card(player_hand)
                    player_score = count_score(player_hand)
                else:
                    choice = input("Do you want to stand or hit ? (S or H): ")
                    if choice.upper() == "S":
                        stand_card(player_hand)
                        print("Player cards are:")
                        show_card(player_hand)
                        break
                    else:
                        hit_card(deck, player_hand, "Player")
                        player_score = count_score(player_hand)
                        print("Player cards are:")
                        show_card(player_hand)
            # DEALER
            while dealer_score < 16:
                hit_card(deck, dealer_hand, "Dealer")
                print("Dealer cards are:")
                show_card(dealer_hand)
                dealer_score = count_score(dealer_hand)

            print_result(player_hand, dealer_hand, bet)
            choice = input("Do you want to play again? (y/n) : ")
            if choice.lower() != "y":
                print("Bye!")


def main():
    global player_balance
    player = player_info()
    player_balance = player[1]
    play_game()


if __name__ == '__main__':
    main()
