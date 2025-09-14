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
5. **Multi-Agent Systems with Supervisor Architecture** ([05_multi_agent_supervisor.ipynb](05_multi_agent_supervisor.ipynb))
   - Build a supervisor-led multi-agent system that delegates between specialized workers
   - Define `research_agent` (Tavily + Wikipedia) to pick ONE company with a brief rationale
   - Define `trading_agent` (ticker lookup, market data via yfinance, order placement) to execute trades from a budget
   - Use `create_supervisor` to orchestrate routing, handoffs, and guardrails; view graph and xray
   - Establish shared time context via a `current_timestamp` tool and post a one-line “NOW” note for recency
   - Routing rules: thematic/ambiguous → research; explicit company + action/budget → trading; ask once if a key detail is missing
   - Handoff: pass chosen company from research to trading; avoid fabricating data; summarize delegated steps and results
   - Real-world flow: invest $1,000 in AI/renewables—research selects a company, trading sizes the order and places a buy
   - [LangGraph Advanced – Build Multi-Agent AI Systems with Supervisor Architecture](https://www.youtube.com/watch?v=TK9kf6a9i10)

6. **Supervisor + Human-in-the-Loop in Multi-Agent Systems** ([06_supervisor_with_hitl.ipynb](06_supervisor_with_hitl.ipynb))
   - Combine supervisor-led delegation with HITL approvals inside child agents (e.g., `trading_agent`).
   - Child interruptions bubble to the supervisor when the checkpointer is owned by the parent; resume the run by invoking the supervisor (not the child) with the same `thread_id`.
   - Implementation:
     - `trading_agent` uses a `post_model_hook` (`halt_on_risky_tools`) to detect `RISKY_TOOLS = {"place_order"}` and call `interrupt({"awaiting": name, "args": {...}})`.
     - On decline, inject a `ToolMessage` like “Cancelled by human…” and continue planning without executing the tool.
     - Supervisor compiled with `InMemorySaver()` (`.compile(checkpointer=...)`) and `output_mode="full_history"`; visualize routing with `xray`.
     - Interact only with the supervisor; to resume, use `Command(resume={"approved": True|False})` and a stable `configurable.thread_id`.
     - Inspect `response["__interrupt__"]` to render an approval UI; helper `print_tool_approval(...)` shows the tool and parameters.
   - Shared time context: call `current_timestamp` once and post a one-line “NOW” note to the thread for recency across agents.
   - Test flows: approve path, reject path, update request (e.g., “buy only 3 shares of NVIDIA”), and continue within the same thread.
   - Real-world flow: invest $1,000 with an approval gate before order placement; supervisor coordinates research → trading and handles pause/resume.
   - [LangGraph Advanced – Combine Supervisor Architecture with Human-in-the-Loop in Multi-Agent AI Systems](https://www.youtube.com/watch?v=W349TTcB0Ng)

7. **Add Long-Term Memory to Multi-Agent AI Systems with Supervisor Architecture** ([07_supervisor_long_term_memory.ipynb](07_supervisor_long_term_memory.ipynb))
   - Integrate persistent memory using `InMemoryStore` across supervisor and child agents for user-specific order history.
   - Define memory tools: `get_order_history` (retrieve past orders by `user_id` namespace) and `add_order_to_history` (record new trades with symbol, shares, price).
   - Research agent: recommends ONE publicly tradable company using `web_search` and `wiki_search` tools, ends with "CHOSEN_COMPANY: <Name>".
   - Portfolio agent: executes trades for the exact recommended company using `lookup_stock_symbol`, `fetch_stock_data_raw`, `place_order`, and records via `add_order_to_history`.
   - Supervisor: delegates to research (for ideas) or portfolio (for execution); uses shared store via `get_global_store()` and temporal context from `current_timestamp`.
   - User isolation: namespace `user_id` for memory access; use `get_user_store()` to access the user’s store.
   - Real-world flow: invest $1,000 in EV or AI industry—research picks company, portfolio trades and records; query "how many shares do I own?" using memory.
   - [LangGraph Advanced – Add Long Term Memory to Multi Agent AI Systems with Supervisor Architecture](https://www.youtube.com/watch?v=piri_eR7s)

8. **Custom Handoffs in Supervisor Architecture** ([08_supervisor_custom_handoff.ipynb](08_supervisor_custom_handoff.ipynb))
   - Improve task reasoning with targeted delegation and shared context
   - Define a custom handoff tool using `create_task_instructions_handoff_tool(...)` to pass explicit `task_instructions` and route control via `Command(goto=...)`
   - Extend agent state with `TaskState(AgentState)` to carry `task_instructions` across handoffs; compile agents/supervisor with `state_schema=TaskState`
   - Use `InjectedState` and `InjectedToolCallId` inside tools to access current state and emit a `ToolMessage` containing handoff metadata (`METADATA_KEY_HANDOFF_DESTINATION`) for xray tracing
   - Supervisor tools include `current_timestamp`, `get_order_history`, and two handoff tools (to `portfolio` and `research`) to guide precise sub-tasks
   - Portfolio and research agents reuse earlier tools (lookup, market data via yfinance, search) while supervisor orchestrates when to fetch prices vs. query memory
   - Demonstration: "How are my investments performing?" → supervisor retrieves order history, delegates to portfolio to fetch current prices, then summarizes performance
   - Compiled with `InMemorySaver()` and `output_mode="full_history"` to visualize routing and handoffs
   - [LangGraph Advanced – Improve Multi Agent AI Systems with Custom Handoffs in Supervisor Architecture](https://www.youtube.com/watch?v=rn4TkOGYU64)

9. **Build Hierarchical Multi-Level Supervisor Architectures and Swarm AI Agents** ([09_supervisor_hierarchy_and_swarm.ipynb](09_supervisor_hierarchy_and_swarm.ipynb))
  - Create hierarchical multi-level supervisor architectures where supervisors control other supervisors.
  - Extract specialized agents into sub-supervisors: portfolio_supervisor (symbol_lookup, market_data, order_execution, record_keeping) and research_supervisor (web_search, wiki_search).
  - Build a super_supervisor that orchestrates research_supervisor, portfolio_supervisor, timestamp, and history agents for end-to-end workflows.
  - Implement swarm AI agents using `create_swarm()` for parallel handoffs between agents without hierarchy (e.g., web_search ↔ market_data).
  - Compile with `InMemorySaver()` and `output_mode="full_history"` to visualize routing and handoffs.

10. **Simplify Multi-Agent AI Systems by Turning Sub-Agents into Tools with Supervisor Architecture** ([10_supervisor_as_tools.ipynb](10_supervisor_as_tools.ipynb))
  - Alternative supervisor architecture where sub-agents are turned into tools instead of sharing message lists.
  - Define `@tool` functions like `research_agent_tool` and `trading_agent_tool` that invoke isolated runs of sub-agents with `RunnableConfig`, passing a task and returning the last `AIMessage` response.
  - Supervisor is a single `create_react_agent` with tools including `current_timestamp`, `research_agent_tool`, `trading_agent_tool`; no sub-agents under control.
  - Benefits: isolated executions (no shared message confusion), easier parallelism, clear task definitions.
  - Drawbacks of traditional shared-message supervisors: long threads confuse agents, hard to parallelize, state sharing issues.
  - Demonstration: invest $1,000 in AI company → supervisor calls research tool (isolated: web_search/wiki_search → recommends MSFT) → calls trading tool (isolated: lookup/fetch/place → executes order) → summarizes.
  - [LangGraph Advanced – Simplify Multi-Agent AI Systems by Turning Sub-Agents into Tools with Supervisor Architecture](https://www.youtube.com/watch?v=O7GDyJZ5X8)

## Contributing

Feedback and contributions are welcome! Please open issues or submit pull requests for suggestions and improvements.

## License

[Specify your license here, e.g., MIT]

---

*This README will be updated as the course progresses. Stay tuned for new lessons and videos!*
