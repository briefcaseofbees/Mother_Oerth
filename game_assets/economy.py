"""

"""

import random
from .game_constants import CoinType, CreatureAttitude, Reputation, VendorType, WealthLevel, VendorMagicalItemOfferings
from .game_constants import _MAGICAL_OFFERINGS_QTY_TABLE

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
        self.wealth = wealth_level                   # how wealthy the merchant is (will also dictate stock)
        self.type:list[VendorType] = []              # vendor can have different offerings
        self.magical_offerings: VendorMagicalItemOfferings | None = None
        self.petty_cash = CoinPurse()                       # the coins that the vendor has on their person
        self.inventory = []                                 # the physical inventory the vendor has
        self.reputation = Reputation.neutral                # the reputation the player has with the vendor
        self.disposition = CreatureAttitude.indifferent     # the attitude the vendor has towards the player

        # need to come up with a way to implement that "barter" option from BG3 with this class...

    def generate_stock(self):
        """

        """

        # need some way to have some persistent stock between days...? (stock changing daily doesn't make sense)

        generated_inventory = []
        stock_qty = 0
        magical_item_qty = None

        """CHECK IF VENDOR HAS MAGICAL ITEMS FOR SALE"""
        if self.magical_offerings is not None:
            magical_item_qty = random.randint(_MAGICAL_OFFERINGS_QTY_TABLE[self.magical_offerings][0],
                                              _MAGICAL_OFFERINGS_QTY_TABLE[self.magical_offerings][1])

        """FIGURE OUT HOW MANY ITEMS ARE IN STOCK"""
        for vendor_type in self.type:
            if self.wealth == WealthLevel.poor:
                stock_qty = random.randint(3, 5)
            elif self.wealth == WealthLevel.lower_class:
                stock_qty = random.randint(5, 7)
            elif self.wealth == WealthLevel.middle_class:
                stock_qty = random.randint(7, 12)
            elif self.wealth == WealthLevel.upper_class:
                stock_qty = random.randint(12, 17)
            elif self.wealth == WealthLevel.rich:
                stock_qty = random.randint(17, 25)
            else:
                stock_qty = 2

        """BEFORE PICKING MUNDANE ITEMS IN STOCK, PICK MAGICAL ITEMS FROM VENDOR TYPE CATEGORIES"""
        if magical_item_qty is not None:
            magical_item_pick = None
            # pick a magical item from vendor type categories
            while magical_item_qty > 0:

                # pick a random category in VendorType to choose magical item from
                vendor_type_pick = random.choice(self.type)

                # pick a random magical item that falls in that VendorType category
                magical_item_pick = None  # this is where the code will go for polling for magical items in categories

                generated_inventory.append(magical_item_pick)
                magical_item_qty -= 1   # decrement magical item qty
                stock_qty -= 1          # decrement stock qty (counts against stock count as well)

        """PICK REST OF STOCK FROM VENDOR TYPE CATEGORIES"""


        self.inventory = generated_inventory

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


def generate_loot_pool(wealth_level: WealthLevel):

    # create a list of items that corresponds with a particular level of wealth

    pass
