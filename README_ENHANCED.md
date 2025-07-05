# DeFiLlama Handler

<div align="center">
  <img src="icon.svg" alt="DeFiLlama" width="64" height="64">
  <h3>DeFiLlama Handler for MindsDB</h3>
  <p>Access comprehensive DeFi data including protocols, TVL, yields, and stablecoins</p>
  
  ![Version](https://img.shields.io/badge/version-0.1.0-blue)
  ![Type](https://img.shields.io/badge/type-Data%20Handler-green)
  ![Status](https://img.shields.io/badge/status-Active-brightgreen)
</div>

---

## Overview

The DeFiLlama handler enables seamless integration with the [DeFiLlama API](https://defillama.com/), providing access to the largest TVL aggregator for DeFi protocols. Query comprehensive decentralized finance data directly from your MindsDB instance using standard SQL.

### Key Features

- 🏦 **Protocol Data**: Access 1000+ DeFi protocol metrics
- 📊 **TVL Analytics**: Historical Total Value Locked data
- 💰 **Yield Farming**: Real-time yield opportunities across chains
- 🪙 **Stablecoins**: Market data for major stablecoins
- ⛓️ **Multi-Chain**: Support for 100+ blockchains
- 🔄 **Real-Time**: Live data updates from DeFiLlama

## Quick Start

### 1. Create Connection

```sql
CREATE DATABASE defillama_datasource
WITH 
  ENGINE = 'defillama',
  PARAMETERS = {
    "base_url": "https://api.llama.fi"
  };
```

### 2. Query Data

```sql
-- Get top DeFi protocols by TVL
SELECT name, tvl, chain, category, change_7d
FROM defillama_datasource.protocols 
ORDER BY tvl DESC 
LIMIT 10;
```

## Available Tables

| Table | Description | Key Columns |
|-------|-------------|-------------|
| `protocols` | DeFi protocol information and metrics | `name`, `tvl`, `chain`, `category` |
| `tvl` | Historical Total Value Locked data | `date`, `totalLiquidityUSD`, `chain` |
| `yields` | Yield farming and staking opportunities | `project`, `apy`, `tvlUsd`, `chain` |
| `stablecoins` | Stablecoin metrics and circulation | `name`, `circulating`, `chains` |
| `chains` | Blockchain TVL and information | `name`, `tvl`, `tokenSymbol` |
| `tokens` | Token price data | `address`, `chain`, `price` |

## Example Queries

### Protocol Analysis

```sql
-- Top protocols by category
SELECT 
    category,
    COUNT(*) as protocol_count,
    AVG(tvl) as avg_tvl,
    SUM(tvl) as total_tvl
FROM defillama_datasource.protocols 
WHERE tvl > 10000000
GROUP BY category 
ORDER BY total_tvl DESC;
```

### Yield Opportunities

```sql
-- High-yield opportunities with good TVL
SELECT 
    project,
    chain,
    symbol,
    apy,
    tvlUsd,
    CASE 
        WHEN apy > 50 THEN 'High Risk'
        WHEN apy > 20 THEN 'Medium Risk'
        ELSE 'Low Risk'
    END as risk_level
FROM defillama_datasource.yields 
WHERE apy > 15 AND tvlUsd > 1000000
ORDER BY apy DESC 
LIMIT 20;
```

### Cross-Chain Analysis

```sql
-- TVL distribution across chains
SELECT 
    chain,
    COUNT(*) as protocol_count,
    SUM(tvlUsd) as total_tvl,
    AVG(apy) as avg_apy
FROM defillama_datasource.yields 
WHERE tvlUsd > 100000
GROUP BY chain 
ORDER BY total_tvl DESC;
```

### Stablecoin Market

```sql
-- Stablecoin market analysis
SELECT 
    name,
    symbol,
    circulating / 1000000000 as circulating_billions,
    chains,
    pegType
FROM defillama_datasource.stablecoins 
WHERE circulating > 1000000000
ORDER BY circulating DESC;
```

## Advanced Features

### Historical TVL Analysis

```sql
-- TVL growth over time for Ethereum
SELECT 
    DATE(date) as date,
    totalLiquidityUSD / 1000000000 as tvl_billions
FROM defillama_datasource.tvl 
WHERE chain = 'Ethereum'
    AND date >= '2024-01-01'
ORDER BY date DESC 
LIMIT 30;
```

### Yield Strategy Discovery

```sql
-- Find stable yield opportunities
SELECT 
    y.project,
    y.chain,
    y.apy,
    y.tvlUsd,
    p.category,
    p.audits
FROM defillama_datasource.yields y
JOIN defillama_datasource.protocols p ON y.project = p.name
WHERE y.apy BETWEEN 5 AND 15
    AND y.tvlUsd > 5000000
    AND p.audits IS NOT NULL
ORDER BY y.tvlUsd DESC;
```

## Configuration

### Connection Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `base_url` | String | No | `https://api.llama.fi` | DeFiLlama API base URL |

### Rate Limits

- **No Authentication Required**: DeFiLlama API is free to use
- **Rate Limits**: Be respectful with request frequency
- **Best Practices**: Cache results when possible

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| Connection timeout | Check internet connectivity |
| No data returned | Verify filters aren't too restrictive |
| Slow queries | Add appropriate WHERE clauses |

### Support

- 📖 [DeFiLlama Documentation](https://docs.llama.fi/)
- 🌐 [DeFiLlama Website](https://defillama.com/)
- 💬 [MindsDB Community](https://mindsdb.com/community)

---

<div align="center">
  <p>Made with ❤️ by XplainCrypto Platform</p>
  <p>
    <a href="https://defillama.com/">DeFiLlama</a> • 
    <a href="https://mindsdb.com/">MindsDB</a> • 
    <a href="https://github.com/mindsdb/mindsdb">GitHub</a>
  </p>
</div> 