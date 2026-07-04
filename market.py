from lmsr import LMSRMarketMaker

class Market:
    def __init__(self, name, options):
        if len(options) < 1 or len(options) > 5:
            raise ValueError("Market must have between 1 and 5 options")
        
        self.name = name
        self.options = options
        
        # 初始化市场，每个选项的份额等于选项总数
        # 例如：2个选项时，每个选项有2个share；3个选项时，每个选项有3个share
        option_count = len(options)
        self.shares = {option: float(option_count) for option in options}
        
        # 每个选项需要1U资金
        self.funding_pool = float(len(options))
        self.market_maker = LMSRMarketMaker(self.funding_pool)
        
    def add_option(self, option):
        """添加新选项到市场"""
        if option in self.options:
            raise ValueError("Option '{}' already exists".format(option))
        if len(self.options) >= 5:
            raise ValueError("Maximum 5 options allowed")
            
        # 为所有现有选项增加1个share
        for existing_option in self.options:
            self.shares[existing_option] += 1.0
            
        # 添加新选项，份额等于当前选项总数+1
        self.options.append(option)
        new_option_count = len(self.options)
        self.shares[option] = float(new_option_count)
        
        # 增加资金池
        self.funding_pool += 1.0
        
        # 更新市场做市商
        self.market_maker = LMSRMarketMaker(self.funding_pool)

    def buy_shares(self, option, amount):
        """Buy shares for a specific option. Returns the cost in USD."""
        if option not in self.options:
            raise ValueError(f"Invalid option: {option}")
        if amount <= 0:
            raise ValueError("Amount must be positive")

        old_shares = [self.shares[opt] for opt in self.options]
        new_shares = old_shares.copy()
        option_index = self.options.index(option)
        new_shares[option_index] += amount

        cost = self.market_maker.calc_cost(old_shares, new_shares)
        if cost > self.funding_pool:
            raise ValueError("Insufficient liquidity in funding pool")

        self.shares[option] += amount
        self.funding_pool += cost
        return cost

    def sell_shares(self, option, amount):
        """Sell shares of a specific option. Returns the payout in USD."""
        if option not in self.options:
            raise ValueError(f"Invalid option: {option}")
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if self.shares[option] < amount:
            raise ValueError("Insufficient shares")

        old_shares = [self.shares[opt] for opt in self.options]
        new_shares = old_shares.copy()
        option_index = self.options.index(option)
        new_shares[option_index] -= amount

        cost = self.market_maker.calc_cost(old_shares, new_shares)
        payout = -cost  # negative cost means payout

        if payout > self.funding_pool:
            raise ValueError("Insufficient funds in pool")

        self.shares[option] -= amount
        self.funding_pool -= payout
        return payout

    def get_prices(self):
        """Get current prices for all options"""
        shares_list = [self.shares[opt] for opt in self.options]
        return {
            option: self.market_maker.calc_marginal_price(shares_list, i)
            for i, option in enumerate(self.options)
        }

    def get_status(self):
        """Get formatted status of the market"""
        prices = self.get_prices()
        status = [
            "【市场】{}".format(self.name),
            "【总资金】{:.2f}".format(self.funding_pool),
            "【选项】"
        ]
        for option in self.options:
            status.append("{} | {:.2f} | {:.4f}".format(option, self.shares[option], prices[option]))
        return "\n".join(status)
        
    def get_max_buyable_shares(self, option, precision=0.0001):
        """
        计算在当前资金池状态下，可以购买的最大份额数量
        
        Args:
            option: 要购买的选项名称
            precision: 计算精度
            
        Returns:
            可购买的最大份额数量
        """
        if option not in self.options:
            raise ValueError(f"Invalid option: {option}")
        
        option_index = self.options.index(option)
        current_shares = [self.shares[opt] for opt in self.options]
        
        # 定义一个函数，判断购买x份额是否会超出资金池
        def is_affordable(x):
            new_shares = current_shares.copy()
            new_shares[option_index] += x
            
            cost = self.market_maker.calc_cost(current_shares, new_shares)
            return cost <= self.funding_pool
        
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
