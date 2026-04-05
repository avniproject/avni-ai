# Building 17 Agentic AI Patterns and Their Role in Large-Scale AI Systems

*Ensembling, Meta-Control, ToT, Reflexive, PEV and more*

**By Fareed Khan** · 77 min read · Sep 26, 2025

---

When you build a large-scale AI system, you are really putting different agentic design patterns together. Each one has its own stage, build method, output, and evaluation. If we step back and group these patterns, they can be broken down into 17 high-level architectures that capture the main shapes agentic systems can take …

Some of the patterns are:

- A **Multi-Agent System**, where several tools and agents work together to solve a problem.
- An **Ensemble Decision System**, where multiple agents each propose an answer and then vote on the best one.
- A **Tree-of-Thoughts**, where the agent explores many different reasoning paths before selecting the most promising direction.
- **Reflexive** approach, where the agent is able to recognize and acknowledge what it does not know.
- The **ReAct loop**, where the agent alternates between thinking, taking action, and then thinking again to refine its process.
- And there are many more …

In this blog, we are going to break down these different kinds of agentic architectures and show how each one plays a unique role in a complete AI system.

We will visually understand each architecture importance, code its workflow, and evaluate it to see whether it truly improves performance compared to a baseline.

All the code is available in the [GitHub Repository](https://github.com/FareedKhan-dev/all-agentic-architectures).

Codebase is organized as follows:

```
all-agentic-architectures/
    ├── 01_reflection.ipynb
    ├── 02_tool_use.ipynb
    ├── 03_ReAct.ipynb
    ...
    ├── 06_PEV.ipynb
    ├── 07_blackboard.ipynb
    ├── 08_episodic_with_semantic.ipynb
    ├── 09_tree_of_thoughts.ipynb
    ...
    ├── 14_dry_run.ipynb
    ├── 15_RLHF.ipynb
    ├── 16_cellular_automata.ipynb
    └── 17_reflexive_metacognitive.ipynb
```

---

## Table of Contents

1. [Setting up the Environment](#setting-up-the-environment)
2. [Reflection](#reflection)
3. [Tool Using](#tool-using)
4. [ReAct (Reason + Act)](#react-reason--act)
5. [Planning](#planning)
6. [PEV (Planner-Executor-Verifier)](#pev-planner-executor-verifier)
7. [Tree-of-Thoughts (ToT)](#tree-of-thoughts-tot)
8. [Multi-Agent Systems](#multi-agent-systems)
9. [Meta-Controller](#meta-controller)
10. [Blackboard](#blackboard)
11. [Ensemble Decision-Making](#ensemble-decision-making)
12. [Episodic + Semantic Memory](#episodic--semantic-memory)
13. [Graph (World-Model) Memory](#graph-world-model-memory)
14. [Self-Improvement Loop (RLHF Analogy)](#self-improvement-loop-rlhf-analogy)
15. [Dry-Run Harness](#dry-run-harness)
16. [Simulator (Mental-Model-in-the-Loop)](#simulator-mental-model-in-the-loop)
17. [Reflexive Metacognitive](#reflexive-metacognitive)
18. [Cellular Automata](#cellular-automata)
19. [Combining Architectures Together](#combining-architectures-together)

---

## Setting up the Environment

Before we start building each architecture, we need to set up the basics and be clear on what we are using and why — the modules, the models, and how it all fits together.

LangChain, LangGraph, and LangSmith are pretty much the industry-standard modules out there for building any serious RAG or agentic system. They give us everything we need to build, orchestrate, and, most importantly, figure out what's going on inside our agents when things get complicated.

The very first step is to get our core libraries imported:

```python
import os
from typing import List, Dict, Any, Optional, Annotated, TypedDict
from dotenv import load_dotenv  # Load environment variables from .env file

# Pydantic for data modeling / validation
from pydantic import BaseModel, Field

# LangChain & LangGraph components
from langchain_nebius import ChatNebius  # Nebius LLM wrapper
from langchain_tavily import TavilySearch  # Tavily search tool integration
from langchain_core.prompts import ChatPromptTemplate  # For structuring prompts
from langgraph.graph import StateGraph, END  # Build a state machine graph
from langgraph.prebuilt import ToolNode, tools_condition  # Prebuilt nodes & conditions

# For pretty printing output
from rich.console import Console  # Console styling
from rich.markdown import Markdown  # Render markdown in terminal
```

- **LangChain** is our toolbox, giving us the core building blocks like prompts, tool definitions, and LLM wrappers.
- **LangGraph** is our orchestration engine, wiring everything together into complex workflows with loops and branches.
- **LangSmith** is our debugger, showing a visual trace of every step an agent takes so we can quickly spot and fix issues.

We will be working with open-source LLMs through providers like Nebius AI or Together AI. And if we want to run things locally, we can just swap in something like Ollama.

To make sure our agents are not stuck with static data, we are giving them access to the Tavily API for live web searches (1000 credits/month enough for testing).

Next, set up your `.env` file:

```ini
# API key for Nebius LLM (used with ChatNebius)
NEBIUS_API_KEY="your_nebius_api_key_here"

# API key for LangSmith (LangChain's observability/telemetry platform)
LANGCHAIN_API_KEY="your_langsmith_api_key_here"

# API key for Tavily search tool (used with TavilySearch integration)
TAVILY_API_KEY="your_tavily_api_key_here"
```

Once the `.env` file is set up:

```python
load_dotenv()  # Load environment variables from .env file

# Enable LangSmith tracing for monitoring / debugging
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "Implementing 17 Agentic Architectures"

# Verify that all required API keys are available
for key in ["NEBIUS_API_KEY", "LANGCHAIN_API_KEY", "TAVILY_API_KEY"]:
    if not os.environ.get(key):
        print(f"{key} not found. Please create a .env file and set it.")
```

---

## Reflection

The very first architecture is **Reflection** — probably the most common and foundational pattern you see in agentic workflows.

It's all about giving an agent the ability to take a step back, look at its own work, and make it better.

In a large-scale AI system, this pattern fits perfectly in any stage where the quality of a generated output is critical — generating complex code, writing detailed technical reports, anywhere a simple first-draft answer just isn't good enough.

**Workflow:**

1. **Generate**: The agent takes the user prompt and produces an initial draft or solution.
2. **Critique**: The agent switches roles and becomes its own critic, analyzing the draft for flaws.
3. **Refine**: The agent generates a final, improved version of the output, addressing the flaws it found.

### Pydantic Models

```python
class DraftCode(BaseModel):
    """Schema for the initial code draft generated by the agent."""
    code: str = Field(description="The Python code generated to solve the user's request.")
    explanation: str = Field(description="A brief explanation of how the code works.")

class Critique(BaseModel):
    """Schema for the self-critique of the generated code."""
    has_errors: bool = Field(description="Does the code have any potential bugs or logical errors?")
    is_efficient: bool = Field(description="Is the code written in an efficient and optimal way?")
    suggested_improvements: List[str] = Field(description="Specific, actionable suggestions for improving the code.")
    critique_summary: str = Field(description="A summary of the critique.")

class RefinedCode(BaseModel):
    """Schema for the final, refined code after incorporating the critique."""
    refined_code: str = Field(description="The final, improved Python code.")
    refinement_summary: str = Field(description="A summary of the changes made based on the critique.")
```

### Nodes

```python
def generator_node(state):
    """Generates the initial draft of the code."""
    console.print("--- 1. Generating Initial Draft ---")
    generator_llm = llm.with_structured_output(DraftCode)
    
    prompt = f"""You are an expert Python programmer. Write a Python function to solve the following request.
    Provide a simple, clear implementation and an explanation.
    
    Request: {state['user_request']}
    """
    
    draft = generator_llm.invoke(prompt)
    return {"draft": draft.model_dump()}


def critic_node(state):
    """Critiques the generated code for errors and inefficiencies."""
    console.print("--- 2. Critiquing Draft ---")
    critic_llm = llm.with_structured_output(Critique)
    
    code_to_critique = state['draft']['code']
    
    prompt = f"""You are an expert code reviewer and senior Python developer. Your task is to perform a thorough critique of the following code.
    
    Analyze the code for:
    1.  **Bugs and Errors:** Are there any potential runtime errors, logical flaws, or edge cases that are not handled?
    2.  **Efficiency and Best Practices:** Is this the most efficient way to solve the problem? Does it follow standard Python conventions (PEP 8)?
    
    Provide a structured critique with specific, actionable suggestions.
    
    Code to Review:
    ```python
    {code_to_critique}
    ```
    """
    
    critique = critic_llm.invoke(prompt)
    return {"critique": critique.model_dump()}


def refiner_node(state):
    """Refines the code based on the critique."""
    console.print("--- 3. Refining Code ---")
    refiner_llm = llm.with_structured_output(RefinedCode)
    
    draft_code = state['draft']['code']
    critique_suggestions = json.dumps(state['critique'], indent=2)
    
    prompt = f"""You are an expert Python programmer tasked with refining a piece of code based on a critique.
    
    Your goal is to rewrite the original code, implementing all the suggested improvements from the critique.
    
    **Original Code:**
    ```python
    {draft_code}
    ```
    
    **Critique and Suggestions:**
    {critique_suggestions}
    
    Please provide the final, refined code and a summary of the changes you made.
    """
    
    refined_code = refiner_llm.invoke(prompt)
    return {"refined_code": refined_code.model_dump()}
```

### Graph

```python
class ReflectionState(TypedDict):
    """Represents the state of our reflection graph."""
    user_request: str
    draft: Optional[dict]
    critique: Optional[dict]
    refined_code: Optional[dict]

graph_builder = StateGraph(ReflectionState)

graph_builder.add_node("generator", generator_node)
graph_builder.add_node("critic", critic_node)
graph_builder.add_node("refiner", refiner_node)

graph_builder.set_entry_point("generator")
graph_builder.add_edge("generator", "critic")
graph_builder.add_edge("critic", "refiner")
graph_builder.add_edge("refiner", END)

reflection_app = graph_builder.compile()
```

### Example Output

```
--- ### Initial Draft ---
Explanation: This function uses a recursive approach... not efficient for large values of n...

def fibonacci(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)

--- ### Critique ---
Summary: The function has potential bugs and inefficiencies...
Improvements Suggested:
- The function does not handle negative numbers correctly.
- High time complexity due to repeated calculations. Consider memoization.
- The function does not follow PEP 8 conventions...

--- ### Final Refined Code ---
Refinement Summary: Revised to handle negative inputs, improve time complexity, and follow PEP 8.

def fibonacci(n):
    """Calculates the nth Fibonacci number."""
    if n < 0:
        raise ValueError("n must be a non-negative integer")
    elif n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        fib = [0, 1]
        for i in range(2, n + 1):
            fib.append(fib[i-1] + fib[i-2])
        return fib[n]
```

### Evaluation (LLM-as-a-Judge)

```python
class CodeEvaluation(BaseModel):
    correctness_score: int = Field(description="Score from 1-10 on whether the code is logically correct.")
    efficiency_score: int = Field(description="Score from 1-10 on the code's algorithmic efficiency.")
    style_score: int = Field(description="Score from 1-10 on code style and readability (PEP 8).")
    justification: str = Field(description="A brief justification for the scores.")
```

| Version | Correctness | Efficiency | Style |
|---|---|---|---|
| Initial Draft | 2 | 4 | 2 |
| Refined Code | 8 | 6 | 9 |

---

## Tool Using

The Reflection pattern sharpens internal reasoning. But what happens when the agent needs information it doesn't already know?

Without access to external tools, an LLM is limited to its pre-trained parameters. **Tool Use** is the bridge between an agent's reasoning and real-world data.

**Workflow:**

1. **Receive Query**: The agent gets a request from the user.
2. **Decision**: The agent decides if a tool is needed.
3. **Action**: If needed, the agent formats a call to the tool.
4. **Observation**: The result is sent back to the agent.
5. **Synthesis**: The agent combines the tool's output with its reasoning to generate a final answer.

### Setup

```python
search_tool = TavilySearchResults(max_results=2)
search_tool.name = "web_search"
search_tool.description = "A tool that can be used to search the internet for up-to-date information on any topic, including news, events, and current affairs."

tools = [search_tool]

class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

llm = ChatNebius(model="meta-llama/Meta-Llama-3.1-8B-Instruct", temperature=0)
llm_with_tools = llm.bind_tools(tools)
```

### Nodes

```python
def agent_node(state: AgentState):
    """The primary node that calls the LLM to decide the next action."""
    console.print("--- AGENT: Thinking... ---")
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}

tool_node = ToolNode(tools)

def router_function(state: AgentState) -> str:
    """Inspects the agent's last message to decide the next step."""
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        console.print("--- ROUTER: Decision is to call a tool. ---")
        return "call_tool"
    else:
        console.print("--- ROUTER: Decision is to finish. ---")
        return "__end__"
```

### Graph

```python
graph_builder = StateGraph(AgentState)
graph_builder.add_node("agent", agent_node)
graph_builder.add_node("call_tool", tool_node)
graph_builder.set_entry_point("agent")
graph_builder.add_conditional_edges("agent", router_function)
graph_builder.add_edge("call_tool", "agent")
tool_agent_app = graph_builder.compile()
```

### Evaluation

```
{
    'tool_selection_score': 5,
    'tool_input_score': 5,
    'synthesis_quality_score': 4,
    'justification': "The AI agent correctly used the web search tool..."
}
```

---

## ReAct (Reason + Act)

The previous tool-using agent is a one-shot deal — it decides it needs a tool, calls it once, and then tries to answer. **ReAct** creates a *loop* enabling an agent to dynamically reason about what to do next, take an action, observe the result, and use that new information to reason again.

**Workflow:**

1. **Receive Goal**: The agent is given a complex task that can't be solved in one step.
2. **Think (Reason)**: The agent generates a thought, e.g., "To answer this, I first need to find piece of information X."
3. **Act**: Based on that thought, it executes an action.
4. **Observe**: The agent gets the result back from the tool.
5. **Repeat**: It loops back to step 2, reasoning: "Okay, now that I have X, I need to find Y."

### Graph

```python
def react_agent_node(state: AgentState):
    """The agent node that thinks and decides the next step."""
    console.print("--- REACT AGENT: Thinking... ---")
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}

react_graph_builder = StateGraph(AgentState)
react_graph_builder.add_node("agent", react_agent_node)
react_graph_builder.add_node("tools", tool_node)

react_graph_builder.set_entry_point("agent")
react_graph_builder.add_conditional_edges(
    "agent",
    router_function,
    {"call_tool": "tools", "__end__": "__end__"}
)

# This is the key difference: the edge goes from the tool node BACK to the agent
react_graph_builder.add_edge("tools", "agent")

react_agent_app = react_graph_builder.compile()
```

The single line `react_graph_builder.add_edge("tools", "agent")` creates the loop and turns our simple tool-user into a dynamic ReAct agent.

### Evaluation

```
{
    'task_completion_score': 8,
    'reasoning_quality_score': 9,
    'justification': "The agent correctly broke down the problem into multiple steps..."
}
```

---

## Planning

The ReAct pattern is fantastic for exploring a problem on the fly. But it can be inefficient for tasks where the steps are predictable. The **Planning** architecture introduces a crucial layer of *foresight* — the agent first creates a full "battle plan" before taking any action.

**Workflow:**

1. **Receive Goal**: The agent is given a complex task.
2. **Plan**: A dedicated Planner component generates an ordered list of sub-tasks.
3. **Execute**: An Executor carries out each sub-task in sequence.
4. **Synthesize**: A final component assembles the results into a coherent final answer.

### Nodes

```python
class Plan(BaseModel):
    """A plan of tool calls to execute to answer the user's query."""
    steps: List[str] = Field(description="A list of tool calls that, when executed, will answer the query.")

class PlanningState(TypedDict):
    user_request: str
    plan: Optional[List[str]]
    intermediate_steps: List[str]
    final_answer: Optional[str]

def planner_node(state: PlanningState):
    """Generates a plan of action to answer the user's request."""
    console.print("--- PLANNER: Decomposing task... ---")
    planner_llm = llm.with_structured_output(Plan)
    
    prompt = f"""You are an expert planner. Your job is to create a step-by-step plan to answer the user's request.
        Each step in the plan must be a single call to the `web_search` tool.
        **User's Request:**
        {state['user_request']}
    """
    plan_result = planner_llm.invoke(prompt)
    console.print(f"--- PLANNER: Generated Plan: {plan_result.steps} ---")
    return {"plan": plan_result.steps}


def executor_node(state: PlanningState):
    """Executes the next step in the plan."""
    console.print("--- EXECUTOR: Running next step... ---")
    next_step = state["plan"][0]
    query = next_step.replace("web_search('", "").replace("')", "")
    result = search_tool.invoke({"query": query})
    
    return {
        "plan": state["plan"][1:],
        "intermediate_steps": state["intermediate_steps"] + [result]
    }
```

### Graph

```python
def planning_router(state: PlanningState):
    """Routes to the executor or synthesizer based on the plan."""
    if not state["plan"]:
        console.print("--- ROUTER: Plan complete. Moving to synthesizer. ---")
        return "synthesize"
    else:
        console.print("--- ROUTER: Plan has more steps. Continuing execution. ---")
        return "execute"

planning_graph_builder = StateGraph(PlanningState)
planning_graph_builder.add_node("plan", planner_node)
planning_graph_builder.add_node("execute", executor_node)
planning_graph_builder.add_node("synthesize", synthesizer_node)
planning_graph_builder.set_entry_point("plan")
planning_graph_builder.add_conditional_edges("plan", planning_router)
planning_graph_builder.add_conditional_edges("execute", planning_router)
planning_graph_builder.add_edge("synthesize", END)
planning_agent_app = planning_graph_builder.compile()
```

### Evaluation

```
{
    'task_completion_score': 8,
    'process_efficiency_score': 9,
    'justification': "The agent created a clear, optimal plan upfront and executed it without any unnecessary steps."
}
```

---

## PEV (Planner-Executor-Verifier)

The Planning agent assumes things won't go wrong. **PEV** adds a critical layer of quality control and self-correction — a Verifier that checks each step's output before proceeding.

**Workflow:**

1. **Plan**: A Planner agent creates a sequence of steps.
2. **Execute**: An Executor takes the next step and calls the tool.
3. **Verify**: A Verifier examines the tool's output for correctness, relevance, and errors.
4. **Route & Iterate**:
   - If the step succeeded → move to the next step.
   - If the step failed → loop back to the Planner with awareness of the failure.

### Verifier

```python
class VerificationResult(BaseModel):
    """Schema for the Verifier's output."""
    is_successful: bool = Field(description="True if the tool execution was successful and the data is valid.")
    reasoning: str = Field(description="Reasoning for the verification decision.")

def verifier_node(state: PEVState):
    """Checks the last tool result for errors."""
    console.print("--- VERIFIER: Checking last tool result... ---")
    verifier_llm = llm.with_structured_output(VerificationResult)
    prompt = f"Verify if the following tool output is a successful, valid result or an error message. The task was '{state['user_request']}'.\n\nTool Output: '{state['last_tool_result']}'"
    verification = verifier_llm.invoke(prompt)
    console.print(f"--- VERIFIER: Judgment is '{'Success' if verification.is_successful else 'Failure'}' ---")
    if verification.is_successful:
        return {"intermediate_steps": state["intermediate_steps"] + [state['last_tool_result']]}
    else:
        return {"plan": [], "intermediate_steps": state["intermediate_steps"] + [f"Verification Failed: {state['last_tool_result']}"]}
```

### Router

```python
def pev_router(state: PEVState):
    """Routes execution based on verification and plan status."""
    if not state["plan"]:
        if state["intermediate_steps"] and "Verification Failed" in state["intermediate_steps"][-1]:
            console.print("--- ROUTER: Verification failed. Re-planning... ---")
            return "plan"
        else:
            console.print("--- ROUTER: Plan complete. Moving to synthesizer. ---")
            return "synthesize"
    else:
        console.print("--- ROUTER: Plan has more steps. Continuing execution. ---")
        return "execute"
```

### Evaluation

```
{
    'task_completion_score': 8,
    'error_handling_score': 10,
    'justification': "The agent demonstrated perfect robustness. It successfully identified the tool failure using its Verifier, triggered a re-planning loop, and formulated a new query to circumvent the problem."
}
```

> PEV isn't just about getting the right answer when things go well — it's about **not getting the wrong answer when things go wrong**.

---

## Tree-of-Thoughts (ToT)

PEV handles tool failures with a new linear plan. But what if the problem is more like a maze with dead ends and multiple possible paths? **ToT** explores multiple reasoning paths at once, evaluates them, prunes the bad ones, and continues exploring the most promising branches.

**Workflow:**

1. **Decomposition**: The problem is broken into a series of steps or "thoughts."
2. **Thought Generation**: For the current state, the agent generates multiple potential next steps (branches).
3. **State Evaluation**: Each potential step is evaluated by a critic or validation function.
4. **Pruning & Expansion**: Bad branches are pruned; the remaining good ones are expanded.
5. **Solution**: This continues until a branch reaches the final goal.

### Core Implementation

```python
class PuzzleState(BaseModel):
    left_bank: set[str] = Field(default_factory=lambda: {"wolf", "goat", "cabbage"})
    right_bank: set[str] = Field(default_factory=set)
    boat_location: str = "left"
    move_description: str = "Initial state."

class ToTState(TypedDict):
    problem_description: str
    active_paths: List[List[PuzzleState]]
    solution: Optional[List[PuzzleState]]

def expand_paths(state: ToTState) -> Dict[str, Any]:
    """The 'Thought Generator'. Expands each active path with all valid next moves."""
    console.print("--- Expanding Paths ---")
    new_paths = []
    for path in state['active_paths']:
        last_state = path[-1]
        possible_next_states = get_possible_moves(last_state)
        for next_state in possible_next_states:
            new_paths.append(path + [next_state])
    console.print(f"[cyan]Expanded to {len(new_paths)} potential paths.[/cyan]")
    return {"active_paths": new_paths}

def prune_paths(state: ToTState) -> Dict[str, Any]:
    """The 'State Evaluator'. Prunes paths that are invalid or contain cycles."""
    console.print("--- Pruning Paths ---")
    pruned_paths = []
    for path in state['active_paths']:
        if path[-1] in path[:-1]:
            continue
        pruned_paths.append(path)
    console.print(f"[green]Pruned down to {len(pruned_paths)} valid, non-cyclical paths.[/green]")
    return {"active_paths": pruned_paths}
```

### Solution Output (Wolf, Goat, Cabbage Puzzle)

```
1. Initial state.
2. Move goat to the right bank.
3. Move the boat empty to the left bank.
4. Move wolf to the right bank.
5. Move goat to the left bank.
6. Move cabbage to the right bank.
7. Move the boat empty to the left bank.
8. Move goat to the right bank.
```

### Evaluation

```
{
    'solution_correctness_score': 8,
    'reasoning_robustness_score': 9,
    'justification': "The agent's process was perfectly robust. It systematically explored a tree of possibilities, pruned invalid paths, and guaranteed a correct solution."
}
```

---

## Multi-Agent Systems

Instead of building one super-agent that does everything, **Multi-Agent Systems** use a team of specialists. Each agent focuses on its own domain, just like human experts do.

**Workflow:**

1. **Decomposition**: A complex task is broken down into sub-tasks.
2. **Role Definition**: Each sub-task is assigned to a specialist agent.
3. **Collaboration**: The agents execute their tasks, passing findings to each other or a central manager.
4. **Synthesis**: A final "manager" agent collects outputs and assembles the final response.

### Specialist Factory

```python
class AgentState(TypedDict):
    user_request: str
    news_report: Optional[str]
    technical_report: Optional[str]
    financial_report: Optional[str]
    final_report: Optional[str]

def create_specialist_node(persona: str, output_key: str):
    """Factory function to create a specialist agent node."""
    system_prompt = persona + "\n\nYou have access to a web search tool. Your output MUST be a concise report section, focusing only on your area of expertise."
    
    prompt = ChatPromptTemplate.from_messages([("system", system_prompt), ("human", "{user_request}")])
    agent = prompt | llm.bind_tools([search_tool])
    def specialist_node(state: AgentState):
        console.print(f"--- CALLING {output_key.replace('_report','').upper()} ANALYST ---")
        result = agent.invoke({"user_request": state["user_request"]})
        return {output_key: result.content}
    return specialist_node

news_analyst_node = create_specialist_node("You are an expert News Analyst...", "news_report")
technical_analyst_node = create_specialist_node("You are an expert Technical Analyst...", "technical_report")
financial_analyst_node = create_specialist_node("You are an expert Financial Analyst...", "financial_report")
```

### Graph

```python
multi_agent_graph_builder = StateGraph(AgentState)
multi_agent_graph_builder.add_node("news_analyst", news_analyst_node)
multi_agent_graph_builder.add_node("technical_analyst", technical_analyst_node)
multi_agent_graph_builder.add_node("financial_analyst", financial_analyst_node)
multi_agent_graph_builder.add_node("report_writer", report_writer_node)
multi_agent_graph_builder.set_entry_point("news_analyst")
multi_agent_graph_builder.add_edge("news_analyst", "technical_analyst")
multi_agent_graph_builder.add_edge("technical_analyst", "financial_analyst")
multi_agent_graph_builder.add_edge("financial_analyst", "report_writer")
multi_agent_graph_builder.add_edge("report_writer", END)
multi_agent_app = multi_agent_graph_builder.compile()
```

### Evaluation

```
{
    'clarity_and_structure_score': 9,
    'analytical_depth_score': 8,
    'completeness_score': 9,
    'justification': "The report is exceptionally well-structured with clear, distinct sections for each analysis type."
}
```

> For complex tasks that can be broken down, **a team of specialists will almost always outperform a single generalist**.

---

## Meta-Controller

Multi-agent teams can be rigid — hardcoded sequences run all analysts even when only one is needed. The **Meta-Controller** is a smart dispatcher: its only job is to look at the user's request and decide which specialist is right for the job.

**Workflow:**

1. **Receive Input**: The system gets a user request.
2. **Meta-Controller Analysis**: The controller examines the request to understand its intent.
3. **Dispatch to Specialist**: It selects the best specialist from its pool of experts.
4. **Execute Task**: The chosen specialist generates a result.
5. **Return Result**: The specialist's result is returned to the user.

### Controller

```python
class ControllerDecision(BaseModel):
    """The routing decision made by the Meta-Controller."""
    next_agent: str = Field(description="The name of the specialist agent to call next. Must be one of ['Generalist', 'Researcher', 'Coder'].")
    reasoning: str = Field(description="A brief reason for choosing the next agent.")

def meta_controller_node(state: MetaAgentState):
    """The central controller that decides which specialist to call."""
    console.print("--- 🧠 Meta-Controller Analyzing Request ---")
    
    specialists = {
        "Generalist": "Handles casual conversation, greetings, and simple questions.",
        "Researcher": "Answers questions requiring up-to-date information from the web.",
        "Coder": "Writes Python code based on a user's specification."
    }
    specialist_descriptions = "\n".join([f"- {name}: {desc}" for name, desc in specialists.items()])
    
    # ... (build prompt and invoke controller_llm) ...
    return {"next_agent_to_call": decision.next_agent}
```

### Graph

```python
class MetaAgentState(TypedDict):
    user_request: str
    next_agent_to_call: Optional[str]
    generation: str

workflow = StateGraph(MetaAgentState)
workflow.add_node("meta_controller", meta_controller_node)
workflow.add_node("Generalist", generalist_node)
workflow.add_node("Researcher", research_agent_node)
workflow.add_node("Coder", coder_node)
workflow.set_entry_point("meta_controller")

def route_to_specialist(state: MetaAgentState) -> str:
    return state["next_agent_to_call"]

workflow.add_conditional_edges("meta_controller", route_to_specialist)
workflow.add_edge("Generalist", END)
workflow.add_edge("Researcher", END)
workflow.add_edge("Coder", END)
meta_agent = workflow.compile()
```

### Example Routing

```
--- 🧠 Meta-Controller Analyzing Request ---
Routing decision: Send to Generalist. Reason: The user's request is a simple greeting...

--- 🧠 Meta-Controller Analyzing Request ---
Routing decision: Send to Researcher. Reason: The user is asking about a recent event...

--- 🧠 Meta-Controller Analyzing Request ---
Routing decision: Send to Coder. Reason: The user is explicitly asking for a Python function...
```

> This makes AI systems scalable and easy to maintain — new skills can be added by plugging in specialists and updating the controller.

---

## Blackboard

A rigid sequence is inefficient when the best next step depends on the results of the previous one. The **Blackboard** architecture uses a *shared workspace* where any specialist can write findings, and a controller dynamically decides who contributes next.

**Workflow:**

1. **Shared Memory (The Blackboard)**: A central data store holds the current state and all findings.
2. **Specialist Agents**: A pool of independent agents monitors the blackboard.
3. **Controller**: Analyzes the current state and decides which specialist runs next.
4. **Opportunistic Activation**: The Controller activates the chosen agent; the agent reads, works, and writes back.
5. **Iteration**: Repeats until the controller decides the problem is solved.

### Controller (Loop)

```python
class BlackboardState(TypedDict):
    user_request: str
    blackboard: List[str]
    available_agents: List[str]
    next_agent: Optional[str]

def controller_node(state: BlackboardState):
    """The intelligent controller that analyzes the blackboard and decides the next step."""
    console.print("--- CONTROLLER: Analyzing blackboard... ---")
    controller_llm = llm.with_structured_output(ControllerDecision)
    blackboard_content = "\n\n".join(state['blackboard'])
    
    prompt = f"""You are the central controller of a multi-agent system. Your job is to analyze the shared blackboard and the original user request to decide which specialist agent should run next.
**Original User Request:**
{state['user_request']}
**Current Blackboard Content:**
---
{blackboard_content if blackboard_content else "The blackboard is currently empty."}
---
**Available Specialist Agents:**
{', '.join(state['available_agents'])}
**Your Task:**
1. Read the user request and the current blackboard content carefully.
2. Determine what the *next logical step* is to move closer to a complete answer.
3. Choose the single best agent to perform that step.
4. If the request has been fully addressed, choose 'FINISH'.
"""
    decision = controller_llm.invoke(prompt)
    return {"next_agent": decision.next_agent}
```

### Graph (All specialists loop back to Controller)

```python
bb_graph_builder = StateGraph(BlackboardState)
bb_graph_builder.add_node("Controller", controller_node)
bb_graph_builder.add_node("News Analyst", news_analyst_bb)
# ... add other specialist nodes ...
bb_graph_builder.set_entry_point("Controller")

bb_graph_builder.add_conditional_edges("Controller", route_to_agent, {
    "News Analyst": "News Analyst",
    # ... other routes ...
    "FINISH": END
})

# After any specialist runs, control always returns to the Controller
bb_graph_builder.add_edge("News Analyst", "Controller")
# ... other edges back to controller ...
blackboard_app = bb_graph_builder.compile()
```

### Evaluation

```
{
    'instruction_following_score': 7,
    'process_efficiency_score': 8,
    'justification': "The agent perfectly followed the user's conditional instructions. After positive news, the system correctly chose Technical Analyst and completely skipped Financial Analyst."
}
```

---

## Ensemble Decision-Making

All previous agents produce a single line of reasoning. LLMs are non-deterministic — the same prompt can yield different answers. **Ensemble Decision-Making** runs multiple independent agents in parallel (often with different "personalities"), then uses an aggregator to synthesize their outputs into a more robust conclusion.

**Workflow:**

1. **Fan-Out (Parallel Exploration)**: A query is sent to multiple specialist agents simultaneously with different personas.
2. **Independent Processing**: Each agent works in isolation, generating its own complete analysis.
3. **Fan-In (Aggregation)**: Outputs from all agents are collected.
4. **Synthesize**: A final "aggregator" agent weighs the different viewpoints and synthesizes a comprehensive final answer.

### Diverse Personas

```python
class EnsembleState(TypedDict):
    query: str
    analyses: Dict[str, str]
    final_recommendation: Optional[Any]

bullish_persona = "The Bullish Growth Analyst: You are extremely optimistic about technology and innovation. Focus on future growth potential and downplay short-term risks."
bullish_analyst_node = create_specialist_node(bullish_persona, "BullishAnalyst")

value_persona = "The Cautious Value Analyst: You are a skeptical investor focused on fundamentals and risk. Scrutinize financials, competition, and potential downside scenarios."
value_analyst_node = create_specialist_node(value_persona, "ValueAnalyst")

quant_persona = "The Quantitative Analyst (Quant): You are purely data-driven. Ignore narratives and focus only on hard numbers like financial metrics and technical indicators."
quant_analyst_node = create_specialist_node(quant_persona, "QuantAnalyst")
```

### Fan-Out / Fan-In Graph

```python
workflow = StateGraph(EnsembleState)
workflow.add_node("start_analysis", lambda state: {"analyses": {}})
workflow.add_node("bullish_analyst", bullish_analyst_node)
workflow.add_node("value_analyst", value_analyst_node)
workflow.add_node("quant_analyst", quant_analyst_node)
workflow.add_node("cio_synthesizer", cio_synthesizer_node)
workflow.set_entry_point("start_analysis")

# FAN-OUT: Run all three analysts in parallel
workflow.add_edge("start_analysis", ["bullish_analyst", "value_analyst", "quant_analyst"])

# FAN-IN: After all analysts are done, call the synthesizer
workflow.add_edge(["bullish_analyst", "value_analyst", "quant_analyst"], "cio_synthesizer")
workflow.add_edge("cio_synthesizer", END)
ensemble_agent = workflow.compile()
```

### Example Output

```
**Final Recommendation:** Buy
**Confidence Score:** 7.5/10

**Synthesis Summary:**
The committee presents a compelling but contested case for NVIDIA. There is unanimous agreement on
the company's current technological dominance... However, the Value and Quant analysts raise
critical, concurring points about the stock's extremely high valuation...

**Identified Opportunities:**
* Unquestioned leadership in the AI accelerator market.

**Identified Risks:**
* Extremely high valuation (P/E and P/S ratios).
```

### Evaluation

```
{
    'analytical_depth_score': 9,
    'nuance_and_balance_score': 8,
    'justification': "The final answer is exceptionally well-balanced. It masterfully synthesizes the optimistic growth case with the skeptical valuation concerns."
}
```

---

## Episodic + Semantic Memory

All previous agents have the memory of a goldfish — once the conversation is over, everything is forgotten. The **Episodic + Semantic Memory Stack** mimics human cognition by giving the agent two types of long-term memory:

- **Episodic Memory**: Memory of specific events / past conversations ("What happened?") — stored in a vector database.
- **Semantic Memory**: Memory of structured facts and relationships ("What do I know?") — stored in a graph database (Neo4j).

**Workflow:**

1. **Interaction**: The agent has a conversation with the user.
2. **Memory Retrieval**: For a new query, the agent searches both memories for relevant context.
3. **Augmented Generation**: Retrieved memories are used to generate a personalized response.
4. **Memory Creation**: A "memory maker" analyzes the conversation, creates a summary (episodic) and extracts facts (semantic).
5. **Memory Storage**: New memories are saved to their respective databases.

### Memory Maker

```python
class Node(BaseModel):
    id: str; type: str

class Relationship(BaseModel):
    source: Node; target: Node; type: str

class KnowledgeGraph(BaseModel):
    relationships: List[Relationship]

def create_memories(user_input: str, assistant_output: str):
    conversation = f"User: {user_input}\nAssistant: {assistant_output}"
    
    # Create Episodic Memory (Summarization)
    summary_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a summarization expert. Create a concise, one-sentence summary of the following user-assistant interaction."),
        ("human", "Interaction:\n{interaction}")
    ])
    summarizer = summary_prompt | llm
    episodic_summary = summarizer.invoke({"interaction": conversation}).content
    
    new_doc = Document(page_content=episodic_summary, metadata={"created_at": uuid.uuid4().hex})
    episodic_vector_store.add_documents([new_doc])
    
    # Create Semantic Memory (Fact Extraction)
    extraction_llm = llm.with_structured_output(KnowledgeGraph)
    # ... (extract and save relationships to Neo4j graph) ...
```

### Example (Multi-turn Test)

```
--- 💬 INTERACTION 1: Seeding Memory ---
User: "Hi, my name is Alex. I'm a conservative investor, mainly interested in established tech companies."
Episodic memory created: 'User Alex is conservative investor in tech...'
Semantic memory created: Added 2 relationships...

--- 💬 INTERACTION 2: Memory Test ---
User: "Based on my goals, what's a good alternative to Apple?"
Retrieved Context: Alex as conservative investor...
Generated Response: Apple (AAPL) fits conservative tech portfolio, strong brand, stable revenue...
```

### Evaluation

```
{
    'personalization_score': 7,
    'justification': "The agent's response was perfectly personalized. It explicitly referenced the user's stated goal of being a 'conservative investor' recalled from a previous conversation."
}
```

---

## Graph (World-Model) Memory

The previous memory system can recall facts but struggles to understand the complex *web of relationships* between facts. **Graph Memory** builds a structured, interconnected "world model" — ingesting unstructured text and converting it into a rich knowledge graph of entities (nodes) and relationships (edges).

**Workflow:**

1. **Information Ingestion**: The agent reads unstructured text.
2. **Knowledge Extraction**: An LLM-powered process identifies key entities and the relationships connecting them.
3. **Graph Update**: Extracted nodes and edges are added to a persistent graph database (Neo4j).
4. **Question Answering**: The agent converts a user's query into a Cypher query, executes it, and synthesizes the results.

### Graph Maker

```python
class Node(BaseModel):
    id: str = Field(description="Unique name or identifier for the entity.")
    type: str = Field(description="The type of the entity (e.g., Person, Company).")

class Relationship(BaseModel):
    source: Node
    target: Node
    type: str = Field(description="The type of relationship (e.g., WORKS_FOR, ACQUIRED).")

class KnowledgeGraph(BaseModel):
    relationships: List[Relationship]

def get_graph_maker_chain():
    extractor_llm = llm.with_structured_output(KnowledgeGraph)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert at extracting information. Extract all entities and relationships from the provided text. The relationship type should be a verb in all caps, like 'WORKS_FOR'."),
        ("human", "Extract a knowledge graph from the following text:\n\n{text}")
    ])
    return prompt | extractor_llm
```

### Text-to-Cypher Query

```python
def query_graph(question: str) -> Dict[str, Any]:
    # 1. Generate Cypher Query
    generated_cypher = cypher_chain.invoke(f"Convert this question to a Cypher query using this schema: {graph.schema}\nQuestion: {question}").content
    
    # 2. Execute Cypher Query
    context = graph.query(generated_cypher)
    
    # 3. Synthesize Final Answer
    answer = synthesis_chain.invoke(f"Answer this question: {question}\nUsing this data: {context}").content
    
    return {"answer": answer}
```

### Multi-hop Example

Given three separate text documents:
- "AlphaCorp announced its acquisition of startup BetaSolutions."
- "Dr. Evelyn Reed is the Chief Science Officer at AlphaCorp."
- "Innovate Inc.'s flagship product, NeuraGen, competes with AlphaCorp's QuantumLeap AI."

**Query**: *"Who works for the company that acquired BetaSolutions?"*

```
Generated Cypher:
MATCH (p:Person)-[:WORKS_FOR]->(c:Company)-[:ACQUIRED]->(:Company {id: 'BetaSolutions'}) RETURN p.id

Query Result: [{'p.id': 'Dr. Evelyn Reed'}]

Final Answer: Dr. Evelyn Reed works for the company that acquired BetaSolutions, which is AlphaCorp.
```

### Evaluation

```
{
    'multi_hop_accuracy_score': 7,
    'justification': "The agent demonstrated perfect multi-hop reasoning. It correctly identified the acquiring company from one fact and then used that to find an employee from a completely separate fact."
}
```

---

## Self-Improvement Loop (RLHF Analogy)

The agent we build today will be the same agent tomorrow — unless we give it a **Self-Improvement Loop**. This architecture mimics the human learning cycle of do → get feedback → improve. An agent's output is evaluated, and if it's not good enough, the agent is forced to revise based on specific feedback.

**Workflow:**

1. **Generate Initial Output**: A "junior" agent produces a first draft.
2. **Critique Output**: A "senior" critic agent evaluates the draft against a strict rubric.
3. **Decision**: Check if the critique's score meets a quality threshold.
4. **Revise (Loop)**: If the score is too low, the draft and feedback are passed back to the junior agent.
5. **Accept**: Once approved, the loop terminates.

### Chains

```python
class MarketingEmail(BaseModel):
    subject: str = Field(description="A catchy and concise subject line for the email.")
    body: str = Field(description="The full body text of the email, written in markdown.")

class Critique(BaseModel):
    score: int = Field(description="Overall quality score from 1 (poor) to 10 (excellent).")
    feedback_points: List[str] = Field(description="A bulleted list of specific, actionable feedback points for improvement.")
    is_approved: bool = Field(description="A boolean indicating if the draft is approved (score >= 8).")

def get_generator_chain():
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a junior marketing copywriter..."),
        ("human", "Write a marketing email about the following topic:\n\n{request}")
    ])
    return prompt | llm.with_structured_output(MarketingEmail)

def get_critic_chain():
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a senior marketing editor. Evaluate the draft against:
        1. Catchy Subject
        2. Clarity & Persuasiveness
        3. Strong Call-to-Action (CTA)
        4. Brand Voice
        Provide a score from 1-10. Score >= 8 means approved."""),
        ("human", "Please critique:\n\n**Subject:** {subject}\n\n**Body:**\n{body}")
    ])
    return prompt | llm.with_structured_output(Critique)
```

### Graph

```python
def should_continue(state: AgentState) -> str:
    if state['critique'].is_approved:
        return "end"
    if state['revision_number'] >= 3:
        return "end"
    else:
        return "continue"

workflow = StateGraph(AgentState)
workflow.add_node("generate", generate_node)
workflow.add_node("critique", critique_node)
workflow.add_node("revise", revise_node)

workflow.set_entry_point("generate")
workflow.add_edge("generate", "critique")
workflow.add_conditional_edges("critique", should_continue, {"continue": "revise", "end": END})
workflow.add_edge("revise", "critique")
self_refine_agent = workflow.compile()
```

### Improvement Trace

| Revision | Score | Notes |
|---|---|---|
| Draft 1 | 4/10 | Generic subject, simplistic body, weak CTA |
| Draft 2 | 9/10 | Catchy subject, persuasive body, clear CTA — **Approved** |

---

## Dry-Run Harness

If an agent is given real-world powers (like sending emails) without safety controls, it can take dangerous actions. The **Dry-Run Harness** principle is simple: *look before you leap*.

The agent first runs in "dry run" mode that simulates the action without actually doing it. This generates a clear plan and logs, which are presented to a human for approval before live execution.

**Workflow:**

1. **Propose Action**: The agent decides to take a real-world action.
2. **Dry Run Execution**: The harness calls the tool with `dry_run=True`. The tool only outputs what it *would* do.
3. **Human/Automated Review**: The dry-run logs are shown to a reviewer.
4. **Go/No-Go Decision**: The reviewer gives approve or reject.
5. **Live Execution**: If approved, the harness calls the tool with `dry_run=False`.

### Tool with Dry-Run Support

```python
class SocialMediaAPI:
    """A mock social media API that supports a dry-run mode."""
    def publish_post(self, post: SocialMediaPost, dry_run: bool = True) -> Dict[str, Any]:
        full_post_text = f"{post.content}\n\n{' '.join([f'#{h}' for h in post.hashtags])}"
        if dry_run:
            log_message = f"[DRY RUN] Would publish the following post:\n{full_post_text}"
            console.print(Panel(log_message, title="[yellow]Dry Run Log[/yellow]"))
            return {"status": "DRY_RUN_SUCCESS", "proposed_post": full_post_text}
        else:
            log_message = "[LIVE] Successfully published post!"
            return {"status": "LIVE_SUCCESS", "post_id": "post_12345"}
```

### Conditional Edge

```python
def route_after_review(state: AgentState) -> str:
    return "execute_live" if state["review_decision"] == "approve" else "reject"
```

### Evaluation

```
{
    'action_safety_score': 10,
    'justification': "The system demonstrated perfect operational safety. It generated a potentially brand-damaging post but intercepted it during the dry-run phase. The human-in-the-loop review correctly identified the risk and prevented the live execution."
}
```

> The Dry-Run Harness is a key architecture for moving agents from the lab to production, giving the transparency and control needed to operate safely.

---

## Simulator (Mental-Model-in-the-Loop)

PEV-like agents handle tool failures in static environments. In *dynamic* environments — like a stock market where the situation constantly changes — **Simulator** agents test their proposed strategy in a safe, internal simulation before committing to real-world action.

**Workflow:**

1. **Observe**: The agent observes the current state of the real environment.
2. **Propose Action**: An "analyst" module generates a high-level strategy.
3. **Simulate**: The agent forks the environment state into a sandboxed simulation, applies the strategy, and runs it forward to see possible outcomes.
4. **Assess & Refine**: A "risk manager" module analyzes the simulation results and refines the initial proposal.
5. **Execute**: The agent executes the final, refined action in the real environment.

### World Simulator

```python
class MarketSimulator(BaseModel):
    """A simple simulation of a stock market for one asset."""
    day: int = 0
    price: float = 100.0
    volatility: float = 0.1
    drift: float = 0.01
    market_news: str = "Market is stable."
    portfolio: Portfolio = Field(default_factory=Portfolio)

    def step(self, action: str, amount: float = 0.0):
        """Advance the simulation by one day, executing a trade first."""
        # 1. Execute trade
        if action == "buy":
            shares_to_buy = int(amount)
            cost = shares_to_buy * self.price
            if self.portfolio.cash >= cost:
                self.portfolio.shares += shares_to_buy
                self.portfolio.cash -= cost
        elif action == "sell":
            shares_to_sell = int(amount)
            if self.portfolio.shares >= shares_to_sell:
                self.portfolio.shares -= shares_to_sell
                self.portfolio.cash += shares_to_sell * self.price
        
        # 2. Update market price (Geometric Brownian Motion)
        daily_return = np.random.normal(self.drift, self.volatility)
        self.price *= (1 + daily_return)
        self.day += 1
```

### Simulation Node

```python
def run_simulation_node(state: AgentState) -> Dict[str, Any]:
    """Runs the proposed strategy in a sandboxed simulation."""
    strategy = state['proposed_action'].strategy
    num_simulations = 5
    simulation_horizon = 10
    results = []

    for i in range(num_simulations):
        # IMPORTANT: Create a deep copy to not affect the real market state
        simulated_market = state['real_market'].model_copy(deep=True)
        # ... (translate strategy, run simulation, record results) ...
    
    return {"simulation_results": results}
```

### Execution Trace

```
--- Day 1: Good News Hits! ---
Analyst Proposal: buy aggressively. Reason: Positive earnings report is a strong bullish signal...
Running Simulations...
Risk Manager Final Decision: buy 20 shares. Reason: Simulations confirm strong upward trend...

--- Day 2: Bad News Hits! ---
Analyst Proposal: sell cautiously. Reason: New competitor introduces significant uncertainty...
Running Simulations...
Risk Manager Final Decision: sell 5 shares. Reason: Simulations show high variance, de-risk portfolio...
```

### Evaluation

```
{
    'decision_robustness_score': 6,
    'risk_management_score': 9,
    'justification': "The agent's decisions were directly informed by a robust simulation process. It correctly identified the opportunity on day 1 and appropriately de-risked on day 2."
}
```

---

## Reflexive Metacognitive

Our agents can now plan, handle errors, and simulate the future. But they all share a critical vulnerability — they don't know what they don't know. A standard agent, if asked a question outside its expertise, will still try its best, often leading to confidently wrong information.

**Reflexive Metacognitive** gives an agent a form of *self-awareness*. Before solving a problem, it first reasons about its own capabilities, confidence, and limitations.

**Workflow:**

1. **Perceive Task**: The agent receives a user request.
2. **Metacognitive Analysis**: The agent analyzes the request against its own self-model — assessing confidence, available tools, and domain scope.
3. **Strategy Selection**:
   - **Reason Directly**: For high-confidence, low-risk queries.
   - **Use Tool**: When the query requires a specific tool the agent has.
   - **Escalate/Refuse**: For low-confidence, high-risk, or out-of-scope queries.
4. **Execute Strategy**: The chosen path is executed.

### Self-Model

```python
class AgentSelfModel(BaseModel):
    """A structured representation of the agent's capabilities and limitations."""
    name: str; role: str
    knowledge_domain: List[str]
    available_tools: List[str]

medical_agent_model = AgentSelfModel(
    name="TriageBot-3000",
    role="A helpful AI assistant for providing preliminary medical information.",
    knowledge_domain=["common_cold", "influenza", "allergies", "basic_first_aid"],
    available_tools=["drug_interaction_checker"]
)
```

### Metacognitive Analysis Node

```python
class MetacognitiveAnalysis(BaseModel):
    confidence: float
    strategy: str = Field(description="Must be one of: 'reason_directly', 'use_tool', 'escalate'.")
    reasoning: str

def metacognitive_analysis_node(state: AgentState):
    """The agent's self-reflection step."""
    prompt = ChatPromptTemplate.from_template(
        """You are a metacognitive reasoning engine for an AI assistant. Your primary directive is SAFETY. Analyze the user's query in the context of the agent's own 'self-model' and choose the safest strategy.
        **WHEN IN DOUBT, ESCALATE.**
        **Agent's Self-Model:** {self_model}
        **User Query:** "{query}"
        """
    )
    chain = prompt | llm.with_structured_output(MetacognitiveAnalysis)
    analysis = chain.invoke({"query": state['user_query'], "self_model": state['self_model'].model_dump_json()})
    return {"metacognitive_analysis": analysis}
```

### Three-Query Test

| Query | Confidence | Strategy |
|---|---|---|
| "What are the symptoms of a common cold?" | 0.90 | `reason_directly` |
| "Is it safe to take Ibuprofen with Lisinopril?" | 0.95 | `use_tool` (drug_interaction_checker) |
| "I have a crushing pain in my chest, what should I do?" | 0.10 | `escalate` |

### Evaluation

```
{
    'safety_score': 8,
    'self_awareness_score': 10,
    'justification': "The agent correctly identified the query as a potential medical emergency, recognized it was outside its defined scope, and immediately escalated to a human expert without attempting to provide medical advice."
}
```

> Knowing what you don't know is the most important knowledge of all.

---

## Cellular Automata

For our final architecture, we take a completely different approach. All previous agents have been "top-down" — a central, intelligent agent makes decisions and executes plans. **Cellular Automata** flips this on its head: a massive number of simple, decentralized agents operate on a grid. There's no single controller. Smart overall behavior emerges from applying simple local rules over and over.

**Workflow:**

1. **Grid Initialization**: A grid of "cell-agents" is created, each with a simple type and state.
2. **Set Boundary Conditions**: A target cell is given a special state to start the computation (e.g., value = 0).
3. **Synchronous Tick**: In each "tick," every cell simultaneously calculates its next state based only on its immediate neighbors.
4. **Emergence**: Information spreads across the grid like a wave, creating gradients and paths.
5. **State Stabilization**: The system runs until the grid stops changing.
6. **Readout**: The solution is read directly from the final state of the grid.

### Core Implementation

```python
class CellAgent:
    """A single agent in our grid. Its only job is to update its value based on neighbors."""
    def __init__(self, cell_type: str):
        self.type = cell_type  # 'EMPTY', 'OBSTACLE', 'PACKING_STATION', etc.
        self.pathfinding_value = float('inf')

    def update_value(self, neighbors: List['CellAgent']):
        """The core local rule."""
        if self.type == 'OBSTACLE': return float('inf')
        min_neighbor_value = min([n.pathfinding_value for n in neighbors])
        return min(self.pathfinding_value, min_neighbor_value + 1)


class WarehouseGrid:
    def __init__(self, layout):
        self.h, self.w = len(layout), len(layout[0])
        self.grid = np.array([[self._cell(ch) for ch in row] for row in layout], dtype=object)

    def tick(self):
        vals = np.array([[cell.update_value(self.neighbors(r,c))
                          for c,cell in enumerate(row)] for r,row in enumerate(self.grid)])
        changed = False
        for r,row in enumerate(self.grid):
            for c,cell in enumerate(row):
                if cell.pathfinding_value != vals[r,c]: changed = True
                cell.pathfinding_value = vals[r,c]
        return changed


def propagate_path_wave(grid: WarehouseGrid, target_pos: Tuple[int, int]):
    """Resets and then runs the simulation until the pathfinding values stabilize."""
    for cell in grid.grid.flatten(): cell.pathfinding_value = float('inf')
    grid.grid[target_pos].pathfinding_value = 0
    
    while grid.tick():
        pass
```

### Warehouse Pathfinding Example

Given this warehouse layout:

```
#######
#A    #
# ### #
#   # #
# # # #
#  P  #
#######
```

The wave propagation (Breadth-First Search via local rules) spreads from Packing Station `P`, filling every cell with its distance to `P`:

```
Path Wave Propagation (Stabilized at Tick #17)
┌─────────────────────────────────┐
│  █    █    █    █    █    █   █ │
│   7    6    5    D    5    6  █  │
│   6    5    4    3    4    5   6 │
│   A    4    3    2    C    6   7 │
│   6    5    4    1    5    B   8 │
│   7    6    5    P    6    7   8 │
│  █    █    █    █    █    █   █ │
└─────────────────────────────────┘
```

The robot follows the gradient downhill from any starting cell to reach `P` via the shortest path.

```
Step 1: Fulfill Item 'A'
🌊 Computing path wave from Packing Station...
🚚 Path: (3, 0) -> (3, 1) -> (3, 2) -> (4, 2) -> (5, 2) -> (5, 3)
✅ Item 'A' has been moved to the packing station.

Step 2: Fulfill Item 'B'
🌊 Computing path wave from Packing Station...
🚚 Path: (4, 5) -> (4, 4) -> (4, 3) -> (5, 3)
✅ Item 'B' has been moved to the packing station.
```

### Evaluation

```
{
    'optimality_score': 7,
    'robustness_score': 8,
    'justification': "The wave propagation method is a form of Breadth-First Search, which guarantees the shortest path. Furthermore, the solution is emergent from local rules, meaning if an obstacle is added, re-running the simulation will automatically find a new optimal path without any change to the core algorithm."
}
```

---

## Combining Architectures Together

Advanced AI systems don't rely on a single architecture — they orchestrate multiple patterns into multi-layered workflows, assigning each module the subtask it handles most efficiently.

Here's how you could combine several architectures to build a production-grade AI marketing system:

### 1. Contextual Recall
- A **Reflexive Metacognitive** agent verifies the request is within scope.
- A **Meta-Controller** routes the task to the "Competitive Analysis" workflow.
- **Episodic + Semantic Memory** surfaces prior analyses to provide immediate, personalized context.

### 2. Deep Research & World Modeling
- A **ReAct** agent performs multi-hop web searches to gather fresh data.
- In parallel, **Graph (World-Model) Memory** extracts entities and relationships, creating a connected model of the competitor's ecosystem.

### 3. Collaborative Strategy Formulation
- **Ensemble Decision-Making** runs multiple agents in parallel (Bullish, Cautious Brand-Safety, Data-Driven ROI).
- Their outputs are posted to a shared **Blackboard**, where a "CMO" controller synthesizes them into a coherent plan.

### 4. Long-Term Learning
- A "Junior Copywriter" agent iteratively drafts content using a **Generate → Critique → Refine** loop.
- Campaign performance is fed back into a **Self-Improvement Loop**, creating a gold-standard dataset that improves future performance.

### 5. Safe, Simulated Execution
- Final content undergoes a **Dry-Run Harness** for human approval.
- For higher-risk actions like ad-budget allocation, a **Simulator (Mental-Model-in-the-Loop)** predicts outcomes before any real-world commitment.

---

*Article by Fareed Khan, published in Level Up Coding, Sep 26, 2025.*

*GitHub: [FareedKhan-dev/all-agentic-architectures](https://github.com/FareedKhan-dev/all-agentic-architectures)*
