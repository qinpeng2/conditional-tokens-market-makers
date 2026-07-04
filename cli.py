from market import Market

def print_help():
    print("""
可用命令:
1. create - 创建新市场
2. add - 添加新选项
3. buy - 购买份额
4. sell - 卖出份额
5. status - 查看市场状态
6. help - 显示此帮助
7. exit - 退出程序

示例:
create
add 选项3
buy 选项1 10
sell 选项1 5
status
    """.strip())

def main():
    market = None
    print("欢迎使用预测市场交易系统!")
    print_help()

    while True:
        try:
            command = input("\n请输入命令: ").strip().split()
            if not command:
                continue

            cmd = command[0].lower()

            if cmd == "exit":
                break

            elif cmd == "help":
                print_help()

            elif cmd == "create":
                if market is not None:
                    print("已经存在一个市场，不能创建新市场")
                    continue

                name = input("请输入市场名称: ").strip()
                if not name:
                    print("市场名称不能为空")
                    continue

                options = []
                print("请输入选项 (每行一个，输入空行结束):")
                while True:
                    option = input().strip()
                    if not option:
                        break
                    options.append(option)

                try:
                    market = Market(name, options)
                    print("\n市场创建成功!")
                    print(market.get_status())
                except ValueError as e:
                    print(f"错误: {e}")
                    market = None
                    
            elif cmd == "add":
                if market is None:
                    print("请先创建市场")
                    continue
                if len(command) != 2:
                    print("用法: add <选项>")
                    continue
                    
                option = command[1]
                try:
                    market.add_option(option)
                    print(f"\n选项 '{option}' 添加成功!")
                    print(market.get_status())
                except ValueError as e:
                    print(f"错误: {e}")

            elif cmd == "buy":
                if market is None:
                    print("请先创建市场")
                    continue
                if len(command) != 3:
                    print("用法: buy <选项> <数量>")
                    continue

                option = command[1]
                try:
                    amount = float(command[2])
                    cost = market.buy_shares(option, amount)
                    print(f"\n购买成功! 支付: {cost:.2f}")
                    print(market.get_status())
                except ValueError as e:
                    print(f"错误: {e}")

            elif cmd == "sell":
                if market is None:
                    print("请先创建市场")
                    continue
                if len(command) != 3:
                    print("用法: sell <选项> <数量>")
                    continue

                option = command[1]
                try:
                    amount = float(command[2])
                    payout = market.sell_shares(option, amount)
                    print(f"\n卖出成功! 获得: {payout:.2f}")
                    print(market.get_status())
                except ValueError as e:
                    print(f"错误: {e}")

            elif cmd == "status":
                if market is None:
                    print("请先创建市场")
                    continue
                print(market.get_status())

            else:
                print(f"未知命令: {cmd}")
                print_help()

        except KeyboardInterrupt:
            print("\n程序已终止")
            break
        except Exception as e:
            print(f"发生错误: {e}")

if __name__ == "__main__":
    main()
