import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';
import { spawn, ChildProcess } from 'child_process';
import axios from 'axios';
import WebSocket from 'ws';

interface GremlinConfig {
    serverPort: number;
    memoryBackend: 'faiss' | 'chromadb';
    debugMode: boolean;
    autoStart: boolean;
}

class GremlinGPTManager {
    private serverProcess: ChildProcess | null = null;
    private statusBarItem: vscode.StatusBarItem;
    private outputChannel: vscode.OutputChannel;
    private websocket: WebSocket | null = null;
    private config: GremlinConfig;

    constructor(private context: vscode.ExtensionContext) {
        this.statusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 100);
        this.outputChannel = vscode.window.createOutputChannel('GremlinGPT');
        this.config = this.loadConfig();
        this.updateStatusBar('stopped');
    }

    private loadConfig(): GremlinConfig {
        const config = vscode.workspace.getConfiguration('gremlingpt');
        return {
            serverPort: config.get('serverPort', 7777),
            memoryBackend: config.get('memoryBackend', 'faiss'),
            debugMode: config.get('debugMode', false),
            autoStart: config.get('autoStart', false)
        };
    }

    private updateStatusBar(status: 'starting' | 'running' | 'stopped' | 'error') {
        const statusMap = {
            starting: { text: '$(loading~spin) GremlinGPT Starting...', color: 'yellow' },
            running: { text: '$(check) GremlinGPT Running', color: 'green' },
            stopped: { text: '$(circle-slash) GremlinGPT Stopped', color: 'red' },
            error: { text: '$(error) GremlinGPT Error', color: 'red' }
        };

        const statusInfo = statusMap[status];
        this.statusBarItem.text = statusInfo.text;
        this.statusBarItem.color = statusInfo.color;
        this.statusBarItem.command = status === 'running' ? 'gremlingpt.dashboard' : 'gremlingpt.start';
        this.statusBarItem.show();
    }

    private log(message: string, level: 'info' | 'warn' | 'error' = 'info') {
        const timestamp = new Date().toISOString();
        const logMessage = `[${timestamp}] ${message}`;
        
        this.outputChannel.appendLine(logMessage);
        
        if (this.config.debugMode) {
            console.log(`[GremlinGPT] ${logMessage}`);
        }

        if (level === 'error') {
            vscode.window.showErrorMessage(`GremlinGPT: ${message}`);
        } else if (level === 'warn') {
            vscode.window.showWarningMessage(`GremlinGPT: ${message}`);
        }
    }

    private getGremlinPath(): string {
        // Try to find GremlinGPT in the workspace
        const workspaceFolders = vscode.workspace.workspaceFolders;
        if (workspaceFolders) {
            for (const folder of workspaceFolders) {
                const gremlinPath = path.join(folder.uri.fsPath, 'GremlinGPT');
                if (fs.existsSync(gremlinPath)) {
                    return gremlinPath;
                }
            }
        }

        // Fallback to extension context
        return path.join(this.context.extensionPath, '..', '..', 'GremlinGPT');
    }

    private async validateCondaEnvironments(): Promise<void> {
        this.log('Validating conda environments...');
        
        const requiredEnvs = [
            'gremlin-orchestrator', 
            'gremlin-dashboard', 
            'gremlin-memory', 
            'gremlin-nlp', 
            'gremlin-scraper'
        ];
        
        try {
            // Check if conda is available and environments exist
            const { spawn } = require('child_process');
            const condaList = spawn('/bin/bash', ['-c', 'source $HOME/miniconda3/etc/profile.d/conda.sh && conda env list'], {
                stdio: 'pipe'
            });
            
            let output = '';
            condaList.stdout.on('data', (data: Buffer) => {
                output += data.toString();
            });
            
            await new Promise((resolve) => {
                condaList.on('close', resolve);
            });
            
            const missingEnvs = requiredEnvs.filter(env => !output.includes(env));
            
            if (missingEnvs.length > 0) {
                const message = `Missing conda environments: ${missingEnvs.join(', ')}. Run './conda_envs/create_envs.sh' to create them.`;
                this.log(message, 'warn');
                vscode.window.showWarningMessage(message);
            } else {
                this.log('All required conda environments found');
            }
            
        } catch (error) {
            this.log(`Could not validate conda environments: ${error}`, 'warn');
        }
    }

    private buildCondaCommand(): string {
        // Build the complete command to activate conda and start GremlinGPT
        const condaProfile = '$HOME/miniconda3/etc/profile.d/conda.sh';
        const anacondaProfile = '$HOME/anaconda3/etc/profile.d/conda.sh';
        
        return `
            # Try to source conda profile
            if [ -f "${condaProfile}" ]; then
                source "${condaProfile}"
            elif [ -f "${anacondaProfile}" ]; then
                source "${anacondaProfile}"
            else
                echo "ERROR: Conda not found"
                exit 1
            fi
            
            # Activate the orchestrator environment and start unified system
            conda activate gremlin-orchestrator && python3 run/unified_startup.py
        `.trim();
    }

    async startGremlin(): Promise<void> {
        if (this.serverProcess) {
            this.log('GremlinGPT is already running');
            return;
        }

        this.updateStatusBar('starting');
        this.log('Starting GremlinGPT system...');

        try {
            const gremlinPath = this.getGremlinPath();
            
            if (!fs.existsSync(gremlinPath)) {
                throw new Error(`GremlinGPT directory not found at: ${gremlinPath}`);
            }

            // Check if conda environments exist
            await this.validateCondaEnvironments();

            // Create the conda activation command for the unified system
            const condaCommand = this.buildCondaCommand();
            
            this.log(`Executing command: ${condaCommand}`);
            
            this.serverProcess = spawn('/bin/bash', ['-c', condaCommand], {
                cwd: gremlinPath,
                env: {
                    ...process.env,
                    PYTHONPATH: gremlinPath,
                    GREMLIN_PORT: this.config.serverPort.toString(),
                    GREMLIN_BACKEND: this.config.memoryBackend,
                    PATH: process.env.PATH || ''
                }
            });

            this.serverProcess.stdout?.on('data', (data) => {
                this.log(`STDOUT: ${data.toString()}`);
            });

            this.serverProcess.stderr?.on('data', (data) => {
                this.log(`STDERR: ${data.toString()}`, 'warn');
            });

            this.serverProcess.on('close', (code) => {
                this.log(`GremlinGPT process exited with code ${code}`);
                this.serverProcess = null;
                this.updateStatusBar('stopped');
                this.disconnectWebSocket();
            });

            this.serverProcess.on('error', (error) => {
                this.log(`Failed to start GremlinGPT: ${error.message}`, 'error');
                this.updateStatusBar('error');
                this.serverProcess = null;
            });

            // Wait for server to be ready
            await this.waitForServer();
            this.updateStatusBar('running');
            this.connectWebSocket();
            
            // Start additional servers
            await this.startAdditionalServers();
            
            this.log('GremlinGPT started successfully');

        } catch (error) {
            this.log(`Error starting GremlinGPT: ${error}`, 'error');
            this.updateStatusBar('error');
            throw error;
        }
    }

    private async startAdditionalServers(): Promise<void> {
        this.log('Starting additional GremlinGPT servers...');
        
        // Start backend server in gremlin-dashboard environment
        const backendCommand = `
            if [ -f "$HOME/miniconda3/etc/profile.d/conda.sh" ]; then
                source "$HOME/miniconda3/etc/profile.d/conda.sh"
            elif [ -f "$HOME/anaconda3/etc/profile.d/conda.sh" ]; then
                source "$HOME/anaconda3/etc/profile.d/conda.sh"
            fi
            conda activate gremlin-dashboard && python3 -m backend.server
        `.trim();
        
        const gremlinPath = this.getGremlinPath();
        
        spawn('/bin/bash', ['-c', backendCommand], {
            cwd: gremlinPath,
            env: {
                ...process.env,
                PYTHONPATH: gremlinPath,
                GREMLIN_PORT: (this.config.serverPort + 1).toString()
            },
            detached: true
        });
        
        this.log('Backend server started');
        
        // Start MCP server if available
        try {
            spawn('gremlingpt-mcp', [], {
                detached: true,
                stdio: 'ignore'
            });
            this.log('MCP server started');
        } catch (error) {
            this.log('MCP server not available or failed to start', 'warn');
        }
    }

    private async waitForServer(maxAttempts: number = 30): Promise<void> {
        for (let i = 0; i < maxAttempts; i++) {
            try {
                await axios.get(`http://localhost:${this.config.serverPort}/api/health`);
                return;
            } catch (error) {
                await new Promise(resolve => setTimeout(resolve, 1000));
            }
        }
        throw new Error('Server failed to start within timeout period');
    }

    private connectWebSocket(): void {
        try {
            this.websocket = new WebSocket(`ws://localhost:${this.config.serverPort}/ws`);
            
            this.websocket.on('open', () => {
                this.log('WebSocket connected to GremlinGPT');
            });

            this.websocket.on('message', (data: any) => {
                try {
                    const message = JSON.parse(data.toString());
                    this.handleWebSocketMessage(message);
                } catch (error) {
                    this.log(`WebSocket message parse error: ${error}`, 'warn');
                }
            });

            this.websocket.on('error', (error: any) => {
                this.log(`WebSocket error: ${error}`, 'warn');
            });

            this.websocket.on('close', () => {
                this.log('WebSocket disconnected');
                this.websocket = null;
            });

        } catch (error) {
            this.log(`Failed to connect WebSocket: ${error}`, 'warn');
        }
    }

    private disconnectWebSocket(): void {
        if (this.websocket) {
            this.websocket.close();
            this.websocket = null;
        }
    }

    private handleWebSocketMessage(message: any): void {
        // Handle real-time updates from GremlinGPT
        switch (message.type) {
            case 'status_update':
                this.log(`Status: ${message.data.status}`);
                break;
            case 'memory_update':
                this.log(`Memory: ${message.data.description}`);
                break;
            case 'trading_signal':
                this.log(`Trading: ${message.data.symbol} - ${message.data.signal}`);
                break;
            case 'error':
                this.log(`System Error: ${message.data.message}`, 'error');
                break;
        }
    }

    async stopGremlin(): Promise<void> {
        if (!this.serverProcess) {
            this.log('GremlinGPT is not running');
            return;
        }

        this.log('Stopping GremlinGPT system...');
        this.disconnectWebSocket();

        try {
            // Try graceful shutdown first
            await axios.post(`http://localhost:${this.config.serverPort}/api/shutdown`);
            await new Promise(resolve => setTimeout(resolve, 2000));
        } catch (error) {
            this.log('Graceful shutdown failed, forcing termination', 'warn');
        }

        // Kill the main process
        if (this.serverProcess) {
            this.serverProcess.kill('SIGTERM');
            setTimeout(() => {
                if (this.serverProcess && !this.serverProcess.killed) {
                    this.serverProcess.kill('SIGKILL');
                }
            }, 5000);
        }

        // Stop all GremlinGPT related processes
        await this.stopAllGremlinProcesses();

        this.serverProcess = null;
        this.updateStatusBar('stopped');
        this.log('GremlinGPT stopped');
    }

    private async stopAllGremlinProcesses(): Promise<void> {
        this.log('Stopping all GremlinGPT processes...');
        
        try {
            // Kill processes by name patterns
            const killCommands = [
                "pkill -f 'unified_startup.py'",
                "pkill -f 'backend.server'", 
                "pkill -f 'gremlingpt-mcp'",
                "pkill -f 'python.*gremlin'",
                "pkill -f 'conda.*gremlin'"
            ];
            
            for (const cmd of killCommands) {
                spawn('/bin/bash', ['-c', cmd], { stdio: 'ignore' });
            }
            
            this.log('Process cleanup completed');
            
        } catch (error) {
            this.log(`Error during process cleanup: ${error}`, 'warn');
        }
    }

    createDashboardWebview(): vscode.WebviewPanel {
        const panel = vscode.window.createWebviewPanel(
            'gremlingpt.dashboard',
            'GremlinGPT Dashboard',
            vscode.ViewColumn.One,
            {
                enableScripts: true,
                localResourceRoots: [
                    vscode.Uri.file(path.join(this.context.extensionPath, 'media')),
                    vscode.Uri.file(path.join(this.getGremlinPath(), 'frontend'))
                ]
            }
        );

        panel.webview.html = this.getDashboardHtml(panel.webview);
        
        // Handle messages from webview
        panel.webview.onDidReceiveMessage(async (message) => {
            await this.handleWebviewMessage(message);
        });

        return panel;
    }

    private getDashboardHtml(webview: vscode.Webview): string {
        const scriptUri = webview.asWebviewUri(
            vscode.Uri.file(path.join(this.getGremlinPath(), 'frontend', 'app.js'))
        );
        
        const styleUri = webview.asWebviewUri(
            vscode.Uri.file(path.join(this.context.extensionPath, 'media', 'dashboard.css'))
        );

        return `<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>GremlinGPT Dashboard</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
            <link href="${styleUri}" rel="stylesheet">
            <style>
                body { 
                    background: #1e1e1e; 
                    color: #d4d4d4; 
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                }
                .navbar { background: #2d2d30 !important; }
                .card { background: #252526; border: 1px solid #3e3e42; }
                .btn-primary { background: #0078d4; border-color: #0078d4; }
                .text-success { color: #4caf50 !important; }
                .text-danger { color: #f44336 !important; }
                .status-indicator {
                    display: inline-block;
                    width: 10px;
                    height: 10px;
                    border-radius: 50%;
                    margin-right: 8px;
                }
                .status-running { background-color: #4caf50; }
                .status-stopped { background-color: #f44336; }
                .status-starting { background-color: #ff9800; }
            </style>
        </head>
        <body>
            <div class="container-fluid">
                <nav class="navbar navbar-dark">
                    <div class="navbar-brand">
                        <span class="status-indicator status-${this.serverProcess ? 'running' : 'stopped'}"></span>
                        GremlinGPT Dashboard v1.0.3
                    </div>
                    <div class="navbar-nav">
                        <button class="btn btn-outline-light btn-sm" onclick="refreshStatus()">Refresh</button>
                    </div>
                </nav>

                <div class="row mt-3">
                    <div class="col-md-12">
                        <div class="card">
                            <div class="card-header">
                                <h5 class="mb-0">System Status</h5>
                            </div>
                            <div class="card-body" id="systemStatus">
                                <div class="row">
                                    <div class="col-md-3">
                                        <strong>Server:</strong> 
                                        <span class="text-${this.serverProcess ? 'success' : 'danger'}">
                                            ${this.serverProcess ? 'Running' : 'Stopped'}
                                        </span>
                                    </div>
                                    <div class="col-md-3">
                                        <strong>Port:</strong> ${this.config.serverPort}
                                    </div>
                                    <div class="col-md-3">
                                        <strong>Backend:</strong> ${this.config.memoryBackend}
                                    </div>
                                    <div class="col-md-3">
                                        <strong>WebSocket:</strong> 
                                        <span class="text-${this.websocket ? 'success' : 'danger'}">
                                            ${this.websocket ? 'Connected' : 'Disconnected'}
                                        </span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div id="gremlin-app-root"></div>
            </div>

            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
            <script>
                const vscode = acquireVsCodeApi();
                
                window.GremlinVSCode = {
                    postMessage: (message) => vscode.postMessage(message),
                    baseUrl: 'http://localhost:${this.config.serverPort}'
                };

                function refreshStatus() {
                    vscode.postMessage({ command: 'refresh_status' });
                }

                // Load GremlinGPT frontend app
                import('${scriptUri}').then(module => {
                    console.log('GremlinGPT frontend loaded');
                }).catch(error => {
                    console.error('Failed to load GremlinGPT frontend:', error);
                });
            </script>
        </body>
        </html>`;
    }

    private async handleWebviewMessage(message: any): Promise<void> {
        switch (message.command) {
            case 'refresh_status':
                // Refresh status logic
                break;
            case 'start_system':
                await this.startGremlin();
                break;
            case 'stop_system':
                await this.stopGremlin();
                break;
        }
    }

    dispose(): void {
        this.stopGremlin();
        this.statusBarItem.dispose();
        this.outputChannel.dispose();
    }
}

