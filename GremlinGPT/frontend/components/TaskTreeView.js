// Initialize component logger
const logger = window.GremlinLogger ? window.GremlinLogger.createLogger('frontend', 'task-tree-view') : console;

export default function TaskTreeView(targetId) {
  logger.info('Initializing TaskTreeView component');
  
  const el = document.getElementById(targetId);
  el.innerHTML = `
    <div class="card bg-secondary">
      <div class="card-header">Task Tree</div>
      <div class="card-body" id="taskList">Loading...</div>
    </div>
  `;

  function fetchTasks() {
    logger.info('Fetching tasks');
    fetch("/api/agent/tasks")
      .then(res => res.json())
      .then(data => {
        logger.info('Tasks fetched successfully', data);
        const html = data.tasks.map(t => `<li>${t.type} - ${t.status}</li>`).join("");
        document.getElementById("taskList").innerHTML = `<ul>${html}</ul>`;
      })
      .catch(error => {
        logger.error('Error fetching tasks', error);
      });
  }

  fetchTasks();
  setInterval(fetchTasks, 5000);
}

