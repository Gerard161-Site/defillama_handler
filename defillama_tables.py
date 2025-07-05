from typing import List, Optional, Dict, Any
from mindsdb.integrations.libs.api_handler import APITable
from mindsdb.integrations.utilities.sql_utils import extract_comparison_conditions
from mindsdb_sql_parser.ast import Constant
import pandas as pd


class ProtocolsTable(APITable):
    """Table for DeFi protocols data."""
    
    def get_columns(self) -> List[str]:
        return [
            'id', 'name', 'address', 'symbol', 'url', 'description', 'chain',
            'logo', 'audits', 'audit_note', 'gecko_id', 'cmcId', 'category',
            'chains', 'module', 'twitter', 'forked_from', 'oracles',
            'slug', 'tvl', 'chainTvls', 'change_1h', 'change_1d', 'change_7d',
            'tokenBreakdowns', 'mcap'
        ]
    
    def select(self, query) -> pd.DataFrame:
        """Get DeFi protocols data."""
        conditions = extract_comparison_conditions(query.where)
        
        # Parse conditions
        protocol_name = None
        protocol_slug = None
        
        for op, arg1, arg2 in conditions:
            if arg1 == 'name' and op == '=':
                protocol_name = arg2
            elif arg1 == 'slug' and op == '=':
                protocol_slug = arg2
        
        # Get data from API
        if protocol_slug:
            # Get specific protocol data
            response = self.handler.call_defillama_api(f'/protocol/{protocol_slug}')
            if response:
                return pd.DataFrame([self._process_protocol_detail(response)], columns=self.get_columns())
        else:
            # Get all protocols
            response = self.handler.call_defillama_api('/protocols')
            if response and isinstance(response, list):
                rows = []
                for protocol in response:
                    if protocol_name and protocol.get('name', '').lower() != protocol_name.lower():
                        continue
                    rows.append(self._process_protocol_data(protocol))
                return pd.DataFrame(rows, columns=self.get_columns())
        
        return pd.DataFrame(columns=self.get_columns())
    
    def _process_protocol_data(self, protocol: Dict) -> List:
        """Process individual protocol data from /protocols endpoint."""
        return [
            protocol.get('id'),
            protocol.get('name'),
            protocol.get('address'),
            protocol.get('symbol'),
            protocol.get('url'),
            protocol.get('description'),
            protocol.get('chain'),
            protocol.get('logo'),
            protocol.get('audits'),
            protocol.get('audit_note'),
            protocol.get('gecko_id'),
            protocol.get('cmcId'),
            protocol.get('category'),
            ','.join(protocol.get('chains', [])) if protocol.get('chains') else None,
            protocol.get('module'),
            protocol.get('twitter'),
            ','.join(protocol.get('forked_from', [])) if protocol.get('forked_from') else None,
            ','.join(protocol.get('oracles', [])) if protocol.get('oracles') else None,
            protocol.get('slug'),
            protocol.get('tvl'),
            str(protocol.get('chainTvls', {})) if protocol.get('chainTvls') else None,
            protocol.get('change_1h'),
            protocol.get('change_1d'),
            protocol.get('change_7d'),
            str(protocol.get('tokenBreakdowns', {})) if protocol.get('tokenBreakdowns') else None,
            protocol.get('mcap')
        ]
    
    def _process_protocol_detail(self, protocol: Dict) -> List:
        """Process detailed protocol data from /protocol/{slug} endpoint."""
        return [
            protocol.get('id'),
            protocol.get('name'),
            protocol.get('address'),
            protocol.get('symbol'),
            protocol.get('url'),
            protocol.get('description'),
            protocol.get('chain'),
            protocol.get('logo'),
            protocol.get('audits'),
            protocol.get('audit_note'),
            protocol.get('gecko_id'),
            protocol.get('cmcId'),
            protocol.get('category'),
            ','.join(protocol.get('chains', [])) if protocol.get('chains') else None,
            protocol.get('module'),
            protocol.get('twitter'),
            ','.join(protocol.get('forked_from', [])) if protocol.get('forked_from') else None,
            ','.join(protocol.get('oracles', [])) if protocol.get('oracles') else None,
            protocol.get('slug'),
            protocol.get('tvl'),
            str(protocol.get('chainTvls', {})) if protocol.get('chainTvls') else None,
            protocol.get('change_1h'),
            protocol.get('change_1d'),
            protocol.get('change_7d'),
            str(protocol.get('tokenBreakdowns', {})) if protocol.get('tokenBreakdowns') else None,
            protocol.get('mcap')
        ]


