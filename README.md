# DeFiLlama Handler

The DeFiLlama handler for MindsDB provides seamless integration with the DeFiLlama API, enabling you to access comprehensive DeFi data including protocol information, Total Value Locked (TVL), yields, stablecoin data, and more directly from your MindsDB instance.

## Implementation

This handler is implemented using the DeFiLlama API and provides access to decentralized finance data through SQL queries.

## DeFiLlama API

DeFiLlama is the largest TVL aggregator for DeFi protocols. It provides comprehensive data on DeFi protocols, yields, stablecoins, and blockchain TVL across multiple chains. The API is free to use and doesn't require authentication for basic endpoints.

## Connection

### Parameters

* `base_url`: DeFiLlama API base URL (default: `https://api.llama.fi`)

### Example Connection

```sql
CREATE DATABASE defillama_datasource
WITH 
  ENGINE = 'defillama',
  PARAMETERS = {
    "base_url": "https://api.llama.fi"
  };
```

## Usage

### Available Tables

The DeFiLlama handler provides access to the following tables:

* `protocols` - DeFi protocol information and metrics  
* `tvl` - Total Value Locked historical data
* `yields` - Yield farming and staking data
* `stablecoins` - Stablecoin metrics and circulation data
* `chains` - Blockchain information and TVL data
* `tokens` - Token price data

### Basic Queries

#### Get All DeFi Protocols

```sql
SELECT name, tvl, chain, category, change_7d
FROM defillama_datasource.protocols 
ORDER BY tvl DESC 
LIMIT 20;
```

#### Get Specific Protocol Information

```sql
SELECT * 
FROM defillama_datasource.protocols 
WHERE slug = 'uniswap';
```

#### Get Top Yield Opportunities

```sql
SELECT project, chain, symbol, apy, tvlUsd
FROM defillama_datasource.yields 
WHERE apy > 10 
ORDER BY apy DESC 
LIMIT 15;
```

#### Get Stablecoin Market Data

```sql
SELECT name, symbol, circulating, chains
FROM defillama_datasource.stablecoins 
ORDER BY circulating DESC 
LIMIT 10;
```

#### Get Chain TVL Data

```sql
SELECT name, tvl, tokenSymbol
FROM defillama_datasource.chains 
ORDER BY tvl DESC;
```

#### Get Historical TVL for Ethereum

```sql
SELECT date, totalLiquidityUSD
FROM defillama_datasource.tvl 
WHERE chain = 'Ethereum' 
ORDER BY date DESC 
LIMIT 30;
```

### Advanced Queries

#### Cross-Chain DeFi Analysis

```sql
SELECT 
    chain,
    COUNT(*) as protocol_count,
    AVG(apy) as avg_apy,
    SUM(tvlUsd) as total_tvl
FROM defillama_datasource.yields 
WHERE apy > 0 
GROUP BY chain 
ORDER BY total_tvl DESC;
```

#### Yield Farming Opportunities by Category

```sql
SELECT 
    p.category,
    y.project,
    y.apy,
    y.tvlUsd,
    y.chain
FROM defillama_datasource.protocols p
JOIN defillama_datasource.yields y ON p.name = y.project
WHERE y.apy > 15 AND y.tvlUsd > 1000000
ORDER BY y.apy DESC;
```

## Supported Columns

### Protocols Table

| Column | Description |
|--------|-------------|
| id | Protocol unique identifier |
| name | Protocol name |
| address | Contract address |
| symbol | Protocol token symbol |
| url | Official website |
| description | Protocol description |
| chain | Primary blockchain |
| logo | Logo URL |
| category | Protocol category |
| tvl | Total Value Locked |
| change_7d | 7-day TVL change percentage |

### TVL Table

| Column | Description |
|--------|-------------|
| date | Date timestamp |
| totalLiquidityUSD | Total liquidity in USD |
| chain | Blockchain name |
| protocol | Protocol name |

### Yields Table  

| Column | Description |
|--------|-------------|
| pool | Pool identifier |
| chain | Blockchain name |
| project | Project name |
| symbol | Token symbol |
| tvlUsd | Pool TVL in USD |
| apy | Annual Percentage Yield |
| apyBase | Base APY without rewards |
| apyReward | Reward APY |

### Stablecoins Table

| Column | Description |
|--------|-------------|
| id | Stablecoin ID |
| name | Stablecoin name |
| symbol | Stablecoin symbol |
| pegType | Peg mechanism type |
| circulating | Circulating supply |
| chains | Supported chains |

### Chains Table

| Column | Description |
|--------|-------------|
| name | Chain name |
| tvl | Total Value Locked |
| tokenSymbol | Native token symbol |
| chainId | Chain ID |

### Tokens Table

| Column | Description |
|--------|-------------|
| address | Token contract address |
| chain | Blockchain name |
| symbol | Token symbol |
| name | Token name |
| price | Current price |

## Rate Limits

DeFiLlama API is free and doesn't enforce strict rate limits, but please be respectful:

* Don't make excessive concurrent requests
* Cache results when possible
* Use appropriate delays between requests

## Troubleshooting

### Common Issues

**"Connection Failed" Error**

* Check your internet connection
* Verify the DeFiLlama API is accessible
* Try with default base_url parameter

**"No Data Returned" Error**

* Verify the endpoint supports the requested data
* Check if filters are too restrictive
* Some endpoints may require specific parameters

## Data Freshness

* Protocol data: Updated regularly
* TVL data: Updated daily
* Yields data: Updated every few hours
* Stablecoin data: Updated regularly
* Token prices: Real-time when available

## Resources

* [DeFiLlama Website](https://defillama.com/)
* [DeFiLlama API Documentation](https://docs.llama.fi/)
* [MindsDB Documentation](https://docs.mindsdb.com/)

## Support

For issues related to:
* MindsDB integration: Check MindsDB documentation
* DeFiLlama data: Visit DeFiLlama website
* API endpoints: Refer to DeFiLlama API docs 