// Extension activation
export function activate(context: vscode.ExtensionContext) {
    console.log('GremlinGPT extension is now active!');

    const gremlinManager = new GremlinGPTManager(context);

    // Register commands
    const commands = [
        vscode.commands.registerCommand('gremlingpt.start', () => gremlinManager.startGremlin()),
        vscode.commands.registerCommand('gremlingpt.stop', () => gremlinManager.stopGremlin()),
        vscode.commands.registerCommand('gremlingpt.dashboard', () => gremlinManager.createDashboardWebview()),
        vscode.commands.registerCommand('gremlingpt.memory', () => {
            vscode.window.showInformationMessage('Memory management panel coming soon!');
        }),
        vscode.commands.registerCommand('gremlingpt.trading', () => {
            vscode.window.showInformationMessage('Trading panel coming soon!');
        }),
        vscode.commands.registerCommand('gremlingpt.terminal', () => {
            const terminal = vscode.window.createTerminal('GremlinGPT');
            terminal.sendText(`cd ${gremlinManager['getGremlinPath']()}`);
            terminal.sendText('python3 run/cli.py');
            terminal.show();
        })
    ];

    context.subscriptions.push(...commands, gremlinManager);

    // Auto-start if configured
    const config = vscode.workspace.getConfiguration('gremlingpt');
    if (config.get('autoStart', false)) {
        gremlinManager.startGremlin().catch(error => {
            console.error('Auto-start failed:', error);
        });
    }
}

export function deactivate() {
    console.log('GremlinGPT extension deactivated');
}
