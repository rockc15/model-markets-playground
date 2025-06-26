# Web Search Features Documentation

## Overview

The conversation manager now includes enhanced web search functionality with conversation history tracking and automatic citation generation. This allows the AI agent to search the web for current information and properly cite sources in the final output.

## New Features

### 1. Web Search Tool
- **Function**: `web_search`
- **Description**: Searches the web for current information using DuckDuckGo
- **Input Parameters**:
  - `query` (required): The search query string
  - `max_results` (optional): Maximum number of results to return (default: 5, max: 10)

### 2. Conversation History Tracking
- Tracks all web search queries and results
- Stores timestamps for each search
- Maintains search context throughout the conversation

### 3. Automatic Citation Generation
- Extracts URLs, titles, and snippets from search results
- Automatically formats citations in the final output
- Links citations back to original search queries

### 4. Enhanced Final Output
- Indicates when web search was used
- Shows number of searches performed
- Lists all search queries
- Provides formatted citations with URLs and summaries

## Usage Examples

### Basic Web Search
```python
from tool_executor import ToolExecutor

executor = ToolExecutor()
result = executor.execute_tool("web_search", {
    "query": "Tesla stock news today",
    "max_results": 5
})
```

### Full Conversation with Web Search
```python
from conversation_manager import ConversationManager
from tools.tools import anthropic_tools

# Initialize conversation manager
conversation_manager = ConversationManager(client, config)

# Prompt that triggers web search
prompt = """
Analyze Apple stock and search for recent news about the company.
Provide a comprehensive analysis with current market information.
"""

result = conversation_manager.start_conversation(prompt, anthropic_tools)
```

## Output Format

When web search is used, the final output includes:

```
[Original AI Response]

==================================================
🔍 WEB SEARCH USED: 2 search(es) performed
==================================================

Search Queries:
1. Apple stock news today
2. Apple earnings report 2024

Sources & Citations:
1. Apple Reports Strong Q4 Earnings
   URL: https://example.com/apple-earnings
   Summary: Apple reported better than expected earnings...

2. Apple Stock Analysis - Market Watch
   URL: https://example.com/apple-analysis
   Summary: Technical analysis shows Apple stock trending...
```

## Technical Implementation

### ConversationManager Updates
- Added `web_search_history` list to track searches
- Added `citations` list to store source information
- Enhanced `_track_web_search()` method for citation extraction
- Updated `_format_final_result()` to include web search indicators

### ToolExecutor Updates
- Implemented `_web_search_tool()` with DuckDuckGo integration
- Added structured result format with sources array
- Included error handling for missing dependencies
- Added timeout and retry logic

### Tool Schema
- Properly defined web_search tool in `anthropic_tools`
- Added input validation for query and max_results
- Included comprehensive tool description

## Dependencies

Required packages (already in requirements.txt):
- `requests`: For HTTP requests to search engines
- `beautifulsoup4`: For parsing HTML search results
- `urllib.parse`: For URL encoding (built-in)

## Testing

Run the test suite to verify functionality:

```bash
python test_web_search.py
```

This will test:
1. Direct web search tool execution
2. Full conversation flow with web search
3. Citation extraction and formatting
4. Error handling

## Configuration

No additional configuration required. The web search tool uses:
- DuckDuckGo as the search engine (no API key needed)
- Default timeout of 10 seconds per search
- User-Agent string to avoid blocking

## Error Handling

The system handles various error scenarios:
- Missing dependencies (requests/beautifulsoup4)
- Network connectivity issues
- Search engine blocking/rate limiting
- Malformed search results
- Timeout errors

In case of errors, the tool returns a structured error response with:
- Error message
- Search query that failed
- `search_performed: false` flag

## Future Enhancements

Potential improvements:
1. Support for multiple search engines (Google, Bing)
2. API key integration for premium search services
3. Advanced result filtering and ranking
4. Image and video search capabilities
5. Search result caching to avoid duplicate queries
6. Custom citation formatting options

## Troubleshooting

### Common Issues

1. **No search results returned**
   - Check internet connectivity
   - Verify search query is not too specific
   - Try different search terms

2. **Missing dependencies error**
   ```bash
   pip install requests beautifulsoup4
   ```

3. **Search timeout**
   - Increase timeout in tool_executor.py
   - Check network stability

4. **Rate limiting**
   - Add delays between searches
   - Use different search engines
   - Implement request throttling

### Debug Mode

Enable debug logging to troubleshoot issues:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

This will show detailed information about:
- Search requests being made
- HTML parsing results
- Citation extraction process
- Error details