class TVLTable(APITable):
    """Table for Total Value Locked (TVL) data."""
    
    def get_columns(self) -> List[str]:
        return [
            'date', 'totalLiquidityUSD', 'chain', 'protocol'
        ]
    
    def select(self, query) -> pd.DataFrame:
        """Get TVL data."""
        conditions = extract_comparison_conditions(query.where)
        
        # Parse conditions
        chain = None
        protocol = None
        
        for op, arg1, arg2 in conditions:
            if arg1 == 'chain' and op == '=':
                chain = arg2
            elif arg1 == 'protocol' and op == '=':
                protocol = arg2
        
        # Get data from API
        if chain:
            response = self.handler.call_defillama_api(f'/charts/{chain}')
        elif protocol:
            response = self.handler.call_defillama_api(f'/protocol/{protocol}')
            if response and 'chainTvls' in response:
                # Process historical TVL data from protocol
                tvl_data = response.get('tvl', [])
                rows = []
                for entry in tvl_data:
                    rows.append([
                        entry.get('date'),
                        entry.get('totalLiquidityUSD'),
                        'all',
                        protocol
                    ])
                return pd.DataFrame(rows, columns=self.get_columns())
        else:
            response = self.handler.call_defillama_api('/charts')
        
        if response and isinstance(response, list):
            rows = []
            for entry in response:
                rows.append([
                    entry.get('date'),
                    entry.get('totalLiquidityUSD'),
                    chain or 'all',
                    protocol or 'all'
                ])
            return pd.DataFrame(rows, columns=self.get_columns())
        
        return pd.DataFrame(columns=self.get_columns())


class YieldsTable(APITable):
    """Table for yield farming data."""
    
    def get_columns(self) -> List[str]:
        return [
            'pool', 'chain', 'project', 'symbol', 'tvlUsd', 'apy', 'apyBase',
            'apyReward', 'rewardTokens', 'count', 'outlier', 'il7d', 'apyBase7d',
            'apyMean30d', 'volumeUsd1d', 'volumeUsd7d', 'apyBaseInception',
            'mu', 'sigma', 'count', 'predictions'
        ]
    
    def select(self, query) -> pd.DataFrame:
        """Get yield farming data."""
        conditions = extract_comparison_conditions(query.where)
        
        # Parse conditions
        chain = None
        project = None
        
        for op, arg1, arg2 in conditions:
            if arg1 == 'chain' and op == '=':
                chain = arg2
            elif arg1 == 'project' and op == '=':
                project = arg2
        
        # Get data from API
        response = self.handler.call_defillama_api('/yields')
        
        if response and 'data' in response:
            rows = []
            for pool in response['data']:
                # Filter by conditions
                if chain and pool.get('chain', '').lower() != chain.lower():
                    continue
                if project and pool.get('project', '').lower() != project.lower():
                    continue
                
                rows.append([
                    pool.get('pool'),
                    pool.get('chain'),
                    pool.get('project'),
                    pool.get('symbol'),
                    pool.get('tvlUsd'),
                    pool.get('apy'),
                    pool.get('apyBase'),
                    pool.get('apyReward'),
                    ','.join(pool.get('rewardTokens', [])) if pool.get('rewardTokens') else None,
                    pool.get('count'),
                    pool.get('outlier'),
                    pool.get('il7d'),
                    pool.get('apyBase7d'),
                    pool.get('apyMean30d'),
                    pool.get('volumeUsd1d'),
                    pool.get('volumeUsd7d'),
                    pool.get('apyBaseInception'),
                    pool.get('mu'),
                    pool.get('sigma'),
                    pool.get('count'),
                    str(pool.get('predictions', {})) if pool.get('predictions') else None
                ])
            return pd.DataFrame(rows, columns=self.get_columns())
        
        return pd.DataFrame(columns=self.get_columns())


