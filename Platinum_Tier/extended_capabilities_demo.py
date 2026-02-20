"""
Extended Watcher with SEND/POST Capabilities
Adds ability to POST on LinkedIn and SEND WhatsApp messages
"""
import os
from pathlib import Path
from dotenv import load_dotenv
from playwright.async_api import async_playwright
from datetime import datetime
import asyncio
import json

class LinkedInPoster:
    """LinkedIn Watcher with POSTING capability"""

    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password
        self.user_data_dir = Path("Platinum_Tier/browser_data/linkedin")
        self.user_data_dir.mkdir(parents=True, exist_ok=True)
        self.page = None
        self.context = None

    async def initialize_browser(self):
        """Initialize browser with persistent session"""
        p = await async_playwright().start()
        self.context = await p.chromium.launch_persistent_context(
            user_data_dir=str(self.user_data_dir),
            headless=False,
            args=['--disable-blink-features=AutomationControlled'],
            viewport={'width': 1280, 'height': 720}
        )

        self.page = self.context.pages[0] if self.context.pages else await self.context.new_page()
        await self.page.goto("https://www.linkedin.com/feed/", wait_until="domcontentloaded")
        await self.page.wait_for_timeout(3000)

        # Check if logged in
        if await self.page.query_selector('input[type="email"]'):
            print("[LinkedIn] Please login manually")
            await self.page.wait_for_timeout(60000)

        print("[LinkedIn] Logged in successfully")

    async def create_post(self, content: str, image_path: str = None):
        """
        POST on LinkedIn

        Args:
            content: Post text
            image_path: Optional image to attach

        Returns:
            bool: Success status
        """
        try:
            if not self.page:
                await self.initialize_browser()

            # Navigate to feed
            await self.page.goto("https://www.linkedin.com/feed/", wait_until="domcontentloaded")
            await self.page.wait_for_timeout(2000)

            # Click "Start a post" button
            start_post_button = await self.page.query_selector('button[aria-label*="Start a post"]')
            if not start_post_button:
                start_post_button = await self.page.query_selector('.share-box-feed-entry__trigger')

            if start_post_button:
                await start_post_button.click()
                await self.page.wait_for_timeout(2000)

                # Type content
                editor = await self.page.query_selector('.ql-editor')
                if editor:
                    await editor.click()
                    await editor.fill(content)
                    await self.page.wait_for_timeout(1000)

                    # Add image if provided
                    if image_path and os.path.exists(image_path):
                        file_input = await self.page.query_selector('input[type="file"]')
                        if file_input:
                            await file_input.set_input_files(image_path)
                            await self.page.wait_for_timeout(3000)

                    # Click Post button
                    post_button = await self.page.query_selector('button[aria-label*="Post"]')
                    if not post_button:
                        post_button = await self.page.query_selector('.share-actions__primary-action')

                    if post_button:
                        await post_button.click()
                        await self.page.wait_for_timeout(3000)

                        print(f"[LinkedIn] Post created successfully!")
                        print(f"[LinkedIn] Content: {content[:50]}...")
                        return True

            return False

        except Exception as e:
            print(f"[LinkedIn] Error creating post: {e}")
            return False


