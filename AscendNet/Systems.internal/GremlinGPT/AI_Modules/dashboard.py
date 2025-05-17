import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import logging
import os
import requests
from core.model_interface import ask_model
from tools import tool_registry
from runtime.dreambox_loop import start_dreambox, stop_dreambox

# Initialize Dash App
app = dash.Dash(__name__)

# API Endpoints (these can be swapped to env vars later)
SECURITY_API = "http://localhost:5002/security_scan"
NETWORK_API = "http://localhost:5003/network_status"
QUANTUM_API = "http://localhost:5004/quantum_compute"
LOGS_API = "http://localhost:5005/fetch_logs"

# Dashboard Logic
class UltimateDashboard:
    def __init__(self):
        self.position = {"x": 100, "y": 100}
        self.interaction_state = "idle"
        self.user_sentiment = "neutral"
        logging.info("[UltimateDashboard] Initialized.")

    def call_api(self, api_url, payload=None):
        try:
            response = requests.post(api_url, json=payload) if payload else requests.get(api_url)
            return response.json().get("result", "[AI] No response received.")
        except Exception as e:
            logging.error(f"[Dashboard] API Call Failed: {str(e)}")
            return "[AI] Service communication failed."

ultimate_dashboard = UltimateDashboard()

# Layout
def glowing_golden_eye():
    return html.Div(
        id="golden-dragon-eye-container",
        children=[
            html.Div(
                "",
                id="golden-dragon-eye",
                style={
                    "width": "75px",
                    "height": "75px",
                    "border-radius": "50%",
                    "background": "radial-gradient(circle, gold, orange, darkgoldenrod)",
                    "box-shadow": "0px 0px 20px 5px rgba(255, 215, 0, 0.8)",
                    "text-align": "center",
                    "font-size": "40px",
                    "line-height": "75px",
                    "cursor": "grab",
                    "position": "absolute",
                    "top": "50px",
                    "left": "50px",
                },
            )
        ],
    )

app.layout = html.Div([
    html.Div(glowing_golden_eye(), id="golden-eye-wrapper", style={"position": "absolute", "top": "20px", "right": "20px"}),

    html.Div([
        html.H2("AI System Status", style={'textAlign': 'center'}),
        html.Div(id="ai-status", style={'textAlign': 'center', 'color': '#FFD700'}),
    
    html.Div([
    html.Button("Start Dreambox", id="start-dreambox-btn"),
    html.Button("Stop Dreambox", id="stop-dreambox-btn", style={"marginLeft": "10px"}),
    html.Div(id="dreambox-status")
], style={"textAlign": "center", "marginTop": "30px"}),

    html.Div([
        dcc.Input(id="user-command", type="text", placeholder="Enter command..."),
        html.Button("Execute Command", id="execute-button"),
        html.Div(id="command-output"),
    ], style={"textAlign": "center", "marginTop": "20px"}),

    html.Div([
        html.Button("Run Security Scan", id="security-button"),
        html.Div(id="security-output"),
    ], style={"textAlign": "center", "marginTop": "20px"}),

    html.Div([
        html.Button("Check Network Status", id="network-button"),
        html.Div(id="network-output"),
    ], style={"textAlign": "center", "marginTop": "20px"}),

    html.Div([
        html.Button("Run Quantum AI", id="quantum-button"),
        html.Div(id="quantum-output"),
    ], style={"textAlign": "center", "marginTop": "20px"}),

    html.Div([
        html.Button("Fetch System Logs", id="logs-button"),
        html.Div(id="logs-output"),
    ], style={"textAlign": "center", "marginTop": "20px"}),

# Callbacks

@app.callback(
    Output("command-output", "children"),
    [Input("execute-button", "n_clicks")],
    [State("user-command", "value")]
)
def execute_ai_command(n_clicks, command):
    if n_clicks and command:
        model_response = ask_model(f"Instruction: {command}")

        for name in tool_registry:
            if name in command.lower():
                result = tool_registry[name]({"command": command})
                return f"Model: {model_response}\n\nTool Result: {result}"

        return f"Model: {model_response}"
    return "Awaiting AI Command..."

@app.callback(Output("security-output", "children"), [Input("security-button", "n_clicks")])
def run_security_scan(n_clicks):
    if n_clicks:
        return ultimate_dashboard.call_api(SECURITY_API)
    return "Press button to scan security."

@app.callback(Output("network-output", "children"), [Input("network-button", "n_clicks")])
def check_network(n_clicks):
    if n_clicks:
        return ultimate_dashboard.call_api(NETWORK_API)
    return "Press button to check network."

@app.callback(Output("quantum-output", "children"), [Input("quantum-button", "n_clicks")])
def execute_quantum_ai(n_clicks):
    if n_clicks:
        return ultimate_dashboard.call_api(QUANTUM_API)
    return "Press button to run Quantum AI."

@app.callback(Output("logs-output", "children"), [Input("logs-button", "n_clicks")])
def fetch_logs(n_clicks):
    if n_clicks:
        return ultimate_dashboard.call_api(LOGS_API)
    return "Press button to fetch logs."

@app.callback(Output("dreambox-status", "children"),
              [Input("start-dreambox-btn", "n_clicks"),
               Input("stop-dreambox-btn", "n_clicks")])
def toggle_dreambox(start, stop):
    changed = dash.callback_context.triggered_id
    if changed == "start-dreambox-btn":
        return start_dreambox()
    elif changed == "stop-dreambox-btn":
        return stop_dreambox()
    return "Dreambox idle."

# Launch
if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
