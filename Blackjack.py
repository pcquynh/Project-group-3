import random

global casino_bank
casino_bank = 0

# prints games rules
def display_menu():
    print("-----Welcome to NL Casino!-----")

    print()
    choice = input("What you like to see the rules? (y/n) ")
    while choice == "y":
        print("BlackJack game rules: ")
        print("\u2660 Each participant attempts to beat the dealer by getting a count as close to 21 as possible, without going over 21.")
        print("\u2665 Face cards (Jack, Queen and King) have a value of 10. Any other card is its face value.")
        print("\u2666 Aces are worth 1 or 11. The during game play, an Ace will change value to give the player the best hand.")
        print("\u2663 Before the round begins, each player places a bet. Minimum and maximum limits are $5 to $1000.")
        print("\u2660 A player must choose to 'stand' (not ask for another card) or 'hit' (ask for another card to get closer to a count of 21, or even hit 21 exactly).")
        break
    print()
    print("Let get started!")

#creates list of players for the game
def get_player_list():
    player_list = []
    age = input("Please confirm the age of all players is over 18 (y/n): ")
    while age.lower() != "y":
        age = input("Please confirm the age of all players is over 18 (y/n): ")
    player_number = int(input("How many players? "))
    print()
    i = 1
    while True:
        player = []
        bet = 0
        player_hand = []
        try:
            balance = int(input(f"Enter Player {i}'s balance: "))
        except ValueError:
            print("Please enter a valid integer")
            continue
        name = input(f"Enter player {i}'s name: ")
        print()
        player.append(name)
        player.append(balance)
        player.append(bet)
        player.append(player_hand)
        player_list.append(player)
        i += 1
        if len(player_list) > player_number - 1:
            break
    return player_list

#generates the hand for the dealer and players
def give_card(deck):
    hand = []
    for i in range(2):
        random.shuffle(deck)
        card = deck.pop(0)
        hand.append(card)
    return hand

#displays players hand
def show_card(player_hand):
    s = ""
    for card in player_hand:
        s = s + " " + str(card)
    print("[" + s + " ]")

#receive input for player bets
def place_bet(player):
    player_balance = player[1]
    while True:
        try:
            bet = int(input(f"{player[0]} - Enter amount of bet (min 5, max 1000):  "))
        except ValueError:
            print("You must enter a valid number")
            continue
        print()
        if bet > player_balance:
            print("The bet should be smaller than the balance")
            continue
        elif bet < 5 or bet > 1000:
            print("Bet must be between 5 and 1000.\n")
            continue
        else:
            return bet

def stand_card(hand):
    return hand

#generates random card for dealer or players
def hit_card(deck, hand, role):
    random.shuffle(deck)
    card = deck.pop(0)
    hand.append(card)
    print(role, " got", card)
    return hand

#evaluates total score for dealer or player's hand
def count_score_without_ace(hand):
    score = 0
    for card in hand:
        if card == "J" or card == "Q" or card == "K":
            score += 10
        elif card != "A":
            score += card
    return score

#evaluates total score for dealer or player's hand
def count_score(hand):
    score = count_score_without_ace(hand)
    for card in hand:
        if card == "A":
            if score >= 11:
                score += 1
            else:
                score += 11
    return score

#checking if dealer and player have blackjack
def is_back_jack(hand):
    if len(hand) == 2:
        if count_score(hand) == 21:
            return True
    return False