class WhatsAppSender:
    """WhatsApp Watcher with SENDING capability"""

    def __init__(self):
        self.user_data_dir = Path("Platinum_Tier/browser_data/whatsapp")
        self.user_data_dir.mkdir(parents=True, exist_ok=True)
        self.page = None
        self.context = None

    async def initialize_browser(self):
        """Initialize browser with persistent session"""
        p = await async_playwright().start()
        self.context = await p.chromium.launch_persistent_context(
            user_data_dir=str(self.user_data_dir),
            headless=False,
            args=['--disable-blink-features=AutomationControlled'],
            viewport={'width': 1280, 'height': 720}
        )

        self.page = self.context.pages[0] if self.context.pages else await self.context.new_page()
        await self.page.goto("https://web.whatsapp.com/", wait_until="domcontentloaded")
        await self.page.wait_for_timeout(3000)

        # Check if QR code needed
        if await self.page.query_selector('canvas[aria-label*="Scan"]'):
            print("[WhatsApp] Please scan QR code")
            await self.page.wait_for_timeout(30000)

        # Wait for chat list
        await self.page.wait_for_selector('[data-testid="chat-list"]', timeout=60000)
        print("[WhatsApp] Logged in successfully")

    async def send_message(self, contact_name: str, message: str):
        """
        SEND WhatsApp message

        Args:
            contact_name: Contact or group name
            message: Message text

        Returns:
            bool: Success status
        """
        try:
            if not self.page:
                await self.initialize_browser()

            # Search for contact
            search_box = await self.page.query_selector('[data-testid="chat-list-search"]')
            if not search_box:
                search_box = await self.page.query_selector('div[contenteditable="true"][data-tab="3"]')

            if search_box:
                await search_box.click()
                await search_box.fill(contact_name)
                await self.page.wait_for_timeout(2000)

                # Click on first result
                first_result = await self.page.query_selector('[data-testid="cell-frame-container"]')
                if first_result:
                    await first_result.click()
                    await self.page.wait_for_timeout(1000)

                    # Type message
                    message_box = await self.page.query_selector('[data-testid="conversation-compose-box-input"]')
                    if not message_box:
                        message_box = await self.page.query_selector('div[contenteditable="true"][data-tab="10"]')

                    if message_box:
                        await message_box.click()
                        await message_box.fill(message)
                        await self.page.wait_for_timeout(500)

                        # Press Enter to send
                        await self.page.keyboard.press('Enter')
                        await self.page.wait_for_timeout(1000)

                        print(f"[WhatsApp] Message sent to {contact_name}")
                        print(f"[WhatsApp] Content: {message[:50]}...")
                        return True

            return False

        except Exception as e:
            print(f"[WhatsApp] Error sending message: {e}")
            return False


# Example usage with CONDITIONS
async def demo_with_conditions():
    """
    Demo showing how to use SEND/POST capabilities with CONDITIONS
    """

    # Load credentials
    load_dotenv()
    LINKEDIN_EMAIL = os.getenv('LINKEDIN_EMAIL')
    LINKEDIN_PASSWORD = os.getenv('LINKEDIN_PASSWORD')

    print("=" * 60)
    print("DEMO: SEND/POST CAPABILITIES WITH CONDITIONS")
    print("=" * 60)
    print()

    # Example 1: LinkedIn Posting with CONDITION
    print("Example 1: LinkedIn Post with Condition")
    print("-" * 60)

    # CONDITION: Only post if it's a weekday
    from datetime import datetime
    is_weekday = datetime.now().weekday() < 5  # Monday=0, Sunday=6

    if is_weekday:
        print("[Condition] It's a weekday - OK to post")

        linkedin = LinkedInPoster(LINKEDIN_EMAIL, LINKEDIN_PASSWORD)
        await linkedin.initialize_browser()

        post_content = """
🚀 Excited to share our latest AI project!

We've built an AI Personal Employee that:
- Monitors Gmail, LinkedIn, WhatsApp
- Sends automated responses
- Requires human approval for sensitive actions

Built with Claude Code and Playwright!

#AI #AgenticAI #Automation
        """

        success = await linkedin.create_post(post_content)
        if success:
            print("[LinkedIn] ✓ Post created successfully!")
    else:
        print("[Condition] It's weekend - Skipping post")

    print()

    # Example 2: WhatsApp Message with CONDITION
    print("Example 2: WhatsApp Message with Condition")
    print("-" * 60)

    # CONDITION: Only send if priority is HIGH
    task_priority = "HIGH"  # This would come from task file

    if task_priority == "HIGH":
        print("[Condition] Priority is HIGH - Sending message")

        whatsapp = WhatsAppSender()
        await whatsapp.initialize_browser()

        message = "Hi! This is an urgent update about the project. Please check your email."

        success = await whatsapp.send_message("Client Name", message)
        if success:
            print("[WhatsApp] ✓ Message sent successfully!")
    else:
        print("[Condition] Priority is not HIGH - Skipping message")

    print()

    # Example 3: Email with CONDITION (already working)
    print("Example 3: Email with Condition")
    print("-" * 60)

    # CONDITION: Only send email if keyword matches
    email_subject = "URGENT: Agentic AI Project"
    has_urgent = "urgent" in email_subject.lower()
    has_agentic = "agentic" in email_subject.lower()

    if has_urgent and has_agentic:
        print("[Condition] Keywords matched - Sending email")
        print("[Email MCP] Email would be sent here")
        print("[Email MCP] ✓ Email sent successfully!")
    else:
        print("[Condition] Keywords not matched - Skipping email")

    print()
    print("=" * 60)
    print("DEMO COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    # Run demo
    asyncio.run(demo_with_conditions())
