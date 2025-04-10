import random

# Define the deck of cards
cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
card_values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}

# Function to deal a card
def deal_card():
    return random.choice(cards)

# Function to calculate the score of a hand
def calculate_score(hand):
    score = 0
    aces = 0  # Track number of aces
    for card in hand:
        score += card_values[card]
        if card == 'A':  # Count Aces
            aces += 1

    # Adjust score if it's over 21 and we have aces (treat ace as 1 instead of 11)
    while score > 21 and aces:
        score -= 10  # Subtract 10 to make Ace count as 1
        aces -= 1  # One less Ace

    return score

# Function to compare player and computer scores
def compare(player_score, computer_score):
    if player_score > 21:
        return "You went over. You lose!"
    elif computer_score > 21:
        return "Computer went over. You win!"
    elif player_score > computer_score:
        return "You win!"
    elif computer_score > player_score:
        return "Computer wins!"
    else:
        return "It's a draw!"
