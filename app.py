from main import create_app
from main.utils.logger import logger

app = create_app()
app.app_context().push()

logger.info("App created!")

if __name__ == "__main__":
    logger.info("Starting server...")
    app.run(debug = True, host="0.0.0.0", port=5000)
