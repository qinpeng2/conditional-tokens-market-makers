import math
from typing import List
import numpy as np
from scipy.optimize import brentq

def calculate_max_buyable_shares(market, option: str) -> float:
    """
    计算在当前资金池状态下，可以购买的最大份额数量
    
    Args:
        market: Market实例
        option: 要购买的选项名称
        
    Returns:
        可购买的最大份额数量
    """
    if option not in market.options:
        raise ValueError(f"Invalid option: {option}")
    
    option_index = market.options.index(option)
    current_shares = [market.shares[opt] for opt in market.options]
    available_funds = market.funding_pool
    b = market.market_maker.b
    
    # 定义一个函数，计算购买x份额后的成本与可用资金的差值
    def cost_difference(x):
        new_shares = current_shares.copy()
        new_shares[option_index] += x
        
        # 计算成本函数 C(q) = b * log(sum(exp(q_i/b)))
        max_old = max(current_shares) / b
        sum_exp_old = sum(math.exp(q/b - max_old) for q in current_shares)
        old_cost = b * (math.log(sum_exp_old) + max_old)
        
        max_new = max(new_shares) / b
        sum_exp_new = sum(math.exp(q/b - max_new) for q in new_shares)
        new_cost = b * (math.log(sum_exp_new) + max_new)
        
        cost = new_cost - old_cost
        return cost - available_funds
    
    # 如果即使购买很小的份额也会超出资金池，返回0
    if cost_difference(0.0001) > 0:
        return 0
    
    # 找一个足够大的上界，使得购买这么多份额肯定会超出资金池
    upper_bound = 1.0
    while cost_difference(upper_bound) < 0:
        upper_bound *= 2
    
    # 使用二分法查找最大可购买份额
    try:
        max_shares = brentq(cost_difference, 0, upper_bound)
        # 为了安全起见，稍微减少一点点
        return max_shares * 0.999
    except ValueError:
        # 如果找不到解，返回一个保守的估计
        return 0

# 如果不想依赖scipy，可以使用这个简单的二分查找实现
def calculate_max_buyable_shares_binary_search(market, option: str, precision=0.0001) -> float:
    """
    使用二分查找计算在当前资金池状态下，可以购买的最大份额数量
    
    Args:
        market: Market实例
        option: 要购买的选项名称
        precision: 精度
        
    Returns:
        可购买的最大份额数量
    """
    if option not in market.options:
        raise ValueError(f"Invalid option: {option}")
    
    option_index = market.options.index(option)
    current_shares = [market.shares[opt] for opt in market.options]
    
    # 定义一个函数，判断购买x份额是否会超出资金池
    def is_affordable(x):
        new_shares = current_shares.copy()
        new_shares[option_index] += x
        
        cost = market.market_maker.calc_cost(current_shares, new_shares)
        return cost <= market.funding_pool
    
    # 找一个足够大的上界，使得购买这么多份额肯定会超出资金池
    upper = 1.0
    while is_affordable(upper):
        upper *= 2
    
    # 二分查找
    lower = 0
    while upper - lower > precision:
        mid = (upper + lower) / 2
        if is_affordable(mid):
            lower = mid
        else:
            upper = mid
    
    # 为了安全起见，返回一个稍微保守的估计
    return lower * 0.999
