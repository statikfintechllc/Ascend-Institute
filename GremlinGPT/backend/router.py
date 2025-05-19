from backend.api import chat_handler, memory_api, scraping_api, planner


def register_routes(app):
    app.add_url_rule("/api/chat", view_func=chat_handler.chat, methods=["POST"])
    app.add_url_rule("/api/memory/graph", view_func=memory_api.graph, methods=["GET"])
    app.add_url_rule("/api/scrape", view_func=scraping_api.scrape_url, methods=["POST"])
    app.add_url_rule("/api/agent/tasks", view_func=planner.list_tasks, methods=["GET"])
    app.add_url_rule(
        "/api/trading/signals", view_func=planner.get_signals, methods=["GET"]
    )
