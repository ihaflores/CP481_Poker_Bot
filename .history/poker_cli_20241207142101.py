from pokerkit import *
import socketio

# SocketIO setup
sio = socketio.Server(async_mode='threading')
app = socketio.WSGIApp(sio)

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
    0,  # ante
    (200, 400),  # Small and big blinds
    400,  # big bet
    (10000, 10000, 10000),  # Starting chips for each player
    3  # Number of players
)

def emit_game_state():
    """Send the current game state to the frontend."""
    sio.emit('update_state', {
        'pot': state.total_pot_amount,
        'board_cards': get_board_cards(),
        'players': [
            {
                'id': i,
                'stack': state.stacks[i],
                'status': 'Active' if state.statuses[i] else 'Folded',
                'hand': tuple(state.get_down_cards(i))
            }
            for i in range(state.player_count)
        ]
    })

def emit_winner():
    """Send the winner information to the frontend."""
    winner = find_winner()
    sio.emit('game_end', {
        'winner': {
            'id': winner['player_id'],
            'hand': winner['hand']
        }
    })

# Helper functions
def get_board_cards():
    board_cards_tuple = tuple(state.get_board_cards(0))
    value_map = {11: 'J', 12: 'Q', 13: 'K', 14: 'A'}
    suit_map = {'h': 'h', 'd': 'd', 'c': 'c', 's': 's'}
    board_cards = "".join(f"{value_map.get(card.rank, str(card.rank))}{suit_map[card.suit]}" for card in board_cards_tuple)
    return board_cards

def find_winner():
    best_hand = None
    winning_player = None
    for player in state.player_indices:
        hand = StandardHighHand.from_game(
            tuple(state.hole_cards[player]),
            tuple(state.get_board_cards(0))
        )
        if best_hand is None or hand > best_hand:
            best_hand = hand
            winning_player = player
    return {'player_id': winning_player, 'hand': str(best_hand)}

if __name__ == '__main__':
    # Deal hole cards
    for player in range(state.player_count * 2):
        state.deal_hole()

    emit_game_state()

    # Game rounds
    for stage in ["pre-flop", "flop", "turn", "river"]:
        if stage == "flop":
            state.burn_card()
            state.deal_board(3)
        elif stage in ["turn", "river"]:
            state.burn_card()
            state.deal_board(1)

        emit_game_state()

        while state.checking_or_calling_amount is not None:
            current_player = state.actor_index
            # Placeholder for player action logic
            state.check_or_call()
            emit_game_state()

    emit_winner()
