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
    
    def add_tool(self, tool_name: str, tool_function: callable):
        """
        Add a new tool to the registry.
        
        Args:
            tool_name: Name of the tool
            tool_function: Function to execute for this tool
        """
        self.tool_registry[tool_name] = tool_function
        logger.info(f"Added tool '{tool_name}' to registry")
    
    def remove_tool(self, tool_name: str):
        """
        Remove a tool from the registry.
        
        Args:
            tool_name: Name of the tool to remove
        """
        if tool_name in self.tool_registry:
            del self.tool_registry[tool_name]
            logger.info(f"Removed tool '{tool_name}' from registry")
        else:
            logger.warning(f"Tool '{tool_name}' not found in registry")
    
    def list_tools(self) -> list:
        """
        Get list of available tools.
        
        Returns:
            List of available tool names
        """
        return list(self.tool_registry.keys())
    
    def get_tool_info(self) -> Dict[str, str]:
        """
        Get information about all available tools.
        
        Returns:
            Dictionary mapping tool names to their descriptions
        """
        tool_info = {}
        for tool_name, tool_func in self.tool_registry.items():
            # Try to get docstring or use default description
            description = getattr(tool_func, '__doc__', 'No description available')
            if description:
                description = description.strip().split('\n')[0]  # First line only
            else:
                description = f"Tool function for {tool_name}"
            tool_info[tool_name] = description
        
        return tool_info


class ToolExecutionError(Exception):
    """Custom exception for tool execution errors."""
    def __init__(self, tool_name: str, message: str, original_error: Exception = None):
        self.tool_name = tool_name
        self.original_error = original_error
        super().__init__(f"Tool '{tool_name}' failed: {message}")


class ToolTimeoutError(ToolExecutionError):
    """Custom exception for tool timeout errors."""
    def __init__(self, tool_name: str, timeout: int):
        super().__init__(tool_name, f"Execution timed out after {timeout} seconds")


# Utility function for safe tool execution
def safe_execute_tool(tool_executor: ToolExecutor, tool_name: str, tool_input: Dict[str, Any], 
                     timeout: int = 30, max_retries: int = 1) -> Dict[str, Any]:
    """
    Safely execute a tool with retry logic and comprehensive error handling.
    
    Args:
        tool_executor: ToolExecutor instance
        tool_name: Name of the tool to execute
        tool_input: Input parameters for the tool
        timeout: Maximum execution time in seconds
        max_retries: Maximum number of retry attempts
        
    Returns:
        Dictionary containing execution result and metadata
    """
    for attempt in range(max_retries + 1):
        try:
            result = tool_executor.execute_tool(tool_name, tool_input, timeout)
            return {
                "success": True,
                "result": result,
                "attempts": attempt + 1,
                "error": None
            }
        except Exception as e:
            if attempt < max_retries:
                logger.warning(f"Tool '{tool_name}' failed on attempt {attempt + 1}, retrying...")
                time.sleep(1)  # Brief delay before retry
            else:
                logger.error(f"Tool '{tool_name}' failed after {attempt + 1} attempts")
                return {
                    "success": False,
                    "result": None,
                    "attempts": attempt + 1,
                    "error": str(e)
                }
