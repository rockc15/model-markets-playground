import os
import argparse
import yaml
from pathlib import Path
from dotenv import load_dotenv

import anthropic

from tools.tools import anthropic_tools, tool_map


def load_config(config_path):
    """Load configuration from YAML file."""
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)


def main(config_path):
    """Main function to execute the trading agent."""
    # Load configuration
    config = load_config(config_path)
    
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
    

    
    client = anthropic.Anthropic(
        api_key=api_key,
    )


    response = client.messages.create(
        model=config["agent"]["name"],
        max_tokens=config["agent"]["max_tokens"],
        temperature=1,
        system=config["agent"]["system_promt"],
        tools=anthropic_tools,
        messages=[
            {"role": "user", "content": config["prompt"]}
        ],
    )

    print(type(response))
    for block in response.content:
        if block.type == "tool_use":
            print("Tool name:", block.name)
            print("Tool input:", block.input)
            print("Tool use ID:", block.id)
        elif block.type == "text":
            print("Claude response:", block.text)
        print("=============================")



    



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Trading agent with configurable settings")
    parser.add_argument("config", help="Path to the configuration YAML file")
    
    args = parser.parse_args()
    main(args.config)
