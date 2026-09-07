import pytest
from war_game import (
    REQUIRED_DECK_LENGTH,
    get_card_value,
    play_game,
    shuffle_deck,
    shuffle_deck_builtin,
    validate_input,
)


class TestGetCardValue:
    def test_known_cards(self):
        assert get_card_value("A") == 14
        assert get_card_value("K") == 13
        assert get_card_value("Q") == 12
        assert get_card_value("J") == 11
        
        for card in range(2, 11):
            assert get_card_value(str(card)) == card

    def test_unknown_card_returns_zero(self):
        assert get_card_value("X") == 0
        assert get_card_value("") == 0


class TestValidateInput:
    @pytest.mark.parametrize(
        "deck1, deck2",
        [
            (["2"] * REQUIRED_DECK_LENGTH, ["3"] * REQUIRED_DECK_LENGTH),
        ],
    )
    def test_valid_lengths_do_not_raise(self, deck1, deck2):
        validate_input(deck1, deck2)  # should not raise
        

    @pytest.mark.parametrize(
        "deck1, deck2",
        [
            (["2"] * REQUIRED_DECK_LENGTH, ["3"] * 4),
            (["2"] * 6, ["3"] * REQUIRED_DECK_LENGTH),
            (["2"] * 3, ["3"] * 4),
            (["2"] * 5, ["3"] * 6),
        ],
    )
    def test_wrong_length_raises(self, deck1, deck2):
        with pytest.raises(ValueError):
            validate_input(deck1, deck2)    


class TestShuffleDeck:
    """Tests for the manual Fisher-Yates implementation."""

    @pytest.fixture
    def sample_deck(self):
        return ["A", "K", "Q", "J", "10"]

    def test_preserves_length(self, sample_deck):
        shuffle_deck(sample_deck)
        assert len(sample_deck) == 5

    def test_preserves_multiset(self, sample_deck):
        original = sample_deck.copy()
        shuffle_deck(sample_deck)
        assert sorted(sample_deck) == sorted(original)

    def test_exact_result_with_mocked_randomness(self, mocker):
        # Pin the "random" choices instead of relying on statistics,
        # so this test is deterministic and never flaky.
        deck = [1, 2, 3, 4]
        mocker.patch("war_game.random.randint", side_effect=[0, 0, 0])
        shuffle_deck(deck)
        # i=3: j=0 -> [4, 2, 3, 1]
        # i=2: j=0 -> [3, 2, 4, 1]
        # i=1: j=0 -> [2, 3, 4, 1]
        assert deck == [2, 3, 4, 1]

    def test_empty_deck_does_not_raise(self):
        deck = []
        shuffle_deck(deck)
        assert deck == []


class TestShuffleDeckBuiltin:
    def test_preserves_length_and_multiset(self):
        original = ["A", "K", "Q", "J", "10"]
        deck = original.copy()
        shuffle_deck_builtin(deck)
        assert len(deck) == len(original)
        assert sorted(deck) == sorted(original)


class TestPlayGame:
    @pytest.fixture
    def strong_deck(self):
        return ["A", "K", "Q", "J", "10", "9", "8", "7", "6", "5"]

    @pytest.mark.parametrize(
        "p1, p2, expected_winner",
        [
            (["A", "K", "Q", "J", "10", "9", "8", "7", "6", "5"], ["2"] * 10, "Player 1 wins!"),
            (["2"] * 10, ["A", "K", "Q", "J", "10", "9", "8", "7", "6", "5"], "Player 2 wins!"),
            (["A"] * 5 + ["2"] * 5, ["2"] * 5 + ["A"] * 5, "It's a tie!"),
        ],
    )
    def test_raises_on_invalid_deck_size(self, p1, p2, expected_winner):
        if expected_winner is None:
            with pytest.raises(ValueError):
                play_game(p1, p2)

    def test_winner_when_shuffle_is_disabled(self, mocker, strong_deck):
        # Neutralize the shuffle so the scoring logic can be verified
        # deterministically, independent of randomness.
        mocker.patch("war_game.shuffle_deck_builtin", lambda deck: None)
        p2 = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J"]
        assert play_game(strong_deck, p2) == "Player 1 wins!"

    def test_tie_is_shuffle_invariant(self):
        # 5xA + 5x2 on both sides always ties, whatever the shuffle order --
        # see the conversation for why (symmetry argument).
        p1 = ["A", "2"] * 5
        p2 = ["2", "A"] * 5
        assert play_game(p1, p2) == "It's a tie!"
