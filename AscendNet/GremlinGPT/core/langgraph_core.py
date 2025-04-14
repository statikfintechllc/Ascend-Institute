from langgraph.graph import Graph
from agents.gremlin_agent import GremlinAgent
from tools import tool_registry
from langgraph.graph import StateGraph
from langgraph.checkpoint import MemorySaver
from langgraph.prebuilt.tool_node import ToolNode
from core.model_interface import ask_model
from tools import tool_registry

def build_gremlin_graph():
    state = StateGraph()

    def ai_router(state):
        if "scrape" in state.lower():
            return "scrape"
        elif "crypto" in state.lower():
            return "buy"
        return "llm"

    def llm_node(task):
        return ask_model(f"[LANGGRAPH LLM TASK]\n{task}")

    state.set_entry_point(ai_router)
    state.add_node("scrape", ToolNode(tool_registry["scrape_web"]))
    state.add_node("buy", ToolNode(tool_registry["buy_crypto"]))
    state.add_node("llm", llm_node)

    state.set_finish_node("llm")  # Default fallback

    return state.compile(MemorySaver())

def build_gremlin_graph():
    agent = GremlinAgent(tools=tool_registry)

    graph = Graph("gremlin-workflow")
    graph.add_node("process", agent.act)
    graph.set_entrypoint("process")

    return graph