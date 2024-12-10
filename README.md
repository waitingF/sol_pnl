# Solana PnL Analyzer

这是一个用于分析Solana钱包地址收益与损失的Python工具。

## 功能特点

- 支持获取7天或30天的交易历史
- 分析交易盈亏情况
- 生成交易统计报告
- 数据可视化展示

## 项目结构

```
sol_pnl/
├── src/                # 源代码目录
│   ├── config.py      # 配置文件
│   ├── data_fetcher.py# 数据获取模块
│   └── analyzer.py    # 数据分析模块
├── tests/             # 测试目录
├── data/              # 数据存储目录
└── requirements.txt   # 项目依赖
```

## 安装

1. 克隆项目
2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 配置环境变量：
- 复制 `.env.example` 为 `.env`
- 在 `.env` 中设置你的 Helius API key

## 使用方法

1. 设置环境变量
2. 运行分析脚本
3. 查看生成的分析报告

## API密钥获取

访问 [Helius开发者平台](https://dev.helius.xyz/) 注册并获取API密钥。
