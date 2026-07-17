""" 
Blackjack - Initial Edition

I built the inital project for the assignment, here and then later added all the fun stuff. 
This is the version for that the "basic" code. 

The aim of the game is to beat the dealer by getting as close to 21 as possible without going over. 

King, Queen and Jack are worth 10 points, Aces can be worth 1 or 11 points, and all other cards are worth their face value.

How to play:
- Click HIT to take another card 
- Click STAND to end your turn and let the dealer play
- Click PLAY AGAIN to start a new round
- Click QUIT to exit the game

Best of luck! :)
"""

import random 

# Global counters

games_played = 0 
player_wins = 0 
dealer_wins = 0 
pushes = 0 
blackjacks_hit = 0 
best_hand_margin = 0 

def create_deck():
    """Creates a deck of cards and shuffles it."""
    suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
    deck = [(rank, suit) for suit in suits for rank in ranks]
    random.shuffle(deck)
    return deck

def card_value(card):
    """Returns the value of a card."""
    rank, suit = card
    if rank in ["Jack", "Queen", "King"]:
        return 10
    elif rank == "Ace":
        return 11  # Initially treat Ace as 11; will adjust later if needed
    else:
        return int(rank)
    
def calculate_hand_value(hand):
    """Calculates the total value of a hand, adjusting for Aces as needed."""
    value = sum(card_value(card) for card in hand)
    # Adjust for Aces if value is over 21
    aces = sum(1 for card in hand if card[0] == "Ace")
    while value > 21 and aces:
        value -= 10  # Treat one Ace as 1 instead of 11
        aces -= 1
    return value

def display_hand(name, hand, hide_first_card=False):
    """Displays the hand of a player or dealer."""
    if hide_first_card:
        print(f"{name}'s hand: [Hidden], " + ", ".join(f"{rank} of {suit}" for rank, suit in hand[1:]))
    else:
        print(f"{name}'s hand: " + ", ".join(f"{rank} of {suit}" for rank, suit in hand) + f" (Total value: {calculate_hand_value(hand)})")

def get_hit_or_stand():
    """Prompts the player to hit or stand."""
    while True:
        choice = input("Do you want to HIT or STAND? (H/S): ").strip().upper()
        if choice in ["H", "S"]:
            return choice
        else:
            print("Invalid input. Please enter 'H' to hit or 'S' to stand.")

def player_turn(deck, player_hand):
    """Handles the player's turn."""
    while True:
        display_hand("Player", player_hand)
        if calculate_hand_value(player_hand) > 21:
            print("You busted!")
            return False  # Player busts
        choice = get_hit_or_stand()
        if choice == "H":
            player_hand.append(deck.pop())
        else:
            return True  # Player stands
        
def dealer_turn(deck, dealer_hand):
    """Handles the dealer's turn."""
    while calculate_hand_value(dealer_hand) < 17:
        dealer_hand.append(deck.pop())
    display_hand("Dealer", dealer_hand)
    if calculate_hand_value(dealer_hand) > 21:
        print("Dealer busted!")
        return False  # Dealer busts
    return True  # Dealer stands

def determine_winner(player_hand, dealer_hand):
    """Determines the winner of the round."""
    player_value = calculate_hand_value(player_hand)
    dealer_value = calculate_hand_value(dealer_hand)
    
    if player_value > 21:
        return "Dealer wins!"
    elif dealer_value > 21:
        return "Player wins!"
    elif player_value > dealer_value:
        return "Player wins!"
    elif dealer_value > player_value:
        return "Dealer wins!"
    else:
        return "It's a push!"
    
def show_stats():
    """Displays the game statistics."""
    print(f"Games played: {games_played}")
    print(f"Player wins: {player_wins}")
    print(f"Dealer wins: {dealer_wins}")
    print(f"Pushes: {pushes}")
    print(f"Blackjacks hit: {blackjacks_hit}")
    print(f"Best hand margin: {best_hand_margin}")

def display_instructions():
    """Displays the game instructions."""
    print("=" * 50)
    print("Welcome to Blackjack!")
    print("=" * 50)
    print("The aim of the game is to beat the dealer by getting as close to 21 as possible without going over.")
    print("King, Queen and Jack are worth 10 points, Aces can be worth 1 or 11 points, and all other cards are worth their face value.")
    print("How to play:")
    print("You go first, and it's the dealer's turn!")
    print("Dealer must hit until reaching 17 or higher.")
    print("=" * 50)

def play_round():
    """Play a single round of Blackjack from start to finish."""
    deck = create_deck()
    player_hand = [deck.pop(), deck.pop()]
    dealer_hand = [deck.pop(), deck.pop()]
 
    print("\n--- New Round ---")
    display_hand("Dealer", dealer_hand, hide_first=True)
    # player_turn() displays the player's hand itself at the start of
    # its loop, so we don't print it again here (that was causing it
    # to show twice).
 
    player_hand = player_turn(deck, player_hand)
 
    # Only run the dealer's turn if the player didn't already bust
    if calculate_hand_value(player_hand) <= 21:
        dealer_hand = dealer_turn(deck, dealer_hand)
 
    result = determine_winner(player_hand, dealer_hand)
    print(f"\n{result}")
 
 
def get_yes_no(prompt):
    """Generic yes/no input validator used for 'play again?' prompts."""
    while True:
        answer = input(prompt).strip().lower()
        if answer in ('y', 'yes'):
            return True
        elif answer in ('n', 'no'):
            return False
        else:
            print("Please answer with 'y' or 'n'.")
 
 def main():
    """Main game loop."""
    display_instructions()

    while True:
        play_round()
        show_stats()
        if not get_yes_no("Do you want to play again? (y/n): "):
            print("Thanks for playing! Final stats:")
            show_stats()
            break    

if __name__ == "__main__":
    main()
