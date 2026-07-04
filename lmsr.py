import math
from typing import List

class LMSRMarketMaker:
    def __init__(self, funding: float):
        self.funding = funding
        self.b = funding / math.log(2)  # liquidity parameter

    def calc_cost(self, old_shares: List[float], new_shares: List[float]) -> float:
        """Calculate the cost for trading from old_shares to new_shares state"""
        if len(old_shares) != len(new_shares):
            raise ValueError("Share arrays must have same length")
        
        old_cost = self._calc_cost_for_shares(old_shares)
        new_cost = self._calc_cost_for_shares(new_shares)
        return new_cost - old_cost

    def _calc_cost_for_shares(self, shares: List[float]) -> float:
        """Calculate the cost function C(q) = b * log(sum(exp(q_i/b)))"""
        max_value = max(shares) / self.b
        # Subtract max_value for numerical stability
        sum_exp = sum(math.exp(q/self.b - max_value) for q in shares)
        return self.b * (math.log(sum_exp) + max_value)

    def calc_marginal_price(self, shares: List[float], outcome_index: int) -> float:
        """Calculate the marginal price of an outcome given current shares"""
        if outcome_index >= len(shares):
            raise ValueError("Invalid outcome index")
        
        denominator = sum(math.exp(q/self.b) for q in shares)
        numerator = math.exp(shares[outcome_index]/self.b)
        return numerator / denominator
