import logging
from core.model_interface import ask_model
from memory.vector_memory import recall_context, store_context
from utils.linter import score_code_quality  # You’ll need to add this
from tools import tool_registry
import os
from langgraph_core import build_gremlin_graph
from memory.task_journal import log_task_event

logger = logging.getLogger(__name__)
graph = build_gremlin_graph()


def run_as_agent(task_text):
    logger.info(f"[Agent] Running LangGraph on task: {task_text}")
    result = graph.run(task_text)
    store_context(task_text, result)
    log_task_event(task_text, "agent_run", result)
    return result


class GremlinAgent:
    def __init__(self, name="Gremlin", tools=None, memory=None, retry_limit=1):
        self.name = name
        self.tools = tools or {}
        self.memory = memory or []
        self.retry_limit = retry_limit

    def decide(self, task):
        context = recall_context(task)
        prompt = f"Context: {context}\n\nTask: {task}\nDecide action."
        return ask_model(prompt)

    def act(self, task, attempt=1):
        decision = self.decide(task)
        logging.info(f"[{self.name}] Decision: {decision}")

        for tool in self.tools:
            if tool in decision.lower():
                try:
                    result = self.tools[tool]({"command": task})
                    store_context(task, result)
                    return result
                except Exception as e:
                    logging.warning(f"[{self.name}] Tool '{tool}' failed: {e}")
                    if attempt < self.retry_limit:
                        return self.act(task, attempt + 1)
                    return f"[{self.name}] Tool '{tool}' failed permanently."

        # Fallback: execute generated code with lint check
        if "code:" in decision.lower():
            code_block = decision.split("code:")[-1].strip()
            score, notes = score_code_quality(code_block)
            if score < 0.5:
                return f"[Code Reject] Lint score too low: {notes}"
            try:
                exec(code_block, globals())
                return "[Code Executed]"
            except Exception as e:
                return f"[Execution Error] {e}"

        return f"[{self.name}] No valid action found."
