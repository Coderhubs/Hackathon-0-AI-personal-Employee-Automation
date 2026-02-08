import os
import time
import random
from datetime import datetime
from pathlib import Path
import logging

def get_random_tech_headline():
    """Generate a random tech headline."""
    headlines = [
        "AI is taking over",
        "New Python release",
        "Machine Learning breakthrough",
        "Quantum computing advances",
        "Blockchain revolution",
        "Cloud computing trends",
        "Cybersecurity threats evolve",
        "Remote work technologies",
        "Data science innovations",
        "Web development frameworks",
        "Mobile app trends",
        "IoT devices growth",
        "Tech startup funding",
        "Digital transformation",
        "Software engineering best practices"
    ]
    return random.choice(headlines)

def create_linkedin_trend_file():
    """Create a file in Inbox with a random tech headline."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"LINKEDIN_trend_{timestamp}.txt"
    filepath = os.path.join("Inbox", filename)
    
    headline = get_random_tech_headline()
    
    with open(filepath, 'w') as f:
        f.write(headline)
    
    print(f"Created LinkedIn trend file: {filepath}")

def setup_logging():
    """Setup logging to file"""
    log_dir = Path("Gold_Tier/Logs")
    log_dir.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / 'linkedin_watcher.log'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger('LinkedInWatcher')

def main():
    """Main function to run the LinkedIn watcher with error recovery."""
    logger = setup_logging()
    logger.info("Starting LinkedIn Watcher with error recovery...")
    logger.info("Creating a new LinkedIn trend file every 2 minutes.")

    retry_count = 0
    max_retries = 5
    base_delay = 1  # Start with 1 second

    while True:
        try:
            create_linkedin_trend_file()
            retry_count = 0  # Reset on success
            time.sleep(120)  # Wait for 2 minutes (120 seconds)
        except KeyboardInterrupt:
            logger.info("LinkedIn Watcher stopped by user.")
            break
        except Exception as e:
            retry_count += 1
            logger.error(f"Error in LinkedIn Watcher: {e}")

            if retry_count <= max_retries:
                # Exponential backoff: 1, 2, 4, 8, 16 seconds
                delay = base_delay * (2 ** (retry_count - 1))
                logger.warning(f"Retry {retry_count}/{max_retries} in {delay} seconds...")
                time.sleep(delay)
            else:
                logger.critical(f"Max retries ({max_retries}) reached. Waiting 120 seconds before reset...")
                time.sleep(120)
                retry_count = 0  # Reset retry counter

if __name__ == "__main__":
    main()