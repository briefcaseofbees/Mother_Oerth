"""

"""

from .game_constants import CoinType, CreatureAttitude, Reputation, WealthLevel


class CoinPurse:
    def __init__(self):
        self.total = {
                        CoinType.cp: 0,
                        CoinType.sp: 0,
                        CoinType.ep: 0,
                        CoinType.gp: 0,
                        CoinType.pp: 0}

        self.weight = 0

    def get_weight(self):
        return self.weight

    def calculate_weight(self):
        # per the SRD, a coin weighs a third of an ounce (regardless of denomination)
        # "50 coins equals 1 lb" p.89

        coin_total = 0

        for coin_amount in self.total.values():
            coin_total += int(coin_amount)

        self.weight = coin_total / 48  # each coin is 1/3 of an ounce, but 16 ounces to a pound, so: coin_total/48 -> lb

    def add_to_coin_purse(self, coin_string: str | list[str]):
        """
        :param coin_string: can either be a string or a list
        """

        if isinstance(coin_string, str):  # single value to parse
            amount, denomination = coin_string.split(" ")
            self.total[CoinType[denomination.lower()]] += int(amount)

        if isinstance(coin_string, list):  # list of values to parse
            for coin_amount in coin_string:
                amount, denomination = coin_amount.split(" ")

                self.total[CoinType[denomination.lower()]] += int(amount)

        self.calculate_weight()  # recalculate weight of coin purse after adding

    def remove_from_purse(self, coin_string: str | list[str]):
        """
        :param coin_string: can either be a string or a list
        """

        if isinstance(coin_string, str):  # single value to parse
            amount, denomination = coin_string.split(" ")

            if self.total[CoinType[denomination.lower()]] < int(amount):
                print(f"not enough coins to remove: {coin_string}")
            else:
                self.total[CoinType[denomination.lower()]] -= int(amount)

        if isinstance(coin_string, list):  # list of values to parse

            adjusted_purse = self.total.copy()  # a temporary coin purse (possible fail points at any point in list)

            for coin_amount in coin_string:
                amount, denomination = coin_amount.split(" ")

                if adjusted_purse[CoinType[denomination.lower()]] < int(amount):
                    print(f"not enough coins in purse to remove {coin_amount} from it, cancelling...")
                    return
                else:
                    adjusted_purse[CoinType[denomination.lower()]] -= int(amount)

            self.total = adjusted_purse
            self.calculate_weight()  # recalculate weight of coin purse after removal

    def display_coin_totals(self):
        for coin in self.total:
            print(f"{coin.label(short_form=False)}: {self.total[coin]}")


class Vendor:
    def __init__(self, wealth_level: WealthLevel):
        self.vendor_wealth = wealth_level                   # how wealthy the merchant is (will also dictate stock)
        self.petty_cash = CoinPurse()                           # the coins that the vendor has on their person
        self.inventory = []                                 # the physical inventory the vendor has
        self.reputation = Reputation.neutral                # the reputation the player has with the vendor
        self.disposition = CreatureAttitude.indifferent     # the attitude the vendor has towards the player

        # need to come up with a way to implement that "barter" option from BG3 with this class...

    def purchase_item(self):
        pass

    def sell_item(self):
        pass

    def money_changing_service(self):
        """
        exchanging denominations of coins with different denominations
        """

        # money changing should charge a % on the total worth of the exchange (convenience charge)
        # convenience charge should also relate to the disposition of the merchant towards the player
        # convenience charge should also relate to the reputation of the player

        # because coins WEIGH something, money changing is actually a very valuable service...

        pass