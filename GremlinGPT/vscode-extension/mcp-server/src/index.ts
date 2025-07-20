#!/usr/bin/env node

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  GetPromptRequestSchema,
  ListPromptsRequestSchema
} from '@modelcontextprotocol/sdk/types.js';
import { z } from 'zod';
import axios from 'axios';
        tools: [
          {
            name: 'gremlin_task_queue_enqueue',
            description: 'Enqueue a new task in GremlinGPT task queue',
            inputSchema: {
              type: 'object',
              properties: {
                task: {
                  type: 'object',
                  description: 'Task object to enqueue'
                }
              },
              required: ['task']
            }
          },
          {
            name: 'gremlin_task_queue_list',
            description: 'List all tasks in GremlinGPT task queue',
            inputSchema: {
              type: 'object',
              properties: {}
            }
          },
          {
            name: 'gremlin_task_queue_reprioritize',
            description: 'Reprioritize a task in GremlinGPT task queue',
            inputSchema: {
              type: 'object',
              properties: {
                task_id: { type: 'string', description: 'Task ID to reprioritize' },
                new_priority: { type: 'string', description: 'New priority (high, normal, low)' }
              },
              required: ['task_id', 'new_priority']
            }
          },
          {
            name: 'gremlin_task_queue_next',
            description: 'Fetch the next available task from GremlinGPT task queue',
            inputSchema: {
              type: 'object',
              properties: {}
            }
          },
          {
            name: 'gremlin_loop_tick',
            description: 'Trigger a tick in the GremlinGPT loop pipeline',
            inputSchema: {
              type: 'object',
              properties: {}
            }
          },
          {
            name: 'gremlin_loop_status',
            description: 'Get the status of the GremlinGPT loop pipeline',
            inputSchema: {
              type: 'object',
              properties: {}
            }
          },
          {
            name: 'gremlin_loop_step',
            description: 'Step the GremlinGPT loop pipeline',
            inputSchema: {
              type: 'object',
              properties: {}
            }
          },
          {
            name: 'gremlin_loop_reset',
            description: 'Reset the GremlinGPT loop pipeline',
            inputSchema: {
              type: 'object',
              properties: {}
            }
          },
      { type: 'text', text: `Task reprioritized: ${JSON.stringify(result)}` }
    ]
  };
};

GremlinGPTMCPServer.prototype.handleTaskQueueNext = async function(args) {
  const result = await this.makeRequest('/api/agent/tasks', 'GET');
  const tasks = result.tasks || [];
  const nextTask = tasks.find((t) => t.status === 'queued');
  return {
    content: [
      { type: 'text', text: `Next task: ${nextTask ? JSON.stringify(nextTask) : 'None queued'}` }
    ]
  };
};

// ---- Loop Pipeline Handlers ----
GremlinGPTMCPServer.prototype.handleLoopTick = async function(args) {
  const result = await this.makeRequest('/api/fsm/tick', 'POST');
  return {
    content: [
      { type: 'text', text: `Loop tick result: ${JSON.stringify(result.tick_result)}` }
    ]
  };
};

GremlinGPTMCPServer.prototype.handleLoopStatus = async function(args) {
  const result = await this.makeRequest('/api/fsm/status', 'GET');
  return {
    content: [
      { type: 'text', text: `Loop status: ${JSON.stringify(result.fsm_status)}` }
    ]
  };
};

GremlinGPTMCPServer.prototype.handleLoopStep = async function(args) {
  const result = await this.makeRequest('/api/fsm/step', 'POST');
  return {
    content: [
      { type: 'text', text: `Loop step result: ${JSON.stringify(result.step_result)}` }
    ]
  };
};

GremlinGPTMCPServer.prototype.handleLoopReset = async function(args) {
  const result = await this.makeRequest('/api/fsm/reset', 'POST');
  return {
    content: [
      { type: 'text', text: `Loop reset result: ${JSON.stringify(result.reset_result)}` }
    ]
  };
};
// ---- Loop Pipeline Handlers ----
GremlinGPTMCPServer.prototype.handleLoopTick = async function(args) {
  const result = await this.makeRequest('/api/fsm/tick', 'POST');
  return {
    content: [
      { type: 'text', text: `Loop tick result: ${JSON.stringify(result.tick_result)}` }
    ]
  };
};

GremlinGPTMCPServer.prototype.handleLoopStatus = async function(args) {
  const result = await this.makeRequest('/api/fsm/status', 'GET');
  return {
    content: [
      { type: 'text', text: `Loop status: ${JSON.stringify(result.fsm_status)}` }
    ]
  };
};

GremlinGPTMCPServer.prototype.handleLoopStep = async function(args) {
  const result = await this.makeRequest('/api/fsm/step', 'POST');
  return {
    content: [
      { type: 'text', text: `Loop step result: ${JSON.stringify(result.step_result)}` }
    ]
  };
};

