# LangGraph Advanced

This repository continues the LangGraph learning journey with a collection of advanced Jupyter notebooks. It focuses on real-world agent architectures, including dynamic tool loading, long-term memory management, human-in-the-loop control, and parallel execution. Designed for developers who already grasp the basics, this series helps you build scalable and production-ready AI workflows with LangGraph and LangChain.

## Getting Started

### 1. Clone the Repository

```bash
git clone git@github.com:esurovtsev/langgraph-advanced.git
cd langgraph-advanced
```

### 2. Set Up Your Python Environment

It is recommended to use a virtual environment to manage dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Usage

- Follow the lessons in order (scripts or notebooks).
- Each lesson will have an accompanying video tutorial.
- Explanations and code comments will help you understand each concept.

## Video Tutorials

Each lesson will have a dedicated video tutorial. Links will be provided as lessons are released.

## Contents

1. **Prebuilt Agents** ([01_prebuilt-agents.ipynb](01_prebuilt-agents.ipynb))
   - Deep dive into the architecture and workflow of prebuilt agents in LangGraph
   - Explains the ReAct agent pattern: act, observe, reason, and how these steps form the backbone of agent logic
   - Demonstrates defining and binding tools to LLMs using low-level APIs, including practical examples like stock symbol lookup and financial data retrieval
   - Walks through constructing a state graph for agent execution, including system and tool nodes, routing, and memory management
   - Real-world scenario: Building an agent that fetches and analyzes financial data for companies (e.g., Tesla), showing the full reasoning and tool invocation loop
   - [LangGraph Advanced – Build AI Agents with Prebuilt Agents and Memory](https://www.youtube.com/watch?v=_0-OoRyFwpo)
2. **Dynamic Models & Prompt Customization** ([02_dynamic-models-prompts.ipynb](02_dynamic-models-prompts.ipynb))
   - Advanced techniques for creating adaptive AI agents with dynamic model selection and role switching
   - Implementing context-aware model selection that chooses different LLMs based on task complexity (e.g., GPT-4 for analysis, GPT-4o-mini for summarization)
   - Creating dynamic prompt modifiers that adapt agent roles and behaviors in response to user queries
   - Combining both techniques to build sophisticated agents that can switch between financial advisor, teacher, or summarizer roles
   - Real-world example: Building a financial analysis agent that adapts both its underlying model and persona based on query complexity
   - [LangGraph Advanced – Build AI Agents with Dynamic Model Selection and Role Switching](https://www.youtube.com/watch?v=bV1K8B4m5PI)
3. **Structured Output with Prebuilt Agents** ([03_structured_output_with_prebuilt_agents.ipynb](03_structured_output_with_prebuilt_agents.ipynb))
   - Why structured output matters for production apps that need machine-readable results, not just chat text
   - Define a Pydantic schema (e.g., `FinancialInfo`) and pass it via `response_format` to `create_react_agent` (v2)
   - Understand the added graph step to generate a structured response and how to access it from the agent state
   - Trade-offs: extra LLM call cost; alternatives include treating the schema as a tool or using a post-model hook with custom state to capture JSON without extra calls
   - Real-world example: TSLA analysis producing JSON fields like company_name, stock_symbol, current_price, market_cap, summary, risk_assessment
   - [LangGraph Advanced – Generate Structured Output in AI Agents Using Prebuilt LangGraph APIs](https://www.youtube.com/watch?v=3Q31aObRBMo)
4. **Human-in-the-Loop Interruption with Prebuilt Agents** ([04_prebuilt_hitl_dynamic_interrupt.ipynb](04_prebuilt_hitl_dynamic_interrupt.ipynb))
   - When and why to add human approvals for risky actions (e.g., placing market/limit orders)
   - Two approaches:
     - Static: `interrupt_before=["tools"]` to always pause before the tools node (simple but coarse-grained)
     - Dynamic: raise `interrupt(...)` inside `post_model_hook` when the LLM proposes a risky tool call
   - Implementation details:
     - Maintain `RISKY_TOOLS = {"place_order"}` and inspect the last `AIMessage.tool_calls`
     - Enable a checkpointer (e.g., `InMemorySaver`) and pass a `thread_id` so runs can be paused and resumed
     - Read the interruption payload from the response to render an approval UI, then resume with a `Command(...)` carrying the decision
   - Resume paths:
     - Approve: proceed to execute the tool normally
     - Decline: inject a `ToolMessage` like “Action cancelled by human” and continue the agent flow without executing the tool
   - Real-world example: Buying TSLA shares with approve/decline flows demonstrated end-to-end
   - [LangGraph Advanced – Use Dynamic Human in the Loop Interruption in Prebuilt AI Agents](https://www.youtube.com/watch?v=8_UQNWTbvEQ)
*This list will be updated as new lessons are added. Each lesson will include code, explanations, and a video walkthrough.*


## Contributing

Feedback and contributions are welcome! Please open issues or submit pull requests for suggestions and improvements.

## License

[Specify your license here, e.g., MIT]

---

*This README will be updated as the course progresses. Stay tuned for new lessons and videos!*
