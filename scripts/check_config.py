import sys
from config.config import config
from config.logger import logger

# Example script to check configuration and logging

def main():
    try:
        config.validate()
        logger.info("Configuration loaded successfully.")
        print("Book Recommender configuration is valid.")
    except Exception as e:
        logger.error(f"Configuration error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
