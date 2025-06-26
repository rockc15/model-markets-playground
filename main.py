import os
import argparse
import yaml
from pathlib import Path
from dotenv import load_dotenv
import logging

import anthropic

from tools.tools import anthropic_tools
from conversation_manager import ConversationManager

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_config(config_path):
    """Load configuration from YAML file."""
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)


def print_conversation_result(result):
    """Print the conversation result in a formatted way."""
    print("\n" + "="*80)
    print(" EXECUTION RESULTS")
    print("="*80)
    
    print(f"\n📊 EXECUTION SUMMARY:")
    print(f"   • Iterations used: {result['iterations_used']}")
    print(f"   • Tools executed: {result['tools_executed']}")
    print(f"   • Conversation length: {result['conversation_length']}")
    print(f"   • Success: {result['success']}")
    
    if result['tool_summary']:
        print(f"\n🔧 TOOLS EXECUTED:")
        for i, tool in enumerate(result['tool_summary'], 1):
            print(f"   {i}. {tool['tool']}({tool['input']}) -> {str(tool['result'])[:100]}...")
    
    print(f"\n🤖 FINAL AGENT RESPONSE:")
    print("-" * 40)
    print(result['final_response'])
    print("-" * 40)
    
    print("\n" + "="*80)


def main(config_path):
    """Main function to execute the trading agent with sequential tool calling."""
    try:
        # Load configuration
        config = load_config(config_path)
        logger.info(f"Loaded configuration from {config_path}")
        
        # Load environment variables
        load_dotenv()
        
        # Get API key
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
        
        # Initialize Anthropic client
        client = anthropic.Anthropic(api_key=api_key)
        logger.info("Initialized Anthropic client")
        
        # Initialize conversation manager
        conversation_manager = ConversationManager(client, config)
        logger.info("Initialized conversation manager")
        
        # Get user prompt from config
        user_prompt = config.get("prompt", "Analyze the current market conditions")
        logger.info(f"Starting conversation with prompt: {user_prompt[:100]}...")
        
        # Start sequential conversation
        result = conversation_manager.start_conversation(user_prompt, anthropic_tools)
        
        # Print results
        print_conversation_result(result)
        
        return result
        
    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}")
        print(f"\n❌ ERROR: {str(e)}")
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Trading agent with sequential tool execution capabilities"
    )
    parser.add_argument("config", help="Path to the configuration YAML file")
    parser.add_argument(
        "--verbose", "-v", 
        action="store_true", 
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    main(args.config)
