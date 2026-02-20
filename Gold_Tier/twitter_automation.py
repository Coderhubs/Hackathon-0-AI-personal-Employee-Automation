#!/usr/bin/env python3
"""
Twitter/X Automation - Playwright-based
Executes approved Twitter actions
"""

import asyncio
import time
from pathlib import Path
from datetime import datetime
from playwright.async_api import async_playwright

class TwitterAutomation:
    """
    Executes approved Twitter actions using Playwright.

    Features:
    - Posts tweets
    - Posts threads
    - Replies to tweets
    - Rate limiting (max 10 tweets per hour)
    """

    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.approved_dir = self.base_dir / "AI_Employee_Vault" / "Approved"
        self.done_dir = self.base_dir / "AI_Employee_Vault" / "Done"
        self.user_data_dir = self.base_dir / "browser_data" / "twitter"

        # Rate limiting
        self.tweets_this_hour = []
        self.max_tweets_per_hour = 10

    def check_rate_limit(self) -> bool:
        """Check if we're within rate limits"""
        now = time.time()
        # Remove tweets older than 1 hour
        self.tweets_this_hour = [t for t in self.tweets_this_hour if now - t < 3600]

        if len(self.tweets_this_hour) >= self.max_tweets_per_hour:
            print(f"Rate limit reached: {len(self.tweets_this_hour)} tweets in last hour")
            return False
        return True

    async def post_tweet(self, text: str) -> bool:
        """Post a tweet to Twitter"""
        try:
            async with async_playwright() as p:
                context = await p.chromium.launch_persistent_context(
                    user_data_dir=str(self.user_data_dir),
                    headless=False,
                    viewport={'width': 1280, 'height': 720}
                )

                page = context.pages[0] if context.pages else await context.new_page()

                # Navigate to Twitter
                await page.goto('https://twitter.com/home', wait_until='networkidle')
                await asyncio.sleep(2)

                # Click on tweet compose box
                await page.click('[data-testid="tweetTextarea_0"]', timeout=10000)
                await asyncio.sleep(1)

                # Type the tweet
                await page.keyboard.type(text, delay=50)
                await asyncio.sleep(1)

                # Click Post button
                await page.click('[data-testid="tweetButtonInline"]', timeout=10000)
                await asyncio.sleep(3)

                print(f"✓ Posted tweet: {text[:50]}...")

                await context.close()

                # Update rate limit
                self.tweets_this_hour.append(time.time())

                return True

        except Exception as e:
            print(f"✗ Error posting tweet: {e}")
            return False

    async def reply_to_tweet(self, tweet_url: str, text: str) -> bool:
        """Reply to a tweet"""
        try:
            async with async_playwright() as p:
                context = await p.chromium.launch_persistent_context(
                    user_data_dir=str(self.user_data_dir),
                    headless=False,
                    viewport={'width': 1280, 'height': 720}
                )

                page = context.pages[0] if context.pages else await context.new_page()

                # Navigate to tweet
                await page.goto(tweet_url, wait_until='networkidle')
                await asyncio.sleep(2)

                # Click reply button
                await page.click('[data-testid="reply"]', timeout=10000)
                await asyncio.sleep(1)

                # Type reply
                await page.keyboard.type(text, delay=50)
                await asyncio.sleep(1)

                # Click Reply button
                await page.click('[data-testid="tweetButton"]', timeout=10000)
                await asyncio.sleep(3)

                print(f"✓ Posted reply: {text[:50]}...")

                await context.close()

                # Update rate limit
                self.tweets_this_hour.append(time.time())

                return True

        except Exception as e:
            print(f"✗ Error posting reply: {e}")
            return False

    async def send_dm(self, user: str, message: str) -> bool:
        """Send a direct message"""
        try:
            async with async_playwright() as p:
                context = await p.chromium.launch_persistent_context(
                    user_data_dir=str(self.user_data_dir),
                    headless=False,
                    viewport={'width': 1280, 'height': 720}
                )

                page = context.pages[0] if context.pages else await context.new_page()

                # Navigate to messages
                await page.goto('https://twitter.com/messages', wait_until='networkidle')
                await asyncio.sleep(2)

                # Click new message button
                await page.click('[data-testid="NewDM_Button"]', timeout=10000)
                await asyncio.sleep(1)

                # Search for user
                await page.keyboard.type(user, delay=50)
                await asyncio.sleep(2)

                # Click on first result
                await page.click('[data-testid="TypeaheadUser"]', timeout=10000)
                await asyncio.sleep(1)

                # Click Next
                await page.click('[data-testid="nextButton"]', timeout=10000)
                await asyncio.sleep(1)

                # Type message
                await page.keyboard.type(message, delay=50)
                await asyncio.sleep(1)

                # Send message
                await page.click('[data-testid="dmComposerSendButton"]', timeout=10000)
                await asyncio.sleep(2)

                print(f"✓ Sent DM to {user}: {message[:50]}...")

                await context.close()

                return True

        except Exception as e:
            print(f"✗ Error sending DM: {e}")
            return False

    def process_approved_files(self):
        """Process all approved Twitter files"""
        if not self.approved_dir.exists():
            print("Approved directory not found")
            return

        twitter_files = list(self.approved_dir.glob("TWITTER_*.md"))

        if not twitter_files:
            print("No approved Twitter actions found")
            return

        print(f"Found {len(twitter_files)} approved Twitter action(s)")

        for file in twitter_files:
            if not self.check_rate_limit():
                print("Rate limit reached. Waiting...")
                break

            print(f"\nProcessing: {file.name}")

            # Read file content
            content = file.read_text(encoding='utf-8')

            # Parse action type and content
            if 'post_tweet' in content.lower():
                # Extract text to tweet
                lines = content.split('\n')
                text = ""
                for line in lines:
                    if 'text:' in line.lower():
                        text = line.split(':', 1)[1].strip()
                        break

                if text:
                    # Post tweet
                    success = asyncio.run(self.post_tweet(text[:280]))  # Twitter limit

                    if success:
                        # Move to Done
                        done_file = self.done_dir / file.name
                        file.rename(done_file)
                        print(f"✓ Moved to Done: {file.name}")

            elif 'reply_to_tweet' in content.lower():
                # Extract tweet URL and reply text
                lines = content.split('\n')
                tweet_url = ""
                text = ""
                for line in lines:
                    if 'tweet_url:' in line.lower():
                        tweet_url = line.split(':', 1)[1].strip()
                    elif 'text:' in line.lower():
                        text = line.split(':', 1)[1].strip()

                if tweet_url and text:
                    # Post reply
                    success = asyncio.run(self.reply_to_tweet(tweet_url, text[:280]))

                    if success:
                        # Move to Done
                        done_file = self.done_dir / file.name
                        file.rename(done_file)
                        print(f"✓ Moved to Done: {file.name}")

            time.sleep(2)  # Delay between tweets

if __name__ == "__main__":
    automation = TwitterAutomation()
    automation.process_approved_files()
