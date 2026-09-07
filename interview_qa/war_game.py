import random

CARD_VALUES = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
    "A": 14,
}
REQUIRED_DECK_LENGTH = 10  # Required length for both players' decks


def get_card_value(card: str) -> int:
    """Get the numeric value of a card."""
    return CARD_VALUES.get(card, 0)


def shuffle_deck(deck: list[str]) -> None:
    """Shuffle a single deck in place, without the built-in shuffle function."""
    for i in range(len(deck) - 1, 0, -1):
        j = random.randint(0, i)
        deck[i], deck[j] = deck[j], deck[i]


def shuffle_deck_builtin(deck: list[str]) -> None:
    """Shuffle a single deck in place using the built-in shuffle function."""
    random.shuffle(deck)


def validate_input(
    p1_deck: list[str], p2_deck: list[str], expected_length: int = REQUIRED_DECK_LENGTH
) -> None:
    """Validate that both decks have the expected length."""
    if len(p1_deck) != expected_length or len(p2_deck) != expected_length:
        raise ValueError(f"Both players must have decks of length {expected_length}.")


def play_game(player1_deck: list[str], player2_deck: list[str]) -> str:
    """Determine the winner of the game based on the decks."""
    validate_input(player1_deck, player2_deck)

    shuffle_deck_builtin(player1_deck)
    shuffle_deck_builtin(player2_deck)
    # shuffle_deck(player1_deck)
    # shuffle_deck(player2_deck)

    print(f"Player 1's shuffled deck: {player1_deck} \nPlayer 2's shuffled deck: {player2_deck}")

    player1_score = 0
    player2_score = 0
    for round_num, (card1, card2) in enumerate(zip(player1_deck, player2_deck, strict=True), start=1):
        value1 = get_card_value(card1)
        value2 = get_card_value(card2)
        if value1 > value2:
            player1_score += 1
        elif value2 > value1:
            player2_score += 1
        print(f"Round {round_num}: Player 1 plays {card1} (value {value1}), Player 2 plays {card2} (value {value2})")

    if player1_score > player2_score:
        return "Player 1 wins!"
    elif player2_score > player1_score:
        return "Player 2 wins!"
    else:
        return "It's a tie!"


if __name__ == "__main__":
    # A few scenarios covering the main paths: a clear win, a tie,
    # and an invalid deck size that should raise instead of running silently.
    scenarios = [
        (
            "Clear win",
            ["A", "K", "Q", "J", "10", "9", "8", "7", "6", "5"],
            ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J"],
        ),
        (
            "Tie",
            ["A", "2", "A", "2", "A", "2", "A", "2", "A", "2"],
            ["2", "A", "2", "A", "2", "A", "2", "A", "2", "A"],
        ),
        (
            "Invalid deck size",
            ["A", "K", "Q"],
            ["2", "3", "4", "5"],
        ),
    ]

    for label, deck1, deck2 in scenarios:
        print(f"--- {label} ---")
        try:
            print(play_game(deck1, deck2))
        except ValueError as e:
            print(f"Error: {e}")
        print()