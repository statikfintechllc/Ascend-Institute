from flask import Flask
from flask_socketio import SocketIO
from backend.router import register_routes
from loguru import logger
import eventlet

eventlet.monkey_patch()

app = Flask(__name__)
app.config["SECRET_KEY"] = "gremlin_secret"
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")

# Register all REST endpoints
register_routes(app)

logger.add("run/logs/runtime.log", rotation="1 MB")


@app.route("/")
def index():
    return {"message": "GremlinGPT Backend Running."}


if __name__ == "__main__":
    logger.info("[BACKEND] Starting GremlinGPT backend server.")
    socketio.run(app, host="0.0.0.0", port=5050)
