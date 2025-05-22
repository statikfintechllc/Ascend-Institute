import ChatInterface from './components/ChatInterface.js';
import TaskTreeView from './components/TaskTreeView.js';
import MemoryGraph from './components/MemoryGraph.js';
import TradingPanel from './components/TradingPanel.js';

window.onload = function () {
  const root = document.getElementById('root');
  root.innerHTML = `
    <div class="container-fluid">
      <h1 class="my-3 text-center">GremlinGPT Control Hub</h1>
      <div class="row">
        <div class="col-md-4"><div id="chat"></div></div>
        <div class="col-md-4"><div id="tasks"></div></div>
        <div class="col-md-4"><div id="memory"></div></div>
      </div>
      <div class="mt-4" id="trading"></div>
    </div>
  `;

  ChatInterface("chat");
  TaskTreeView("tasks");
  MemoryGraph("memory");
  TradingPanel("trading");
};

