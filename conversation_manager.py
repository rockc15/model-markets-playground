"""
Conversation Manager for Sequential Tool Execution
Handles multi-turn conversations with Claude, allowing sequential tool calls
until a final decision is reached.
"""

import anthropic
from typing import List, Dict, Any, Optional
import json
import logging
from datetime import datetime
from tool_executor import ToolExecutor

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConversationManager:
    def __init__(self, client: anthropic.Anthropic, config: Dict[str, Any]):
        """
        Initialize the conversation manager.
        
        Args:
            client: Anthropic client instance
            config: Configuration dictionary from YAML
        """
        self.client = client
        self.config = config
        self.tool_executor = ToolExecutor()
        self.conversation_history = []
        self.tool_results = []
        self.web_search_history = []  # Track web search queries and results
        self.citations = []  # Track sources for citation
        
        # Configuration parameters
        self.max_iterations = config.get('conversation', {}).get('max_iterations', 10)
        self.require_final_decision = config.get('conversation', {}).get('require_final_decision', True)
        self.tool_timeout = config.get('conversation', {}).get('tool_timeout', 30)
        
    def start_conversation(self, user_prompt: str, tools: List[Dict]) -> Dict[str, Any]:
        """
        Start a conversation with sequential tool execution.
        
        Args:
            user_prompt: Initial user query
            tools: List of available tools
            
        Returns:
            Dictionary containing final response and conversation summary
        """
        logger.info(f"Starting conversation with prompt: {user_prompt[:100]}...")
        
        # Initialize conversation with user prompt
        self.conversation_history = [
            {"role": "user", "content": user_prompt}
        ]
        
        iteration_count = 0
        final_response = None
        
        while iteration_count < self.max_iterations:
            iteration_count += 1
            logger.info(f"Conversation iteration {iteration_count}")
            
            try:
                # Get Claude's response
                response = self._get_claude_response(tools)
                
                # Add Claude's response to conversation history
                self._add_assistant_response(response)
                
                # Check if this is a final response (no tool calls)
                tool_calls = self._extract_tool_calls(response)
                
                if not tool_calls:
                    # No more tool calls - this is the final response
                    final_response = response
                    logger.info("Final response received - no more tool calls")
                    break
                
                # Execute tools and add results to conversation
                self._execute_and_add_tool_results(tool_calls)
                
            except Exception as e:
                logger.error(f"Error in conversation iteration {iteration_count}: {str(e)}")
                # Add error to conversation and continue
                self.conversation_history.append({
                    "role": "user", 
                    "content": f"Error occurred: {str(e)}. Please continue with available information."
                })
        
        if final_response is None:
            logger.warning(f"Reached max iterations ({self.max_iterations}) without final response")
            # Force a final response
            final_response = self._force_final_response(tools)
        
        return self._format_final_result(final_response, iteration_count)
    
    def _get_claude_response(self, tools: List[Dict]) -> Any:
        """Get response from Claude with current conversation history."""
        try:
            response = self.client.messages.create(
                model=self.config["agent"]["name"],
                max_tokens=self.config["agent"]["max_tokens"],
                temperature=self.config["agent"].get("temperature", 0.1),
                system=self._build_system_prompt(),
                tools=tools,
                messages=self.conversation_history
            )
            return response
        except Exception as e:
            logger.error(f"Error getting Claude response: {str(e)}")
            raise
    
    def _build_system_prompt(self) -> str:
        """Build enhanced system prompt for sequential tool execution."""
        base_prompt = self.config["agent"]["system_promt"]
        
        enhanced_prompt = f"""{base_prompt}

IMPORTANT INSTRUCTIONS FOR SEQUENTIAL TOOL EXECUTION:

1. You can call multiple tools in sequence to gather comprehensive information before making a final decision.

2. After each tool call, analyze the results and determine if you need more information:
   - If you need more data, call additional tools
   - If you have sufficient information, provide your final analysis and recommendation

3. When making tool calls:
   - Be strategic about which tools to use and in what order
   - Build upon previous tool results
   - Gather diverse data points for comprehensive analysis

4. For your final response:
   - Summarize all the information you gathered
   - Provide clear reasoning for your decision
   - Include confidence level in your recommendation
   - No more tool calls should be made in your final response

5. Available information from previous tool calls:
{self._format_tool_results_summary()}

Remember: You have the freedom to call multiple tools sequentially to gather all necessary information before making your final decision.
"""
        return enhanced_prompt
    
    def _add_assistant_response(self, response: Any):
        """Add Claude's response to conversation history."""
        content = []
        
        for block in response.content:
            if block.type == "text":
                content.append({
                    "type": "text",
                    "text": block.text
                })
            elif block.type == "tool_use":
                content.append({
                    "type": "tool_use",
                    "id": block.id,
                    "name": block.name,
                    "input": block.input
                })
        
        self.conversation_history.append({
            "role": "assistant",
            "content": content
        })
    
    def _extract_tool_calls(self, response: Any) -> List[Dict]:
        """Extract tool calls from Claude's response."""
        tool_calls = []
        
        for block in response.content:
            if block.type == "tool_use":
                tool_calls.append({
                    "id": block.id,
                    "name": block.name,
                    "input": block.input
                })
        
        return tool_calls
    
    def _execute_and_add_tool_results(self, tool_calls: List[Dict]):
        """Execute tools and add results to conversation history."""
        tool_results = []
        
        for tool_call in tool_calls:
            logger.info(f"Executing tool: {tool_call['name']} with input: {tool_call['input']}")
            
            try:
                # Execute the tool
                result = self.tool_executor.execute_tool(
                    tool_call['name'], 
                    tool_call['input'],
                    timeout=self.tool_timeout
                )
                
                # Special handling for web search tool
                if tool_call['name'] == 'web_search':
                    self._track_web_search(tool_call['input'], result)
                
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": tool_call["id"],
                    "content": json.dumps(result) if not isinstance(result, str) else result
                })
                
                # Store for summary
                self.tool_results.append({
                    "tool": tool_call['name'],
                    "input": tool_call['input'],
                    "result": result,
                    "iteration": len(self.conversation_history) // 2 + 1
                })
                
                logger.info(f"Tool {tool_call['name']} executed successfully")
                
            except Exception as e:
                logger.error(f"Error executing tool {tool_call['name']}: {str(e)}")
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": tool_call["id"],
                    "content": f"Error executing tool: {str(e)}"
                })
        
        # Add tool results to conversation
        if tool_results:
            self.conversation_history.append({
                "role": "user",
                "content": tool_results
            })
    
    def _track_web_search(self, search_input: Dict[str, Any], search_result: Any):
        """Track web search queries and extract citations."""
        query = search_input.get('query', '')
        
        # Store web search history
        search_entry = {
            "query": query,
            "timestamp": json.dumps(datetime.now(), default=str),
            "result": search_result
        }
        self.web_search_history.append(search_entry)
        
        # Extract citations from search result
        if isinstance(search_result, dict) and 'sources' in search_result:
            for source in search_result['sources']:
                citation = {
                    "url": source.get('url', ''),
                    "title": source.get('title', ''),
                    "snippet": source.get('snippet', ''),
                    "query": query
                }
                self.citations.append(citation)
        elif isinstance(search_result, str):
            # Try to extract URLs from string result (basic implementation)
            import re
            urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', search_result)
            for url in urls:
                citation = {
                    "url": url,
                    "title": f"Source for query: {query}",
                    "snippet": search_result[:200] + "..." if len(search_result) > 200 else search_result,
                    "query": query
                }
                self.citations.append(citation)
        
        logger.info(f"Tracked web search: {query} with {len(self.citations)} total citations")
    
    def _format_tool_results_summary(self) -> str:
        """Format a summary of all tool results for the system prompt."""
        if not self.tool_results:
            return "No previous tool results available."
        
        summary = "Previous tool results:\n"
        for i, result in enumerate(self.tool_results, 1):
            summary += f"{i}. {result['tool']}({result['input']}) -> {str(result['result'])[:200]}...\n"
        
        # Add web search history summary
        if self.web_search_history:
            summary += f"\nWeb Search History ({len(self.web_search_history)} searches):\n"
            for i, search in enumerate(self.web_search_history, 1):
                summary += f"  {i}. Query: '{search['query']}'\n"
        
        return summary
    
    def _force_final_response(self, tools: List[Dict]) -> Any:
        """Force a final response when max iterations reached."""
        self.conversation_history.append({
            "role": "user",
            "content": "Please provide your final analysis and recommendation based on all the information gathered so far. Do not make any more tool calls."
        })
        
        return self._get_claude_response([])  # No tools to force final response
    
    def _format_final_result(self, final_response: Any, iterations: int) -> Dict[str, Any]:
        """Format the final result with conversation summary and web search citations."""
        
        # Extract text content from final response
        final_text = ""
        for block in final_response.content:
            if block.type == "text":
                final_text += block.text
        
        # Add web search usage indicator and citations to final response
        if self.web_search_history:
            final_text += "\n\n" + "="*50
            final_text += f"\n🔍 WEB SEARCH USED: {len(self.web_search_history)} search(es) performed"
            final_text += "\n" + "="*50
            
            # Add search queries
            final_text += "\n\nSearch Queries:"
            for i, search in enumerate(self.web_search_history, 1):
                final_text += f"\n{i}. {search['query']}"
            
            # Add citations if available
            if self.citations:
                final_text += "\n\nSources & Citations:"
                for i, citation in enumerate(self.citations, 1):
                    final_text += f"\n{i}. {citation['title']}"
                    final_text += f"\n   URL: {citation['url']}"
                    if citation['snippet']:
                        final_text += f"\n   Summary: {citation['snippet']}"
                    final_text += "\n"
        
        return {
            "final_response": final_text,
            "iterations_used": iterations,
            "tools_executed": len(self.tool_results),
            "tool_summary": self.tool_results,
            "web_search_used": len(self.web_search_history) > 0,
            "web_search_count": len(self.web_search_history),
            "web_search_history": self.web_search_history,
            "citations": self.citations,
            "conversation_length": len(self.conversation_history),
            "success": True
        }
