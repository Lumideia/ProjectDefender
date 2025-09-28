from collections import Counter


class Dice:
    edges: int

    def __init__(self, edges):
        self.edges = edges


def format_dice(dice_list):
    counter = Counter([d.edges for d in dice_list]) if dice_list else {}
    return " + ".join([f"{count}d{sides}" if count > 1 else f"d{sides}" for sides, count in counter.items()]) or "—"
