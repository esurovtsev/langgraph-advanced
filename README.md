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
2. **Lesson 2:** (Coming soon)
3. **Lesson 3:** (Coming soon)

*This list will be updated as new lessons are added. Each lesson will include code, explanations, and a video walkthrough.*


## Contributing

Feedback and contributions are welcome! Please open issues or submit pull requests for suggestions and improvements.

## License

[Specify your license here, e.g., MIT]

---

*This README will be updated as the course progresses. Stay tuned for new lessons and videos!*
