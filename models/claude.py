import anthropic
from dotenv import load_dotenv
import os

from pathlib import Path

# Path to the .env file in another directory
env_path = Path(__file__).resolve().parent / '.env'
load_dotenv(dotenv_path=env_path)


api_key = os.getenv("ANTHROPIC_API_KEY")

client = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key=api_key,
)

message = client.messages.create(
    model="claude-opus-4-20250514",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello, Claude"}
    ]
)
print(message.content)