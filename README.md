# conditional-tokens-market-makers

> Fork of [gnosis/conditional-tokens-market-makers](https://github.com/gnosis/conditional-tokens-market-makers)
>
> **📦 本地备份快照** (2026-07-04) — 原路径 `/opt/workspace/playground/ctf/`

## 这是什么

Gnosis **条件代币自动做市商（AMM）** 智能合约。用于预测市场等场景，基于 LMSR（对数市场评分规则）提供流动性。

## 分支说明

| 分支 | 来源路径 | 改动摘要 |
|------|---------|---------|
| `master` | `ctf/conditional-tokens-market-makers` | 修改 `FixedProductMarketMaker.sol`（4 行合约逻辑调整） |
| `demo` | `ctf/market-makers-demo` | 同上合约改动 + Python 做市模拟工具 |

### `demo` 分支额外文件

| 文件 | 说明 |
|------|------|
| `cli.py` | 命令行交互入口 |
| `lmsr.py` | LMSR 定价算法实现 |
| `market.py` | 市场状态管理 |
| `max_shares.py` | 最大份额计算 |
| `test_max_shares.py` | 单元测试 |

## 快速开始

### 合约（Foundry/Hardhat）

```bash
# 安装依赖后编译测试
npm install
npm test
```

### Python 模拟（`demo` 分支）

```bash
git checkout demo
python cli.py
python -m pytest test_max_shares.py
```

## 上游

- 仓库：https://github.com/gnosis/conditional-tokens-market-makers
- 相关：[conditional-tokens](https://github.com/gnosis/conditional-tokens) 条件代币标准

## 关联项目

同目录下还有：
- `qinpeng2/conditional-tokens-tutorial` — 前端教程与市场配置
- `qinpeng2/ctf-exchange` — Polymarket CTF 交易所合约
