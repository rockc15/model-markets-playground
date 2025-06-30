"""
Tool Executor for Sequential Tool Execution
Handles the execution of individual tools with error handling and timeout support.
"""

import time
import logging
from typing import Dict, Any, Optional
from concurrent.futures import ThreadPoolExecutor, TimeoutError
import signal
from contextlib import contextmanager

# Import tool functions
from tools.tools import (
    get_stock_data_tool,
    get_market_overview_tool,
    buy_stock_tool,
    sell_stock_tool,
    hold_stock_tool
)

logger = logging.getLogger(__name__)

class ToolExecutor:
    def __init__(self):
        """Initialize the tool executor with available tools."""
        self.tool_registry = {
            "get_stock_data": get_stock_data_tool,
            "get_market_overview": get_market_overview_tool,
            "buy_stock": buy_stock_tool,
            "sell_stock": sell_stock_tool,
            "hold_stock": hold_stock_tool,
            "web_search": self._web_search_tool,  # Placeholder for web search
        }
        
    def execute_tool(self, tool_name: str, tool_input: Dict[str, Any], timeout: int = 30) -> Any:
        """
        Execute a tool with the given input and timeout.
        
        Args:
            tool_name: Name of the tool to execute
            tool_input: Input parameters for the tool
            timeout: Maximum execution time in seconds
            
        Returns:
            Tool execution result
            
        Raises:
            ValueError: If tool is not found
            TimeoutError: If tool execution exceeds timeout
            Exception: For other tool execution errors
        """
        if tool_name not in self.tool_registry:
            available_tools = list(self.tool_registry.keys())
            raise ValueError(f"Tool '{tool_name}' not found. Available tools: {available_tools}")
        
        tool_function = self.tool_registry[tool_name]
        
        logger.info(f"Executing tool '{tool_name}' with input: {tool_input}")
        start_time = time.time()
        
        try:
            # Execute tool with timeout
            with ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(tool_function, tool_input)
                try:
                    result = future.result(timeout=timeout)
                    execution_time = time.time() - start_time
                    logger.info(f"Tool '{tool_name}' completed in {execution_time:.2f}s")
                    return result
                except TimeoutError:
                    logger.error(f"Tool '{tool_name}' timed out after {timeout}s")
                    raise TimeoutError(f"Tool '{tool_name}' execution timed out after {timeout} seconds")
                    
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"Tool '{tool_name}' failed after {execution_time:.2f}s: {str(e)}")
            raise Exception(f"Tool '{tool_name}' execution failed: {str(e)}")
    
    def _web_search_tool(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enhanced web search tool implementation with structured results.
        Uses requests and BeautifulSoup for basic web scraping as a fallback.
        """
        query = inputs.get("query", "")
        max_results = inputs.get("max_results", 5)
        
        logger.info(f"Web search requested for: {query}")
        
        try:
            # Try to use DuckDuckGo search as a free alternative
            import requests
            from bs4 import BeautifulSoup
            import urllib.parse
            
            # DuckDuckGo Instant Answer API (free, no API key required)
            search_url = f"https://duckduckgo.com/html/?q={urllib.parse.quote(query)}"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(search_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract search results
            results = []
            search_results = soup.find_all('div', class_='result')[:max_results]
            
            for result in search_results:
                title_elem = result.find('a', class_='result__a')
                snippet_elem = result.find('a', class_='result__snippet')
                
                if title_elem:
                    title = title_elem.get_text(strip=True)
                    url = title_elem.get('href', '')
                    snippet = snippet_elem.get_text(strip=True) if snippet_elem else ""
                    
                    results.append({
                        "title": title,
                        "url": url,
                        "snippet": snippet
                    })
            
            if not results:
                # Fallback: return a structured response indicating no results
                return {
                    "query": query,
                    "sources": [],
                    "summary": f"No web search results found for '{query}'. This may be due to search limitations or network issues.",
                    "search_performed": True
                }
            
            return {
                "query": query,
                "sources": results,
                "summary": f"Found {len(results)} web search results for '{query}'",
                "search_performed": True
            }
            
        except ImportError:
            logger.warning("requests or beautifulsoup4 not installed. Install with: pip install requests beautifulsoup4")
            return {
                "query": query,
                "sources": [],
                "summary": f"Web search for '{query}' - Missing dependencies (requests, beautifulsoup4). Please install required packages.",
                "search_performed": False,
                "error": "Missing dependencies"
            }
        except Exception as e:
            logger.error(f"Web search failed: {str(e)}")
            return {
                "query": query,
                "sources": [],
                "summary": f"Web search for '{query}' failed due to: {str(e)}",
                "search_performed": False,
                "error": str(e)
            }
    
