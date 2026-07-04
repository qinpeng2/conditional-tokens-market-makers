#!/usr/bin/env python3
from market import Market

def main():
    # Create a test market
    market = Market("Test Market", ["Option A", "Option B", "Option C"])
    
    # Print initial market status
    print(market.get_status())
    print("\nCalculating maximum buyable shares for each option:")
    
    # Calculate and print max buyable shares for each option
    for option in market.options:
        max_shares = market.get_max_buyable_shares(option)
        print("{}: Max buyable shares = {:.4f}".format(option, max_shares))
    
    # Test buying close to the maximum amount
    option = "Option A"
    max_shares = market.get_max_buyable_shares(option)
    buy_amount = max_shares * 0.95  # Buy 95% of the max
    
    print("\nTrying to buy {:.4f} shares of {} (95% of max)".format(buy_amount, option))
    cost = market.buy_shares(option, buy_amount)
    print("Purchase successful! Cost: {:.4f}".format(cost))
    print(market.get_status())
    
    # Recalculate max buyable shares after purchase
    print("\nAfter purchase, recalculating max buyable shares:")
    for option in market.options:
        max_shares = market.get_max_buyable_shares(option)
        print("{}: Max buyable shares = {:.4f}".format(option, max_shares))
    
    # Try to buy more than the maximum (should fail)
    try:
        option = "Option B"
        max_shares = market.get_max_buyable_shares(option)
        buy_amount = max_shares * 1.1  # Buy 110% of the max
        
        print("\nTrying to buy {:.4f} shares of {} (110% of max)".format(buy_amount, option))
        market.buy_shares(option, buy_amount)
        print("Purchase successful! (This should not happen)")
    except ValueError as e:
        print("Purchase failed, error: {}".format(e))
    
if __name__ == "__main__":
    main()