#determines wins and loses and allocates payout for bets
#tracks house money
def print_result(player, dealer_hand):
    global casino_bank
    player_balance = player[1]
    bet = player[2]
    player_hand = player[3]
    if is_back_jack(dealer_hand):
        if is_back_jack(player_hand):
            print(player[0] + " and Dealer all have Blackjack")
            print(player[0] + "'s balance is: ", player_balance)
            casino_bank = casino_bank
        else:
            player_balance -= bet
            print("Dealer has Blackjack." + player[0] + " lost bet.")
            print(player[0] + "'s balance is: ", player_balance)
            player[1] = player_balance
            casino_bank += bet
    elif is_back_jack(player_hand):
        show_card(player_hand)
        player_balance += 1.5 * bet
        print(player[0] + " has Blackjack. " + player[0] + " win bet.")
        print(player[0] + "'s balance is: ", player_balance)
        casino_bank -= 1.5 * bet
        player[1] = player_balance
    elif count_score(dealer_hand) == count_score(player_hand) <= 21:
        print(player[0] + " and Dealer have the same score.")
        print(player[0] + "'s balance is: ", player_balance)
    elif count_score(dealer_hand) < count_score(player_hand) <= 21:
        player_balance += bet
        print(player[0] + " win bet.")
        print(player[0] + " balance is: ", player_balance)
        player[1] = player_balance
        casino_bank -= bet
    elif count_score(player_hand) < count_score(dealer_hand) <= 21:
        player_balance -= bet
        print(player[0] + " lost bet.")
        print(player[0] + "'s balance is: ", player_balance)
        player[1] = player_balance
        casino_bank += bet
    elif count_score(dealer_hand) > 21 and count_score(player_hand) <= 21:
        player_balance += bet
        print("Dealer is bust. "+ player[0] + " win bet.")
        print(player[0] + "'s balance is: ", player_balance)
        player[1] = player_balance
        casino_bank -= bet
    elif count_score(player_hand) > 21 and count_score(dealer_hand) <= 21:
        player_balance -= bet
        print(player[0] + " is bust. " + player[0] + " lost bet.")
        print(player[0] + "'s balance is: ", player_balance)
        player[1] = player_balance
        casino_bank += bet
    else:
        print(player[0] + " and Dealer are bust.")
        player_balance -= bet
        print(player[0] + "'s balance is: ", player_balance)
        casino_bank += bet

def reset_player_list():
    global player_list
    for player in player_list:
        player[2] = 0
        player[3] = []

#deals cards, calculates points and prompts user to hit or stand
def play_game():
    global player_list
    choice = "y"
    while choice.lower() == "y":
        reset_player_list()
        dealer_hand = []
        deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K", "A"] * 4

        #give_card(deck, player_list)
        new_player_list = []
        for player in player_list:
            player_balance = player[1]
            if player_balance < 5:
                print(f"{player[0]}'s balance is not enough. Bye!")
                print(f"{player[0]} was removed.")
                continue
            new_player_list.append(player)
        player_list = new_player_list

        if len(player_list) == 0:
            print("There are no players at the table.")
            print("Please add players.\n")
            break

        print("====Blackjack====")
        for player in player_list:
            bet = place_bet(player)
            player[2] = bet
        for player in player_list:
            player_hand = give_card(deck)
            player[3] = player_hand
            print(player[0] + " cards are:")
            show_card(player_hand)
            player_score = count_score(player_hand)
            print(f"{player[0]}'s score is: {player_score}")
            print()
        dealer_hand = give_card(deck)
        dealer_score = count_score(dealer_hand)
        print("Dealer cards are:")
        print(f"[ {dealer_hand[0]} ? ]")
        print("===============")

        for player in player_list:
            player_hand = player[3]
            player_score = count_score(player_hand)
            if is_back_jack(player_hand):
                continue
                # PLAYER
                #continues prompting the player as long as player has 21 or more.
            else:
                while player_score <= 21:
                    player_score = count_score(player_hand)
                    print(f"{player[0]}'s score is: {player_score}")
                    print(player[0] + " cards are:")
                    show_card(player_hand)
                    choice = input(f"{player[0]} - Do you want to stand or hit ? (S or H): ")
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
                        print()
                    # DEALER
                print()
                print("============NEXT PLAYER=============")

        print("Dealer cards are:")
        print(*dealer_hand)
        dealer_score = count_score(dealer_hand)
        print(f"Dealer's Score is {dealer_score}")

        if dealer_score > 16:
            show_card(dealer_hand)
        else:
            while dealer_score <= 16:
                print("Dealer must hit!")
                hit_card(deck, dealer_hand, "Dealer")
                print("Dealer cards are:")
                show_card(dealer_hand)
                dealer_score = count_score(dealer_hand)
        print(f"Dealer score is {dealer_score}")
        print()
        print("===========RESULTS===========")
        for player in player_list:
            print_result(player, dealer_hand)

        print()
        choice = input("Do you want to continue playing? (y/n): ")

def main():
    global casino_bank
    global player_list
    choice = "y"
    while choice =="y":
        display_menu()
        player_list = get_player_list()
        play_game()
        choice = input("Do you want to play a new game?(y/n) ")
    print("Bye!")
    print(f"Casino Bank Account Balance: ${casino_bank}")
    #writes the changes in house money
    with open("Casino_Bank.txt", "w") as file:
        file.write("Casino Bank Account Balance:"+"\n")
        file.write(str(casino_bank))

if __name__ == '__main__':
    main()
