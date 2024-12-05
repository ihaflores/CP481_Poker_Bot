from pokerkit import *

# Set up the initial game state
state = NoLimitTexasHoldem.create_state(
    # Automations
    (
        Automation.ANTE_POSTING,
        Automation.BET_COLLECTION,
        Automation.BLIND_OR_STRADDLE_POSTING,
        Automation.HOLE_CARDS_SHOWING_OR_MUCKING,
        Automation.HAND_KILLING,
        Automation.CHIPS_PUSHING,
        Automation.CHIPS_PULLING,
    ),
    False,  # False for big blind ante
    0, # ante
    (200, 400), # Small and big blinds
    400, # big bet
    (10000, 10000, 10000), # Starting chips for each player
    3 # Set the number of players
)

# Global vars
players = [x for x in state.player_indices]
small_blind_idx = 0 # start with first player as the small blind
big_blind_idx = small_blind_idx  + 1 # big blind is to left of small blind
starting_player_idx = big_blind_idx + 1 # starting player is player to left of big blind
game_over = False # flag to indicate if the game is over

def player_action(player):
    """Prompt player for an action."""
    hand = tuple(state.get_down_cards(player))
    print(f"Pot: {state.total_pot_amount} | Player {player}'s Stack: {tuple(state.stacks)[player]}")
    print(f"Player {player}'s turn with {tuple(state.get_down_cards(player))}")
    print(f"Board Cards: {tuple(state.get_board_cards(0))}")
    print(f"Check/Call amount: {state.checking_or_calling_amount}")
    print(f"The minimum completion, betting, or raising to amount: {state.min_completion_betting_or_raising_to_amount}")

    while True:
        action = input("Choose action: check, call, bet, raise, fold: ").strip().lower()
        print(f"\n")
        if action == "check" or action == "call":
            state.check_or_call()
        elif action == "bet":
            amount = int(input("Enter bet amount: "))
            if amount < state.min_completion_betting_or_raising_to_amount:
                print(f"Bet amount is less than the minimum of {state.min_completion_betting_or_raising_to_amount}. Please input a valid bet amount")
                continue
            state.complete_bet_or_raise_to(amount)
        elif action == "raise":
            amount = int(input("Enter raise amount: "))
            if amount < state.min_completion_betting_or_raising_to_amount:
                print(f"Raise amount is less than the minimum of {state.min_completion_betting_or_raising_to_amount}. Please input a valid raise amount")
                continue
            state.complete_bet_or_raise_to(amount)
        elif action == "fold":
            state.fold()
        else:
            print(f"Please input a valid action")
            continue
        break

def get_player_hand(player):
    board_cards_tuple = tuple(state.get_board_cards(0))
    player_cards_tuple = tuple(state.hole_cards[player])
    board_cards = ""
    player_cards = ""

    value_map = {11: 'J', 12: 'Q', 13: 'K', 14: 'A'}
    suit_map = {'h': 'h', 'd': 'd', 'c': 'c', 's': 's'}

    for card in board_cards_tuple:
        value_str = value_map.get(card.rank, str(card.rank))  # Get face card or numeric value
        suit_str = suit_map[card.suit]                        # Get suit character
        board_cards += value_str + suit_str
    for card in player_cards_tuple:
        value_str = value_map.get(card.rank, str(card.rank))  # Get face card or numeric value
        suit_str = suit_map[card.suit]                        # Get suit character
        player_cards += value_str + suit_str
    hand = StandardHighHand.from_game(player_cards, board_cards)
    return hand

def get_player_hole_cards(player):
    player_cards_tuple = tuple(state.hole_cards[player])
    player_cards = ""

    value_map = {11: 'J', 12: 'Q', 13: 'K', 14: 'A'}
    suit_map = {'h': 'h', 'd': 'd', 'c': 'c', 's': 's'}
    for card in player_cards_tuple:
        value_str = value_map.get(card.rank, str(card.rank))  # Get face card or numeric value
        suit_str = suit_map[card.suit]                        # Get suit character
        player_cards += value_str + suit_str
    return player_cards

def get_board_cards():
    board_cards_tuple = tuple(state.get_board_cards(0))
    board_cards = ""

    value_map = {11: 'J', 12: 'Q', 13: 'K', 14: 'A'}
    suit_map = {'h': 'h', 'd': 'd', 'c': 'c', 's': 's'}

    for card in board_cards_tuple:
        value_str = value_map.get(card.rank, str(card.rank))  # Get face card or numeric value
        suit_str = suit_map[card.suit]                        # Get suit character
        board_cards += value_str + suit_str
    return board_cards

def find_winner():
    # Evaluate each player's hand and determine the winner
    best_hand = None
    winning_player = None

    print("\nFinal hands:")
    print(f"Board Cards: {tuple(state.get_board_cards(0))}\n")

    for player in state.player_indices:
        # display player's hole cards
        print(f"Player {player}: {tuple(state.get_down_cards(player))}\n")

        # Get the player's hand rank
        hand = get_player_hand(player)
        print(f"Player {player} hand rank: {hand}")

        # Determine the highest-ranked hand
        if best_hand is None or hand > best_hand:
            best_hand = hand
            winning_player = player

    print(f"The winner is Player {winning_player} with a hand rank of {best_hand}.")

def check_game_over():
    # Check if all players but one have folded
    count = 0
    for status in state.statuses:
        if status is True:
            count += 1
    
    # If only 1 player remains, the game is over
    if count == 1:
        return True
    else:
        return False

if __name__ == '__main__':
    # Deal the initial hole cards to all players in sequence, one at a time
    for player in range(state.player_count * 2):
        state.deal_hole()

    # Game rounds
    for stage in ["pre-flop", "flop", "turn", "river"]:
        # Check if game has ended early
        if game_over:
            break

        # Start next round
        print(f"\n{stage.capitalize()} round:")
        if stage == "flop":
            state.burn_card()
            state.deal_board(3)  # Deal three community cards for the flop
        elif stage == "turn" or stage == "river":
            state.burn_card()
            state.deal_board(1)  # Deal one community card for turn and river

        while state.checking_or_calling_amount is not None:
            # Get the current player
            current_player = players[state.actor_index]
            
            # Get player's hole cards and board cards
            board_cards = get_board_cards()
            player_hole_cards = get_player_hole_cards(current_player)

            # Calculate player's hand strength
            hand_strength = calculate_hand_strength(
                state.player_count, # Number of players
                parse_range(player_hole_cards), # Hole cards
                Card.parse(board_cards), # Board cards
                2,
                5,
                Deck.STANDARD,
                (StandardHighHand, ),
                sample_count=1000,
            )
            print(f"Player {current_player} hand strength: {hand_strength}")

            # Run next player action
            player_action(current_player)

            # Check if all players have folded except one
            if check_game_over():
                game_over = True
                break

    # the winner is the remaining hand, find index of remaining hole cards to find winner's player index
    winner = -1
    for player_idx in range(len(state.statuses)):
        if state.statuses[player_idx] is True:
            winner = player_idx

    # Get the winning hand
    winning_hand = get_player_hand(winner)

    # Display the winner and winning hand
    print(f"The winner is Player {winner}!")
    print(f"Winning Hand: {winning_hand}")