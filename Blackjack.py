import random
def display_menu():


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


def count_score_without_ace():


def count_score():


def is_blackjack():


def play_game():

    
def print_result():


def main():


if __name__ == '__main__':
    main()