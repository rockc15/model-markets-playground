#!/usr/bin/env python3
"""
Test script for web search functionality with conversation history and citations.
"""

import anthropic
import yaml
import json
from conversation_manager import ConversationManager
from tools.tools import anthropic_tools

def load_config():
    """Load configuration from YAML file."""
    try:
        with open('config.yaml', 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print("Error: config.yaml not found. Please create a configuration file.")
        return None
    except yaml.YAMLError as e:
        print(f"Error parsing config.yaml: {e}")
        return None

def test_web_search_conversation():
    """Test the conversation manager with web search functionality."""
    
    # Load configuration
    config = load_config()
    if not config:
        return
    
    # Initialize Anthropic client
    try:
        client = anthropic.Anthropic(api_key=config['anthropic']['api_key'])
    except Exception as e:
        print(f"Error initializing Anthropic client: {e}")
        return
    
    # Initialize conversation manager
    conversation_manager = ConversationManager(client, config)
    
    # Test prompt that should trigger web search
    test_prompt = """
    I want to analyze Tesla (TSLA) stock. Please:
    1. Get the current stock data for Tesla
    2. Search the web for recent Tesla news and developments
    3. Get market overview for context
    4. Provide a comprehensive analysis and recommendation
    
    Make sure to use web search to get the latest news and information about Tesla.
    """
    
    print("🚀 Starting conversation with web search test...")
    print(f"Prompt: {test_prompt}")
    print("\n" + "="*80 + "\n")
    
    try:
        # Start conversation
        result = conversation_manager.start_conversation(test_prompt, anthropic_tools)
        
        # Display results
        print("📊 CONVERSATION RESULTS:")
        print("="*50)
        print(f"Final Response:\n{result['final_response']}")
        print("\n" + "="*50)
        
        # Display conversation metadata
        print("📈 CONVERSATION METADATA:")
        print(f"• Iterations used: {result['iterations_used']}")
        print(f"• Tools executed: {result['tools_executed']}")
        print(f"• Web search used: {result.get('web_search_used', False)}")
        print(f"• Web search count: {result.get('web_search_count', 0)}")
        print(f"• Citations found: {len(result.get('citations', []))}")
        print(f"• Conversation length: {result['conversation_length']}")
        
        # Display web search history
        if result.get('web_search_history'):
            print("\n🔍 WEB SEARCH HISTORY:")
            for i, search in enumerate(result['web_search_history'], 1):
                print(f"{i}. Query: '{search['query']}'")
                print(f"   Timestamp: {search['timestamp']}")
        
        # Display citations
        if result.get('citations'):
            print("\n📚 CITATIONS:")
            for i, citation in enumerate(result['citations'], 1):
                print(f"{i}. {citation['title']}")
                print(f"   URL: {citation['url']}")
                if citation.get('snippet'):
                    print(f"   Snippet: {citation['snippet'][:100]}...")
                print()
        
        # Display tool summary
        print("\n🔧 TOOL EXECUTION SUMMARY:")
        for i, tool in enumerate(result['tool_summary'], 1):
            print(f"{i}. {tool['tool']} (Iteration {tool['iteration']})")
            print(f"   Input: {tool['input']}")
            result_preview = str(tool['result'])[:100] + "..." if len(str(tool['result'])) > 100 else str(tool['result'])
            print(f"   Result: {result_preview}")
            print()
        
    except Exception as e:
        print(f"❌ Error during conversation: {e}")
        import traceback
        traceback.print_exc()

def test_simple_web_search():
    """Test just the web search tool directly."""
    from tool_executor import ToolExecutor
    
    print("🔍 Testing web search tool directly...")
    
    executor = ToolExecutor()
    
    try:
        result = executor.execute_tool("web_search", {"query": "Tesla stock news today", "max_results": 3})
        print("Web search result:")
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Error testing web search: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🧪 Web Search Test Suite")
    print("="*50)
    
    # Test 1: Direct web search tool
    print("\n1. Testing web search tool directly:")
    test_simple_web_search()
    
    print("\n" + "="*50)
    
    # Test 2: Full conversation with web search
    print("\n2. Testing full conversation with web search:")
    test_web_search_conversation()
    
    print("\n✅ Test completed!")