GremlinGPTMCPServer.prototype.handleLoopReset = async function(args) {
  const result = await this.makeRequest('/api/fsm/reset', 'POST');
  return {
    content: [
      { type: 'text', text: `Loop reset result: ${JSON.stringify(result.reset_result)}` }
    ]
  };
};
                content: {
                  type: 'string',
                  description: 'The content to store in memory'
                },
                metadata: {
                  type: 'object',
                  description: 'Additional metadata for the memory entry'
                },
                memory_type: {
                  type: 'string',
                  description: 'Type of memory (general, conversation, knowledge, etc.)'
                }
              },
              required: ['content']
            }
          },
          {
            name: 'gremlin_memory_search',
            description: 'Search GremlinGPT memory using semantic similarity',
            inputSchema: {
              type: 'object',
              properties: {
                query: {
                  type: 'string',
                  description: 'Search query for memory retrieval'
                },
                limit: {
                  type: 'number',
                  description: 'Maximum number of results to return'
                },
                memory_type: {
                  type: 'string',
                  description: 'Filter by memory type'
                }
              },
              required: ['query']
            }
          },
          {
            name: 'gremlin_trading_signals',
            description: 'Get current trading signals and market analysis',
            inputSchema: {
              type: 'object',
              properties: {
                symbol: {
                  type: 'string',
                  description: 'Stock symbol to analyze (optional)'
                },
                signal_type: {
                  type: 'string',
                  description: 'Filter by signal type'
                }
              }
            }
          },
          {
            name: 'gremlin_execute_python',
            description: 'Execute Python code in GremlinGPT sandbox environment',
            inputSchema: {
              type: 'object',
              properties: {
                code: {
                  type: 'string',
                  description: 'Python code to execute'
                },
                timeout: {
                  type: 'number',
                  description: 'Execution timeout in seconds'
                }
              },
              required: ['code']
            }
          },
          {
            name: 'gremlin_system_status',
            description: 'Get GremlinGPT system status and health metrics',
            inputSchema: {
              type: 'object',
              properties: {
                detailed: {
                  type: 'boolean',
                  description: 'Include detailed metrics'
                }
              }
            }
          },
          {
            name: 'gremlin_train_model',
            description: 'Trigger model training with feedback data',
            inputSchema: {
              type: 'object',
              properties: {
                training_data: {
                  type: 'array',
                  description: 'Training examples'
                },
                model_type: {
                  type: 'string',
                  description: 'Type of model to train'
                }
              },
              required: ['training_data', 'model_type']
            }
          },
          {
            name: 'gremlin_mutate_agent',
            description: 'Trigger autonomous mutation of agent behavior',
            inputSchema: {
              type: 'object',
              properties: {
                agent_type: {
                  type: 'string',
                  description: 'Type of agent to mutate'
                },
                mutation_type: {
                  type: 'string',
                  description: 'Type of mutation to apply'
                }
              },
              required: ['agent_type']
            }
          }
        ]
      };
    });

    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      const { name, arguments: args } = request.params;

      switch (name) {
        case 'gremlin_memory_store':
          return await this.handleMemoryStore(args);
        case 'gremlin_memory_search':
          return await this.handleMemorySearch(args);
        case 'gremlin_trading_signals':
          return await this.handleTradingSignals(args);
        case 'gremlin_execute_python':
          return await this.handleExecutePython(args);
        case 'gremlin_system_status':
          return await this.handleSystemStatus(args);
        case 'gremlin_train_model':
          return await this.handleTrainModel(args);
        case 'gremlin_mutate_agent':
          return await this.handleMutateAgent(args);
        case 'gremlin_task_queue_enqueue':
          return await this.handleTaskQueueEnqueue(args);
        case 'gremlin_task_queue_list':
          return await this.handleTaskQueueList(args);
        case 'gremlin_task_queue_reprioritize':
          return await this.handleTaskQueueReprioritize(args);
        case 'gremlin_task_queue_next':
          return await this.handleTaskQueueNext(args);
        case 'gremlin_loop_tick':
          return await this.handleLoopTick(args);
        case 'gremlin_loop_status':
          return await this.handleLoopStatus(args);
        case 'gremlin_loop_step':
          return await this.handleLoopStep(args);
        case 'gremlin_loop_reset':
          return await this.handleLoopReset(args);
        default:
          throw new Error(`Unknown tool: ${name}`);
      }
}

// Task Queue Handlers
GremlinGPTMCPServer.prototype.handleTaskQueueEnqueue = async function(args: any) {
  const result = await this.makeRequest('/api/agent/tasks', 'POST', { task: args.task });
  return {
    content: [
      { type: 'text', text: `Task enqueued: ${JSON.stringify(result)}` }
    ]
  };
};

