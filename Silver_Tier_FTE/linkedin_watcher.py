import os
import time
import random
from datetime import datetime

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

def main():
    """Main function to run the LinkedIn watcher."""
    print("Starting LinkedIn Watcher...")
    print("Creating a new LinkedIn trend file every 2 minutes.")
    
    while True:
        try:
            create_linkedin_trend_file()
            time.sleep(120)  # Wait for 2 minutes (120 seconds)
        except KeyboardInterrupt:
            print("\nLinkedIn Watcher stopped.")
            break
        except Exception as e:
            print(f"Error in LinkedIn Watcher: {e}")
            time.sleep(120)  # Wait before retrying

if __name__ == "__main__":
    main()