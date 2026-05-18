import logging
from waitress import serve
from app import app

# Set up clean production logging format
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("WaitressProduction")

if __name__ == "__main__":
    port = 5000
    logger.info(f"Initializing industrial-grade WSGI production engine on port {port}...")
    logger.info(f"Gateway live. Direct multi-user trial traffic to: http://127.0.0.1:{port}")
    
    # Serve the Flask application using multiple background execution threads
    serve(app, host="0.0.0.0", port=port, threads=6)