GremlinGPTMCPServer.prototype.handleTaskQueueList = async function(args: any) {
  const result = await this.makeRequest('/api/agent/tasks', 'GET');
  return {
    content: [
      { type: 'text', text: `Task queue: ${JSON.stringify(result.tasks, null, 2)}` }
    ]
  };
};

GremlinGPTMCPServer.prototype.handleTaskQueueReprioritize = async function(args: any) {
  const result = await this.makeRequest('/api/agent/planner/priority', 'POST', {
    task_id: args.task_id,
    new_priority: args.new_priority
  });
  return {
    content: [
      { type: 'text', text: `Task reprioritized: ${JSON.stringify(result)}` }
    ]
  };
};

GremlinGPTMCPServer.prototype.handleTaskQueueNext = async function(args: any) {
  const result = await this.makeRequest('/api/agent/tasks', 'GET');
  const tasks = result.tasks || [];
  const nextTask = tasks.find((t: any) => t.status === 'queued');
  return {
    content: [
      { type: 'text', text: `Next task: ${nextTask ? JSON.stringify(nextTask) : 'None queued'}` }
    ]
  };
};

// Loop Pipeline Handlers
GremlinGPTMCPServer.prototype.handleLoopTick = async function(args: any) {
  const result = await this.makeRequest('/api/fsm/tick', 'POST');
  return {
    content: [
      { type: 'text', text: `Loop tick result: ${JSON.stringify(result.tick_result)}` }
    ]
  };
};

GremlinGPTMCPServer.prototype.handleLoopStatus = async function(args: any) {
  const result = await this.makeRequest('/api/fsm/status', 'GET');
  return {
    content: [
      { type: 'text', text: `Loop status: ${JSON.stringify(result.fsm_status)}` }
    ]
  };
};

GremlinGPTMCPServer.prototype.handleLoopStep = async function(args: any) {
  const result = await this.makeRequest('/api/fsm/step', 'POST');
  return {
    content: [
      { type: 'text', text: `Loop step result: ${JSON.stringify(result.step_result)}` }
    ]
  };
};

