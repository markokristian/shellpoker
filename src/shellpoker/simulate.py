import random
from shellpoker.game import Game, Player
from shellpoker.wins import WIN_TYPES

N_SIMULATIONS = 5000
START_MONEY = 20
TARGET_UPSIDE = 4

def random_bet_behaviour(game: Game):
    # prefer bets with jokers, guessing most people bet high
    weights = [1, 1, 3, 2, 4]
    bet_choices = [1, 2, 3, 4, 5]
    game.bet = random.choices(bet_choices, weights=weights, k=1)[0]

def rational_card_selection(game: Game):
    hand = game.player.hand
    rank_counts = {}
    suit_counts = {}
    for card in hand:
        rank_counts[card.rank.value] = rank_counts.get(card.rank.value, 0) + 1
        suit_counts[card.suit] = suit_counts.get(card.suit, 0) + 1

    keep_indices = [i+1 for i, card in enumerate(hand) if rank_counts[card.rank.value] > 1]
    if not keep_indices and max(suit_counts.values()) >= 3:
        flush_suit = max(suit_counts, key=lambda s: suit_counts[s])
        keep_indices = [i+1 for i, card in enumerate(hand) if card.suit == flush_suit]
    if not keep_indices:
        max_rank = max(card.rank.value for card in hand)
        keep_indices = [i+1 for i, card in enumerate(hand) if card.rank.value == max_rank]
    game.keep_selected_cards(keep_indices)

def simulate_once():
    game = Game(Player("Sim", START_MONEY))
    stats = {
        "hands": 0,
        "wins": 0,
        "total_money_won": 0,
        "win_types": {win_type.name: 0 for win_type in WIN_TYPES},
        "joker_wins": 0,
        "biggest_win": 0,
        "final_money": 0,
        "happy": False,
    }
    game.start_new_game()
    while game.player.money > 0:
        random_bet_behaviour(game)
        game.shuffle_deck()
        game.deal_hand()
        rational_card_selection(game)
        stats["hands"] += 1
        win_name, money_won = game.get_win()
        if win_name and money_won > 0:
            stats["wins"] += 1
            stats["total_money_won"] += money_won
            stats["win_types"][win_name] += 1
            stats["biggest_win"] = max(stats["biggest_win"], money_won)
            if any(card.is_joker() for card in game.player.hand):
                stats["joker_wins"] += 1
        if money_won:
            game.player.money += money_won
        game.player.money -= game.bet
        if stats["hands"] > 0:
            if game.player.money >= START_MONEY * TARGET_UPSIDE:
                stats["happy"] = True
                break
    stats["final_money"] = game.player.money
    return stats

def aggregate_stats(results):
    agg = {
        "hands": 0,
        "wins": 0,
        "total_money_won": 0,
        "win_types": {win_type.name: 0 for win_type in WIN_TYPES},
        "joker_wins": 0,
        "biggest_win": 0,
        "happy_count": 0,
        "final_money_total": 0,
    }
    for s in results:
        agg["hands"] += s["hands"]
        agg["wins"] += s["wins"]
        agg["total_money_won"] += s["total_money_won"]
        agg["joker_wins"] += s["joker_wins"]
        agg["biggest_win"] = max(agg["biggest_win"], s["biggest_win"])
        agg["happy_count"] += int(s["happy"])
        agg["final_money_total"] += s["final_money"]
        for k in agg["win_types"]:
            agg["win_types"][k] += s["win_types"][k]
    return agg

def main():
    print(f"Simulating {N_SIMULATIONS} games with starting money of {START_MONEY}$ and target upside of {TARGET_UPSIDE * START_MONEY}$")
    random.seed(42)
    results = [simulate_once() for _ in range(N_SIMULATIONS)]
    stats = aggregate_stats(results)
    total_starting_money = N_SIMULATIONS * START_MONEY
    bank_earnings = total_starting_money - stats['final_money_total']
    print(f"Happy ({TARGET_UPSIDE*START_MONEY}$): {stats['happy_count']} times ({stats['happy_count']/N_SIMULATIONS*100:.2f}%)")
    print(f"Avg hands played: {stats['hands']/N_SIMULATIONS:.2f}")
    print(f"Avg final money: {stats['final_money_total']/N_SIMULATIONS:.2f}")
    print(f"Total wins: {stats['wins']} ({stats['wins']/stats['hands']*100:.2f}%)")
    print(f"Total money won: {stats['total_money_won']}")
    print(f"Biggest win: {stats['biggest_win']}")
    print(f"Joker in win: {stats['joker_wins']} times")
    print(f"Bank earnings: {bank_earnings}")
    print("Win type distribution:")
    for k, v in stats["win_types"].items():
        print(f"  {k:<20}: {v}")

if __name__ == "__main__":
    main()
