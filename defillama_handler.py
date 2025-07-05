import requests
from typing import Optional, Dict, Any
from mindsdb.integrations.libs.api_handler import APIHandler
from mindsdb.integrations.libs.response import (
    HandlerStatusResponse as StatusResponse,
    HandlerResponse as Response,
    RESPONSE_TYPE
)
from mindsdb.utilities import log
from mindsdb_sql_parser import parse_sql
from .defillama_tables import (
    ProtocolsTable,
    TVLTable,
    YieldsTable,
    StablecoinsTable,
    ChainsTable,
    TokensTable
)

logger = log.getLogger(__name__)


class DeFiLlamaHandler(APIHandler):
    """
    The DeFiLlama handler implementation.
    """
    
    name = 'defillama'
    
    def __init__(self, name: str, **kwargs):
        """
        Initialize the DeFiLlama handler.
        
        Args:
            name (str): The handler name
            kwargs: Connection arguments
        """
        super().__init__(name)
        
        # Connection parameters
        connection_data = kwargs.get('connection_data', {})
        self.base_url = connection_data.get('base_url', 'https://api.llama.fi')
        
        # API configuration
        self.headers = {
            'User-Agent': 'MindsDB-DeFiLlama-Handler/1.0',
            'Accept': 'application/json'
        }
        
        # Register available tables
        self._register_table('protocols', ProtocolsTable(self))
        self._register_table('tvl', TVLTable(self))
        self._register_table('yields', YieldsTable(self))
        self._register_table('stablecoins', StablecoinsTable(self))
        self._register_table('chains', ChainsTable(self))
        self._register_table('tokens', TokensTable(self))
        
    def connect(self) -> StatusResponse:
        """
        Set up any connections required by the handler.
        
        Returns:
            HandlerStatusResponse
        """
        try:
            # Test connection by making a simple API call
            response = self.call_defillama_api('/protocols')
            if response and isinstance(response, list):
                self.is_connected = True
                return StatusResponse(True)
            else:
                self.is_connected = False
                return StatusResponse(False, "Connection failed: Invalid response from DeFiLlama API")
        except Exception as e:
            self.is_connected = False
            logger.error(f"Error connecting to DeFiLlama: {e}")
            return StatusResponse(False, f"Connection failed: {str(e)}")
    
    def check_connection(self) -> StatusResponse:
        """
        Check if the connection is alive and healthy.
        
        Returns:
            HandlerStatusResponse
        """
        return self.connect()
    
    def native_query(self, query: str) -> Response:
        """
        Receive and process a raw query.
        
        Args:
            query (str): query in native format
            
        Returns:
            HandlerResponse
        """
        ast = parse_sql(query, dialect='mindsdb')
        return self.query(ast)
    
    def call_defillama_api(self, endpoint: str, params: Optional[Dict] = None) -> Any:
        """
        Call DeFiLlama API endpoint.
        
        Args:
            endpoint (str): API endpoint path
            params (dict): Optional query parameters
            
        Returns:
            API response data
        """
        # FIXED: Use correct subdomain based on endpoint
        if endpoint == '/yields':
            base_url = 'https://yields.llama.fi'
            url = base_url + '/pools'  # yields endpoint uses /pools
        elif endpoint == '/stablecoins':
            base_url = 'https://stablecoins.llama.fi'
            url = base_url + endpoint
        elif endpoint.startswith('/prices/'):
            base_url = 'https://coins.llama.fi'
            url = base_url + endpoint
        else:
            # Use main API for protocols, chains, charts, etc.
            base_url = 'https://api.llama.fi'
            url = base_url + endpoint
        
        try:
            response = requests.get(url, headers=self.headers, params=params or {})
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in API call: {e}")
            raise 