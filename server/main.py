"""
main driver program, testing ground for now
"""
import uvicorn
from game_server import app
from game_assets import *  # temporary while testing game_asset features

if __name__ == "__main__":
    # uvicorn.run(app, host="0.0.0.0", port=8000)
    pass

    test_coin_purse = Coins()
    test_coin_purse.add_to_coin_purse("75 SP")
    test_coin_purse.add_to_coin_purse(["5 CP", "75 SP", "11 EP", "100 PP"])
    test_coin_purse.display_coin_totals()
    test_coin_purse.remove_from_purse(["5 CP", "100 SP", "11 EP", "100 PP"])
    test_coin_purse.display_coin_totals()
