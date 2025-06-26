# Sequential Tool Execution System

A sophisticated AI agent system that enables **sequential tool calling** for comprehensive analysis and decision-making. The agent can call multiple tools in sequence, analyze results, and make informed decisions based on accumulated information.

## 🚀 Key Features

### ✅ **Sequential Tool Execution**
- Agent can call multiple tools in sequence
- Each tool result informs the next decision
- Continues until sufficient information is gathered
- Automatic stopping when final decision is reached

### ✅ **Intelligent Decision Making**
- Builds comprehensive analysis from multiple data sources
- Strategic tool selection and ordering
- Context-aware reasoning with accumulated information
- Configurable decision thresholds and stopping conditions

### ✅ **Robust Error Handling**
- Tool execution timeouts and retry logic
- Graceful failure recovery
- Comprehensive logging and debugging
- Safe conversation state management

### ✅ **Enhanced Financial Tools**
- Real-time stock data retrieval
- Market overview and sentiment analysis
- Anthropic's web search integration
- Investment recommendation generation

## 🏗️ Architecture

```
User Query → ConversationManager → Claude → Tool Selection → Tool Execution → Analysis → More Tools? → Final Decision
```

### Core Components

1. **ConversationManager** (`conversation_manager.py`)
   - Manages multi-turn conversations
   - Handles tool execution flow
   - Maintains conversation history and context

2. **ToolExecutor** (`tool_executor.py`)
   - Executes individual tools with timeout support
   - Provides error handling and retry logic
   - Manages tool registry and execution

3. **Enhanced Tools** (`tools/tools.py`)
   - Financial data retrieval (yfinance integration)
   - Market analysis tools
   - Anthropic web search integration
   - Investment recommendation tools

## 📊 Example Workflow

**User:** "Should I invest in NVDA stock?"

**Agent's Sequential Process:**
1. `get_market_overview()` → Gets overall market conditions
2. `get_stock_data("NVDA")` → Gets NVIDIA's detailed metrics
3. `web_search("NVDA recent news")` → Gets latest news and analysis
4. **Analysis:** Combines all data points
5. `buy_stock("NVDA")` → Generates final recommendation

## 🛠️ Installation & Setup

### Prerequisites
```bash
pip install anthropic yfinance python-dotenv pyyaml
```

### Environment Setup
Create a `.env` file:
```bash
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

### Configuration
Edit `config.yaml`:
```yaml
agent:
  name: claude-3-5-haiku-latest
  max_tokens: 2048
  temperature: 0.1
  system_promt: "Your agent system prompt here"

conversation:
  max_iterations: 10
  require_final_decision: true
  tool_timeout: 30

decision_framework:
  require_reasoning: true
  min_data_points: 2
  confidence_threshold: 0.7
```

## 🚀 Usage

### Basic Usage
```bash
python3 main.py config.yaml
```

### With Verbose Logging
```bash
python3 main.py config.yaml --verbose
```

### Testing Sequential Tools
```bash
python3 test_sequential_tools.py
```

## 🔧 Available Tools

| Tool                  | Description                   | Input Parameters     |
| --------------------- | ----------------------------- | -------------------- |
| `get_stock_data`      | Comprehensive stock analysis  | `symbol`, `period`   |
| `get_market_overview` | Major market indices overview | None                 |
| `web_search`          | Anthropic web search          | `query`              |
| `buy_stock`           | Generate buy recommendation   | `symbol`, `quantity` |
| `sell_stock`          | Generate sell recommendation  | `symbol`, `quantity` |
| `hold_stock`          | Generate hold recommendation  | `symbol`, `reason`   |

## 📈 Example Output

```
================================================================================
SEQUENTIAL TOOL EXECUTION RESULTS
================================================================================

📊 EXECUTION SUMMARY:
   • Iterations used: 4
   • Tools executed: 3
   • Conversation length: 8
   • Success: True

🔧 TOOLS EXECUTED:
   1. get_market_overview({}) → Market indices data
   2. get_stock_data({'symbol': 'NVDA', 'period': '6mo'}) → NVIDIA analysis
   3. buy_stock({'symbol': 'NVDA', 'quantity': 3}) → Final recommendation

🤖 FINAL AGENT RESPONSE:
Investment Recommendation: BUY
- Confidence Level: High
- Recommended Quantity: 3 shares
- Rationale: Strong market leadership in AI and semiconductor technologies...
```

## ⚙️ Configuration Options

### Conversation Settings
- `max_iterations`: Maximum conversation rounds (default: 10)
- `require_final_decision`: Force final decision (default: true)
- `tool_timeout`: Tool execution timeout in seconds (default: 30)

### Decision Framework
- `require_reasoning`: Require reasoning in final response
- `min_data_points`: Minimum tools to execute before decision
- `confidence_threshold`: Confidence level for recommendations

## 🔍 Advanced Features

### Custom Tool Development
Add new tools to the system:

```python
def my_custom_tool(inputs):
    """Custom tool implementation."""
    # Your tool logic here
    return result

# Register the tool
tool_executor.add_tool("my_tool", my_custom_tool)
```

### Tool Registry Management
```python
# List available tools
tools = tool_executor.list_tools()

# Get tool information
info = tool_executor.get_tool_info()

# Remove a tool
tool_executor.remove_tool("tool_name")
```

### Error Handling
```python
from tool_executor import safe_execute_tool

result = safe_execute_tool(
    tool_executor, 
    "tool_name", 
    {"param": "value"},
    timeout=30,
    max_retries=3
)
```

## 🐛 Debugging

### Enable Debug Logging
```bash
python3 main.py config.yaml --verbose
```

### Check Tool Execution
Monitor tool execution in logs:
```
INFO:tool_executor:Executing tool 'get_stock_data' with input: {'symbol': 'NVDA'}
INFO:tool_executor:Tool 'get_stock_data' completed in 0.64s
```

### Conversation Flow
Track conversation iterations:
```
INFO:conversation_manager:Conversation iteration 1
INFO:conversation_manager:Tool get_market_overview executed successfully
INFO:conversation_manager:Final response received - no more tool calls
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your enhancements
4. Test with `test_sequential_tools.py`
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- **Anthropic** for Claude AI and web search capabilities
- **yfinance** for financial data integration
- **Python ecosystem** for robust tooling support

---

**Built with ❤️ for intelligent sequential decision-making**
