#!/usr/bin/env python3
"""
Test script to demonstrate sequential tool execution capabilities
"""

import os
import yaml
from dotenv import load_dotenv
import anthropic
from conversation_manager import ConversationManager
from tools.tools import anthropic_tools

def test_sequential_execution():
    """Test the sequential tool execution with different scenarios."""
    
    # Load environment
    load_dotenv()
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ ANTHROPIC_API_KEY not found")
        return
    
    # Initialize client
    client = anthropic.Anthropic(api_key=api_key)
    
    # Test configuration
    test_config = {
        "agent": {
            "name": "claude-3-5-haiku-latest",
            "max_tokens": 1500,
            "temperature": 0.1,
            "system_promt": "You are a financial analysis agent. Use multiple tools to gather comprehensive information before making decisions."
        },
        "conversation": {
            "max_iterations": 5,
            "require_final_decision": True,
            "tool_timeout": 30
        }
    }
    
    # Test scenarios
    test_scenarios = [
        {
            "name": "Quick Stock Analysis",
            "prompt": "Should I buy AAPL stock? Give me a quick analysis.",
            "expected_tools": ["get_stock_data", "get_market_overview"]
        },
        {
            "name": "Market Comparison",
            "prompt": "Compare TSLA and NVDA stocks and recommend which one to buy.",
            "expected_tools": ["get_stock_data", "get_market_overview"]
        },
        {
            "name": "Market Overview Only",
            "prompt": "What's the current state of the stock market?",
            "expected_tools": ["get_market_overview"]
        }
    ]
    
    print("🧪 TESTING SEQUENTIAL TOOL EXECUTION SYSTEM")
    print("=" * 60)
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n📋 Test {i}: {scenario['name']}")
        print(f"Query: {scenario['prompt']}")
        print("-" * 40)
        
        try:
            # Initialize conversation manager
            conversation_manager = ConversationManager(client, test_config)
            
            # Run the test
            result = conversation_manager.start_conversation(scenario['prompt'], anthropic_tools)
            
            # Display results
            print(f"✅ Success: {result['success']}")
            print(f"🔄 Iterations: {result['iterations_used']}")
            print(f"🔧 Tools used: {result['tools_executed']}")
            
            if result['tool_summary']:
                print("📊 Tools executed:")
                for tool in result['tool_summary']:
                    print(f"   • {tool['tool']}({tool['input']})")
            
            print(f"💬 Response length: {len(result['final_response'])} characters")
            print(f"📝 Final response preview: {result['final_response'][:100]}...")
            
        except Exception as e:
            print(f"❌ Test failed: {str(e)}")
        
        print("-" * 40)
    
    print("\n🎉 Sequential tool execution testing complete!")

if __name__ == "__main__":
    test_sequential_execution()