class StablecoinsTable(APITable):
    """Table for stablecoin data."""
    
    def get_columns(self) -> List[str]:
        return [
            'id', 'name', 'symbol', 'gecko_id', 'pegType', 'pegMechanism',
            'circulating', 'circulatingPrevDay', 'circulatingPrevWeek',
            'circulatingPrevMonth', 'chains', 'chainCirculating', 'price',
            'delisted', 'mintRedeemDescription'
        ]
    
    def select(self, query) -> pd.DataFrame:
        """Get stablecoin data."""
        conditions = extract_comparison_conditions(query.where)
        
        # Parse conditions
        stablecoin_id = None
        include_prices = False
        
        for op, arg1, arg2 in conditions:
            if arg1 == 'id' and op == '=':
                stablecoin_id = arg2
            elif arg1 == 'include_prices' and op == '=':
                include_prices = bool(arg2)
        
        # Get data from API
        endpoint = '/stablecoins'
        if include_prices:
            endpoint += '?includePrices=true'
        
        response = self.handler.call_defillama_api(endpoint)
        
        # FIXED: Stablecoins API returns 'peggedAssets' not 'stablecoins'
        if response and 'peggedAssets' in response:
            rows = []
            for stablecoin in response['peggedAssets']:
                # Filter by conditions
                if stablecoin_id and str(stablecoin.get('id')) != str(stablecoin_id):
                    continue
                
                rows.append([
                    stablecoin.get('id'),
                    stablecoin.get('name'),
                    stablecoin.get('symbol'),
                    stablecoin.get('gecko_id'),
                    stablecoin.get('pegType'),
                    stablecoin.get('pegMechanism'),
                    stablecoin.get('circulating', {}).get('peggedUSD'),
                    stablecoin.get('circulatingPrevDay', {}).get('peggedUSD'),
                    stablecoin.get('circulatingPrevWeek', {}).get('peggedUSD'),
                    stablecoin.get('circulatingPrevMonth', {}).get('peggedUSD'),
                    ','.join(stablecoin.get('chains', [])) if stablecoin.get('chains') else None,
                    str(stablecoin.get('chainCirculating', {})) if stablecoin.get('chainCirculating') else None,
                    stablecoin.get('price'),
                    stablecoin.get('delisted'),
                    stablecoin.get('mintRedeemDescription')
                ])
            return pd.DataFrame(rows, columns=self.get_columns())
        
        return pd.DataFrame(columns=self.get_columns())


class ChainsTable(APITable):
    """Table for blockchain chains data."""
    
    def get_columns(self) -> List[str]:
        return [
            'gecko_id', 'tvl', 'tokenSymbol', 'cmcId', 'name', 'chainId'
        ]
    
    def select(self, query) -> pd.DataFrame:
        """Get chains data."""
        response = self.handler.call_defillama_api('/chains')
        
        if response and isinstance(response, list):
            rows = []
            for chain in response:
                rows.append([
                    chain.get('gecko_id'),
                    chain.get('tvl'),
                    chain.get('tokenSymbol'),
                    chain.get('cmcId'),
                    chain.get('name'),
                    chain.get('chainId')
                ])
            return pd.DataFrame(rows, columns=self.get_columns())
        
        return pd.DataFrame(columns=self.get_columns())


class TokensTable(APITable):
    """Table for token price data."""
    
    def get_columns(self) -> List[str]:
        return [
            'address', 'chain', 'symbol', 'name', 'decimals', 'price',
            'timestamp', 'confidence'
        ]
    
    def select(self, query) -> pd.DataFrame:
        """Get token price data."""
        conditions = extract_comparison_conditions(query.where)
        
        # Parse conditions
        chain = None
        address = None
        
        for op, arg1, arg2 in conditions:
            if arg1 == 'chain' and op == '=':
                chain = arg2
            elif arg1 == 'address' and op == '=':
                address = arg2
        
        if chain and address:
            # Get specific token price
            token_id = f'{chain}:{address}'
            response = self.handler.call_defillama_api(f'/prices/current/{token_id}')
            
            if response and 'coins' in response:
                rows = []
                for token_key, token_data in response['coins'].items():
                    rows.append([
                        token_data.get('address', address),
                        chain,
                        token_data.get('symbol'),
                        token_data.get('name'),
                        token_data.get('decimals'),
                        token_data.get('price'),
                        token_data.get('timestamp'),
                        token_data.get('confidence')
                    ])
                return pd.DataFrame(rows, columns=self.get_columns())
        
        return pd.DataFrame(columns=self.get_columns()) 