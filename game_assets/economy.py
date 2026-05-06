"""

"""

from .game_constants import CoinType


class Coins:
    def __init__(self):
        self.total = {
                        CoinType.cp: 0,
                        CoinType.sp: 0,
                        CoinType.ep: 0,
                        CoinType.gp: 0,
                        CoinType.pp: 0}


    def parse(self, cost_string: str | list[str]):
        """
        :param cost_string: can either be a string or a list
        """

        if isinstance(cost_string, str):  # single value to parse
            amount, denomination = cost_string.split(" ")
            self.total[CoinType[denomination]] = int(amount)

        if isinstance(cost_string, list):  # list of values to parse
            for coin_amount in cost_string:
                amount, denomination = coin_amount.split(" ")

                self.total[CoinType[denomination.lower()]] = int(amount)

    @classmethod
    def to_coins(cls, copper_total):
        result = {}
        remaining = copper_total
        for coin in sorted(cls, key=lambda x: x.value["value"], reverse=True):
            if remaining >= coin.value["value"]:
                result[coin.name] = remaining // coin.value["value"]
                remaining %= coin.value["value"]

        return result