import logging

# Configure the logger
logging.basicConfig(
    level=logging.INFO,  #can be INFO or DEBUG
    format='%(asctime)s | %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

# Get the logger
logger = logging.getLogger("AppLogger")
