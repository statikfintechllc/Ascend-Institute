// Initialize component logger
const logger = window.GremlinLogger ? window.GremlinLogger.createLogger('frontend', 'memory-graph') : console;

export default function MemoryGraph(targetId) {
  logger.info('Initializing MemoryGraph component');
  
  const el = document.getElementById(targetId);
  el.innerHTML = `
    <div class="card bg-secondary">
      <div class="card-header">Vector Memory</div>
      <div class="card-body" id="memoryGraph">Loading...</div>
    </div>
  `;

  fetch("/api/memory/graph")
    .then(res => res.json())
    .then(data => {
      document.getElementById("memoryGraph").innerText = JSON.stringify(data, null, 2);
    });
}

