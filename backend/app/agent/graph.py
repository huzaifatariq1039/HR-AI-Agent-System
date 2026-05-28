"""
HR AI Agent — LangGraph State Graph
=====================================
Defines the core LangGraph agent architecture:
- State management with MessagesState
- Agent node (LLM decision-making)
- Action node (tool execution via ToolNode)
- Conditional routing between agent ↔ action ↔ END
- MemorySaver checkpointer for multi-turn conversation memory
"""

import os
from typing import Literal

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode

from app.agent.prompts import HR_SYSTEM_PROMPT
from app.tools.recruitment import create_job_posting, list_job_postings
from app.tools.records import get_employee_profile, search_employees
from app.tools.onboarding import get_onboarding_status
from app.tools.payroll import get_payslip_summary
from app.tools.leave import apply_leave, get_leave_balance
from app.tools.performance import get_goals
from app.tools.training import list_training_programs
from app.tools.relations import file_grievance
from app.tools.compliance import get_policy
from app.tools.analytics import get_headcount_metrics
from app.tools.engagement import send_recognition


# ---------------------------------------------------------------------------
# 1. Collect all HR tools
# ---------------------------------------------------------------------------

ALL_HR_TOOLS = [
    # Recruitment
    create_job_posting,
    list_job_postings,
    # Employee Records
    get_employee_profile,
    search_employees,
    # Onboarding
    get_onboarding_status,
    # Payroll
    get_payslip_summary,
    # Leave & Attendance
    apply_leave,
    get_leave_balance,
    # Performance
    get_goals,
    # Training
    list_training_programs,
    # Relations
    file_grievance,
    # Compliance
    get_policy,
    # Analytics
    get_headcount_metrics,
    # Engagement
    send_recognition,
]


# ---------------------------------------------------------------------------
# 2. Initialize the LLM with tools bound
# ---------------------------------------------------------------------------

def _create_llm():
    """Create and configure the ChatOpenAI instance with all HR tools bound."""
    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0.3,
        streaming=True,
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    # Bind all HR tools so the LLM knows about them and can invoke them
    return llm.bind_tools(ALL_HR_TOOLS)


# ---------------------------------------------------------------------------
# 3. Define graph nodes
# ---------------------------------------------------------------------------

def agent_node(state: MessagesState) -> dict:
    """
    The core agent node.
    
    Takes the current conversation state (messages), prepends the system prompt,
    and invokes the LLM. The LLM will either:
    - Produce a direct text response (no tool calls) → route to END
    - Produce a response with tool_calls → route to the action node
    """
    llm = _create_llm()

    # Prepend the system message if it's not already the first message
    messages = state["messages"]
    if not messages or not isinstance(messages[0], SystemMessage):
        messages = [SystemMessage(content=HR_SYSTEM_PROMPT)] + messages

    response = llm.invoke(messages)
    return {"messages": [response]}


# The ToolNode automatically executes whichever tool the LLM selected
# and returns a ToolMessage with the result back into the state.
action_node = ToolNode(ALL_HR_TOOLS)


# ---------------------------------------------------------------------------
# 4. Define conditional routing
# ---------------------------------------------------------------------------

def should_continue(state: MessagesState) -> Literal["action", "__end__"]:
    """
    Conditional edge function.
    
    Examines the last message in the state:
    - If it contains tool_calls → route to the "action" node
    - Otherwise → route to END (the agent is done responding)
    """
    last_message = state["messages"][-1]

    # Check if the LLM wants to call a tool
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "action"

    return "__end__"


# ---------------------------------------------------------------------------
# 5. Build and compile the state graph
# ---------------------------------------------------------------------------

def build_graph():
    """
    Construct the LangGraph state graph for the HR AI Agent.

    Graph structure:
        
        ┌──────────┐    tool_calls?    ┌──────────┐
        │  agent   │ ───────Yes──────► │  action  │
        │  (LLM)  │                    │ (ToolNode)│
        │          │ ◄─────────────── │          │
        └──────────┘    tool result    └──────────┘
             │
             │ No tool_calls
             ▼
           [END]

    Returns:
        A compiled LangGraph with MemorySaver checkpointer.
    """
    # Create the state graph using MessagesState (manages the `messages` list)
    workflow = StateGraph(MessagesState)

    # Add nodes
    workflow.add_node("agent", agent_node)
    workflow.add_node("action", action_node)

    # Set entry point
    workflow.set_entry_point("agent")

    # Add conditional edge: agent → action (if tool calls) or → END
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "action": "action",
            "__end__": END,
        },
    )

    # Add standard edge: action → agent (so LLM can interpret tool results)
    workflow.add_edge("action", "agent")

    # Compile with memory checkpointer for multi-turn conversation support
    memory = MemorySaver()
    compiled_graph = workflow.compile(checkpointer=memory)

    return compiled_graph


# ---------------------------------------------------------------------------
# 6. Module-level graph instance (singleton)
# ---------------------------------------------------------------------------

# The graph is compiled once and reused across all requests.
# The MemorySaver checkpointer handles session isolation via config.
hr_agent_graph = build_graph()
