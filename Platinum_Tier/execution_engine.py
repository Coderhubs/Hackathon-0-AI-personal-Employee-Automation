"""
Execution Engine - LinkedIn and WhatsApp executors with persistent sessions
"""
import asyncio
import logging
from pathlib import Path
from playwright.async_api import async_playwright
from datetime import datetime
import time

logger = logging.getLogger('ExecutionEngine')


class LinkedInExecutor:
    """Execute LinkedIn posts using persistent browser session"""

    def __init__(self):
        self.user_data_dir = Path("Platinum_Tier/browser_data/linkedin")
        self.user_data_dir.mkdir(parents=True, exist_ok=True)
        self.max_retries = 3
        self.retry_delay = 2  # seconds

    async def post_content(self, content: str) -> bool:
        """
        Post content to LinkedIn

        Args:
            content: Post text content

        Returns:
            bool: True if successful, False otherwise
        """
        for attempt in range(self.max_retries):
            try:
                logger.info(f"LinkedIn post attempt {attempt + 1}/{self.max_retries}")

                async with async_playwright() as p:
                    # Use persistent context
                    context = await p.chromium.launch_persistent_context(
                        user_data_dir=str(self.user_data_dir),
                        headless=False,
                        args=['--disable-blink-features=AutomationControlled'],
                        viewport={'width': 1280, 'height': 720}
                    )

                    page = context.pages[0] if context.pages else await context.new_page()

                    # Navigate to feed
                    await page.goto("https://www.linkedin.com/feed/", wait_until="domcontentloaded")
                    await page.wait_for_timeout(3000)

                    # Check if logged in
                    if await page.query_selector('input[type="email"]'):
                        logger.error("Not logged in to LinkedIn. Please login manually first.")
                        await context.close()
                        return False

                    # Click "Start a post" button
                    start_post_button = await page.query_selector('button[aria-label*="Start a post"]')
                    if not start_post_button:
                        start_post_button = await page.query_selector('.share-box-feed-entry__trigger')

                    if start_post_button:
                        await start_post_button.click()
                        await page.wait_for_timeout(2000)

                        # Type content in editor
                        editor = await page.query_selector('.ql-editor')
                        if not editor:
                            editor = await page.query_selector('div[contenteditable="true"]')

                        if editor:
                            await editor.click()
                            await page.wait_for_timeout(500)
                            await editor.fill(content)
                            await page.wait_for_timeout(1000)

                            # Click Post button
                            post_button = await page.query_selector('button[aria-label*="Post"]')
                            if not post_button:
                                post_button = await page.query_selector('.share-actions__primary-action')

                            if post_button:
                                await post_button.click()
                                await page.wait_for_timeout(3000)

                                logger.info(f"✓ LinkedIn post created successfully")
                                logger.info(f"Content preview: {content[:100]}...")
                                await context.close()
                                return True
                            else:
                                logger.error("Could not find Post button")
                        else:
                            logger.error("Could not find editor")
                    else:
                        logger.error("Could not find 'Start a post' button")

                    await context.close()

            except Exception as e:
                logger.error(f"LinkedIn post attempt {attempt + 1} failed: {e}")
                if attempt < self.max_retries - 1:
                    delay = self.retry_delay * (2 ** attempt)  # Exponential backoff
                    logger.info(f"Retrying in {delay} seconds...")
                    await asyncio.sleep(delay)
                else:
                    logger.error("All LinkedIn post attempts failed")
                    return False

        return False


class WhatsAppExecutor:
    """Execute WhatsApp messages using persistent browser session"""

    def __init__(self):
        self.user_data_dir = Path("Platinum_Tier/browser_data/whatsapp")
        self.user_data_dir.mkdir(parents=True, exist_ok=True)
        self.max_retries = 3
        self.retry_delay = 2  # seconds

    async def send_message(self, contact_name: str, message: str) -> bool:
        """
        Send WhatsApp message

        Args:
            contact_name: Contact or group name
            message: Message text

        Returns:
            bool: True if successful, False otherwise
        """
        for attempt in range(self.max_retries):
            try:
                logger.info(f"WhatsApp message attempt {attempt + 1}/{self.max_retries}")

                async with async_playwright() as p:
                    # Use persistent context
                    context = await p.chromium.launch_persistent_context(
                        user_data_dir=str(self.user_data_dir),
                        headless=False,
                        args=['--disable-blink-features=AutomationControlled'],
                        viewport={'width': 1280, 'height': 720}
                    )

                    page = context.pages[0] if context.pages else await context.new_page()

                    # Navigate to WhatsApp Web
                    await page.goto("https://web.whatsapp.com/", wait_until="domcontentloaded")
                    await page.wait_for_timeout(3000)

                    # Check if QR code needed
                    if await page.query_selector('canvas[aria-label*="Scan"]'):
                        logger.error("WhatsApp not logged in. Please scan QR code first.")
                        await context.close()
                        return False

                    # Wait for chat list
                    await page.wait_for_selector('[data-testid="chat-list"]', timeout=30000)

                    # Search for contact
                    search_box = await page.query_selector('[data-testid="chat-list-search"]')
                    if not search_box:
                        search_box = await page.query_selector('div[contenteditable="true"][data-tab="3"]')

                    if search_box:
                        await search_box.click()
                        await page.wait_for_timeout(500)
                        await search_box.fill(contact_name)
                        await page.wait_for_timeout(2000)

                        # Click on first result
                        first_result = await page.query_selector('[data-testid="cell-frame-container"]')
                        if first_result:
                            await first_result.click()
                            await page.wait_for_timeout(1000)

                            # Type message
                            message_box = await page.query_selector('[data-testid="conversation-compose-box-input"]')
                            if not message_box:
                                message_box = await page.query_selector('div[contenteditable="true"][data-tab="10"]')

                            if message_box:
                                await message_box.click()
                                await page.wait_for_timeout(500)
                                await message_box.fill(message)
                                await page.wait_for_timeout(500)

                                # Press Enter to send
                                await page.keyboard.press('Enter')
                                await page.wait_for_timeout(1000)

                                logger.info(f"✓ WhatsApp message sent to {contact_name}")
                                logger.info(f"Message preview: {message[:100]}...")
                                await context.close()
                                return True
                            else:
                                logger.error("Could not find message box")
                        else:
                            logger.error(f"Could not find contact: {contact_name}")
                    else:
                        logger.error("Could not find search box")

                    await context.close()

            except Exception as e:
                logger.error(f"WhatsApp message attempt {attempt + 1} failed: {e}")
                if attempt < self.max_retries - 1:
                    delay = self.retry_delay * (2 ** attempt)  # Exponential backoff
                    logger.info(f"Retrying in {delay} seconds...")
                    await asyncio.sleep(delay)
                else:
                    logger.error("All WhatsApp message attempts failed")
                    return False

        return False


# Utility functions
def retry_with_backoff(max_retries: int = 3, initial_delay: float = 1.0):
    """
    Decorator for retry logic with exponential backoff

    Args:
        max_retries: Maximum number of retry attempts
        initial_delay: Initial delay in seconds (doubles each retry)
    """
    def decorator(func):
        async def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if attempt < max_retries - 1:
                        delay = initial_delay * (2 ** attempt)
                        logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay}s...")
                        await asyncio.sleep(delay)
                    else:
                        logger.error(f"All {max_retries} attempts failed: {e}")
                        raise
        return wrapper
    return decorator