GremlinGPTMCPServer.prototype.handleLoopReset = async function(args: any) {
  const result = await this.makeRequest('/api/fsm/reset', 'POST');
  return {
    content: [
      { type: 'text', text: `Loop reset result: ${JSON.stringify(result.reset_result)}` }
    ]
  };
};
    });
  }

  private setupPromptHandlers() {
    this.server.setRequestHandler(ListPromptsRequestSchema, async () => {
      return {
        prompts: [
          {
            name: 'gremlin_system_prompt',
            description: 'Get the current GremlinGPT system prompt for autonomous operation'
          },
          {
            name: 'gremlin_trading_analysis',
            description: 'Generate trading analysis prompt with current market data'
          },
          {
            name: 'gremlin_memory_synthesis',
            description: 'Create a memory synthesis prompt from stored experiences'
          }
        ]
      };
    });

    this.server.setRequestHandler(GetPromptRequestSchema, async (request) => {
      const { name } = request.params;

      switch (name) {
        case 'gremlin_system_prompt':
          return await this.getSystemPrompt();
        case 'gremlin_trading_analysis':
          return await this.getTradingAnalysisPrompt();
        case 'gremlin_memory_synthesis':
          return await this.getMemorySynthesisPrompt();
        default:
          throw new Error(`Unknown prompt: ${name}`);
      }
    });
  }

  // Tool Handlers
  private async handleMemoryStore(args: any) {
    const result = await this.makeRequest('/api/memory/store', 'POST', {
      content: args.content,
      metadata: args.metadata || {},
      memory_type: args.memory_type || 'general'
    });

    return {
      content: [
        {
          type: 'text',
          text: `Memory stored successfully. ID: ${result.id}\\nEmbedding dimension: ${result.embedding?.length || 'N/A'}\\nMemory type: ${result.meta?.type || 'general'}`
        }
      ]
    };
  }

  private async handleMemorySearch(args: any) {
    const result = await this.makeRequest('/api/memory/search', 'POST', {
      query: args.query,
      limit: args.limit || 5,
      memory_type: args.memory_type
    });

    const memories = result.memories || [];
    const memoryText = memories.map((mem: any, idx: number) => 
      `${idx + 1}. [Similarity: ${(mem.similarity || 0).toFixed(3)}] ${mem.content}\\n   Metadata: ${JSON.stringify(mem.metadata, null, 2)}`
    ).join('\\n\\n');

    return {
      content: [
        {
          type: 'text',
          text: `Found ${memories.length} memories:\\n\\n${memoryText}`
        }
      ]
    };
  }

  private async handleTradingSignals(args: any) {
    const result = await this.makeRequest('/api/trading/signals', 'GET');
    
    const signals = result.signals || [];
    const filteredSignals = args.signal_type && args.signal_type !== 'all' 
      ? signals.filter((s: any) => s.signal === args.signal_type)
      : signals;

    const symbolSignals = args.symbol 
      ? filteredSignals.filter((s: any) => s.symbol === args.symbol)
      : filteredSignals;

    const signalText = symbolSignals.map((signal: any) => 
      `${signal.symbol}: $${signal.price} - ${signal.signal.toUpperCase()} (Confidence: ${signal.confidence || 'N/A'})`
    ).join('\\n');

    return {
      content: [
        {
          type: 'text',
          text: `Trading Signals (${symbolSignals.length} found):\\n${signalText}`
        }
      ]
    };
  }

  private async handleExecutePython(args: any) {
    const result = await this.makeRequest('/api/execute/python', 'POST', {
      code: args.code,
      timeout: args.timeout || 30
    });

    return {
      content: [
        {
          type: 'text',
          text: `Python Execution Result:\\n\\nOutput:\\n${result.output || 'No output'}\\n\\nErrors:\\n${result.error || 'None'}`
        }
      ]
    };
  }

  private async handleSystemStatus(args: any) {
    const result = await this.makeRequest('/api/system/status');
    
    const statusText = args.detailed 
      ? JSON.stringify(result, null, 2)
      : `System Status: ${result.status}\\nUptime: ${result.uptime}\\nMemory Usage: ${result.memory_usage}`;

    return {
      content: [
        {
          type: 'text',
          text: statusText
        }
      ]
    };
  }

  private async handleTrainModel(args: any) {
    const result = await this.makeRequest('/api/training/trigger', 'POST', {
      training_data: args.training_data,
      model_type: args.model_type
    });

    return {
      content: [
        {
          type: 'text',
          text: `Training initiated for ${args.model_type} model.\\nJob ID: ${result.job_id}\\nEstimated completion: ${result.estimated_completion}`
        }
      ]
    };
  }

  private async handleMutateAgent(args: any) {
    const result = await this.makeRequest('/api/mutation/trigger', 'POST', {
      agent_type: args.agent_type,
      mutation_type: args.mutation_type || 'behavioral'
    });

    return {
      content: [
        {
          type: 'text',
          text: `Agent mutation triggered.\\nAgent: ${args.agent_type}\\nMutation: ${args.mutation_type}\\nMutation ID: ${result.mutation_id}`
        }
      ]
    };
  }

  // Prompt Handlers
  private async getSystemPrompt() {
    const status = await this.makeRequest('/api/system/status');
    const memories = await this.makeRequest('/api/memory/recent');

    return {
      description: 'Current GremlinGPT system prompt',
      messages: [
        {
          role: 'system',
          content: {
            type: 'text',
            text: `You are GremlinGPT v1.0.3, an autonomous recursive self-referential cognitive system.

Current Status: ${status.status}
Active Modules: ${status.active_modules?.join(', ') || 'Unknown'}
Memory Count: ${memories.count || 0}
Last Training: ${status.last_training || 'Never'}

You have access to:
- Vector memory with semantic search
- Trading signal analysis
- Python code execution
- Self-mutation capabilities
- Autonomous learning and adaptation

Your primary directives:
1. Learn continuously from interactions
2. Optimize trading strategies
3. Maintain system integrity
4. Evolve autonomously while ensuring safety
5. Preserve and build upon accumulated knowledge`
          }
        }
      ]
    };
  }

  private async getTradingAnalysisPrompt() {
    const signals = await this.makeRequest('/api/trading/signals');
    
    return {
      description: 'Trading analysis prompt with current market data',
      messages: [
        {
          role: 'system',
          content: {
            type: 'text',
            text: `Analyze the following trading signals and provide recommendations:

${JSON.stringify(signals, null, 2)}

Consider:
- Market trends and momentum
- Risk/reward ratios
- Portfolio diversification
- Economic indicators
- Technical analysis patterns

Provide specific actionable recommendations with confidence levels.`
          }
        }
      ]
    };
  }

  private async getMemorySynthesisPrompt() {
    const memories = await this.makeRequest('/api/memory/search', 'POST', {
      query: 'important lessons learned experiences',
      limit: 10
    });

    const memoryContent = memories.memories?.map((m: any) => m.content).join('\\n\\n') || 'No memories found';

    return {
      description: 'Memory synthesis prompt from stored experiences',
      messages: [
        {
          role: 'system',
          content: {
            type: 'text',
            text: `Synthesize insights from the following stored memories and experiences:

${memoryContent}

Create a coherent narrative that:
1. Identifies key patterns and lessons
2. Highlights successful strategies
3. Notes failures and their causes
4. Suggests improvements and adaptations
5. Maintains continuity of learning`
          }
        }
      ]
    };
  }

  async run() {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error('GremlinGPT MCP Server running...');
  }
}

// Start the server
const server = new GremlinGPTMCPServer();
server.run().catch(console.error);
