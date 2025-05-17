import logging
import traceback

# Configure logging
logging.basicConfig(
    filename='logs/gremlingpt.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s'
)

def log_exception(e):
    logging.error(f"Exception occurred: {e}")
    logging.error(traceback.format_exc())
