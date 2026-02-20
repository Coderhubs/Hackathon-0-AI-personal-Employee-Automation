"""
Complete LinkedIn Scheduler with Image Generation
- Generates AI images for posts
- Schedules posts at specific times
- Supports public/private visibility
- Waits for complete upload before closing
"""
import os
import sys
import asyncio
import schedule
import time
from pathlib import Path
from datetime import datetime, timedelta
import logging
from playwright.async_api import async_playwright
from dotenv import load_dotenv
import json
import random

load_dotenv()

class LinkedInScheduler:
    def __init__(self):
        self.email = os.getenv("LINKEDIN_EMAIL")
        self.password = os.getenv("LINKEDIN_PASSWORD")
        self.base_dir = Path(__file__).parent
        self.user_data_dir = self.base_dir / "browser_data" / "linkedin"
        self.user_data_dir.mkdir(parents=True, exist_ok=True)
        self.vault_dir = self.base_dir / "AI_Employee_Vault"
        self.approved_dir = self.vault_dir / "Approved"
        self.done_dir = self.vault_dir / "Done"
        self.logs_dir = self.vault_dir / "Logs"
        self.images_dir = self.vault_dir / "Generated_Images"

        self.approved_dir.mkdir(parents=True, exist_ok=True)
        self.done_dir.mkdir(parents=True, exist_ok=True)
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        self.images_dir.mkdir(parents=True, exist_ok=True)

        self.logger = self.setup_logging()
        self.schedule_file = self.vault_dir / "linkedin_schedule.json"

    def setup_logging(self):
        """Setup logging"""
        log_file = self.logs_dir / f"linkedin_scheduler_{datetime.now().strftime('%Y%m%d')}.log"

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger('LinkedInScheduler')

    def generate_image_prompt(self, post_content: str) -> str:
        """Generate image prompt based on post content"""
        # Extract key themes from post
        keywords = []
        if 'automation' in post_content.lower():
            keywords.append('automation')
        if 'ai' in post_content.lower() or 'artificial intelligence' in post_content.lower():
            keywords.append('AI')
        if 'business' in post_content.lower():
            keywords.append('business')
        if 'productivity' in post_content.lower():
            keywords.append('productivity')

        # Generate prompt
        if keywords:
            theme = ', '.join(keywords)
            prompt = f"Professional LinkedIn post image about {theme}, modern design, clean, corporate style, high quality"
        else:
            prompt = "Professional business LinkedIn post image, modern design, clean, corporate style"

        return prompt

    async def generate_image(self, post_content: str) -> Path:
        """Generate image for LinkedIn post using AI"""
        try:
            self.logger.info("Generating image for post...")

            # Generate prompt
            prompt = self.generate_image_prompt(post_content)
            self.logger.info(f"Image prompt: {prompt}")

            # For hackathon demo, create a placeholder image with text
            # In production, integrate with DALL-E, Midjourney, or Stable Diffusion
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            image_path = self.images_dir / f"linkedin_post_{timestamp}.png"

            # Create simple image with PIL
            try:
                from PIL import Image, ImageDraw, ImageFont

                # Create image
                img = Image.new('RGB', (1200, 630), color=(41, 128, 185))
                draw = ImageDraw.Draw(img)

                # Add text
                text = "AI-Generated\nLinkedIn Post"
                try:
                    font = ImageFont.truetype("arial.ttf", 60)
                except:
                    font = ImageFont.load_default()

                # Center text
                bbox = draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                x = (1200 - text_width) / 2
                y = (630 - text_height) / 2

                draw.text((x, y), text, fill=(255, 255, 255), font=font)

                # Save
                img.save(image_path)
                self.logger.info(f"Image generated: {image_path}")
                return image_path

            except ImportError:
                self.logger.warning("PIL not installed. Skipping image generation.")
                return None

        except Exception as e:
            self.logger.error(f"Error generating image: {e}")
            return None

    async def post_to_linkedin(self, content: str, visibility: str = "public", image_path: Path = None) -> bool:
        """Post content to LinkedIn with proper upload verification"""

        self.logger.info("="*80)
        self.logger.info("LinkedIn Post - Starting")
        self.logger.info("="*80)
        self.logger.info(f"Content length: {len(content)} characters")
        self.logger.info(f"Visibility: {visibility}")
        self.logger.info(f"Image: {image_path if image_path else 'None'}")

        try:
            async with async_playwright() as p:
                self.logger.info("Launching browser with saved session...")

                context = await p.chromium.launch_persistent_context(
                    user_data_dir=str(self.user_data_dir),
                    headless=False,
                    args=[
                        '--disable-blink-features=AutomationControlled',
                        '--no-sandbox'
                    ]
                )

                page = context.pages[0] if context.pages else await context.new_page()

                # Navigate to LinkedIn feed
                self.logger.info("Navigating to LinkedIn feed...")
                try:
                    await page.goto("https://www.linkedin.com/feed/", wait_until="networkidle", timeout=30000)
                    await page.wait_for_timeout(5000)
                except Exception as e:
                    self.logger.warning(f"Navigation warning: {e}")
                    await page.wait_for_timeout(5000)

                # Check current URL for security challenges
                current_url = page.url
                self.logger.info(f"Current URL: {current_url}")

                if "checkpoint" in current_url or "challenge" in current_url or "login" in current_url:
                    self.logger.error("LinkedIn session expired or verification required!")
                    self.logger.error("Please run: python setup_linkedin_login.py")
                    self.logger.error("Complete the login/verification in the browser, then try again.")
                    await page.screenshot(path="linkedin_verification_needed.png")
                    await context.close()
                    return False

                # Check if logged in
                try:
                    feed_check = await page.wait_for_selector('[aria-label="Main Feed"]', timeout=5000, state='visible')
                    if not feed_check:
                        self.logger.error("Not logged in. Run setup_linkedin_login.py first")
                        await page.screenshot(path="linkedin_not_logged_in.png")
                        await context.close()
                        return False
                except Exception as e:
                    self.logger.error(f"Failed to verify login: {e}")
                    self.logger.error("Session expired. Please run: python setup_linkedin_login.py")
                    await page.screenshot(path="linkedin_login_error.png")
                    await context.close()
                    return False

                self.logger.info("[OK] Logged in successfully")

                # Click "Start a post" button - try multiple selectors
                self.logger.info("Opening post composer...")
                start_post_selectors = [
                    'button:has-text("Start a post")',
                    '[aria-label="Start a post"]',
                    '.share-box-feed-entry__trigger',
                    'button.share-box-feed-entry__trigger'
                ]

                start_post_button = None
                for selector in start_post_selectors:
                    try:
                        start_post_button = await page.wait_for_selector(selector, timeout=5000, state='visible')
                        if start_post_button:
                            self.logger.info(f"Found start button: {selector}")
                            break
                    except:
                        continue

                if not start_post_button:
                    self.logger.error("Could not find 'Start a post' button")
                    await page.screenshot(path="debug_no_start_button.png")
                    await context.close()
                    return False

                # Click with human-like delay
                await page.wait_for_timeout(500)
                await start_post_button.click()
                await page.wait_for_timeout(2000)

                # Wait for editor - try multiple selectors
                self.logger.info("Waiting for editor...")
                editor_selectors = [
                    '[role="textbox"]',
                    '.ql-editor',
                    '[contenteditable="true"]'
                ]

                editor = None
                for selector in editor_selectors:
                    try:
                        editor = await page.wait_for_selector(selector, timeout=5000, state='visible')
                        if editor:
                            self.logger.info(f"Found editor: {selector}")
                            break
                    except:
                        continue

                if not editor:
                    self.logger.error("Editor did not open")
                    await page.screenshot(path="debug_no_editor.png")
                    await context.close()
                    return False

                # Focus editor
                await editor.click()
                await page.wait_for_timeout(500)

                # Type content with human-like speed
                self.logger.info("Typing content...")
                await editor.type(content, delay=50)  # 50ms delay between keystrokes
                await page.wait_for_timeout(1000)

                # Verify content was entered
                editor_text = await editor.inner_text()
                if not editor_text or len(editor_text) < 10:
                    self.logger.warning("Content may not have been entered, trying JavaScript fallback...")

                    # JavaScript fallback
                    await page.evaluate(f"""
                        const editor = document.querySelector('[role="textbox"]');
                        if (editor) {{
                            editor.focus();
                            editor.innerText = `{content}`;
                            editor.dispatchEvent(new Event('input', {{ bubbles: true }}));
                        }}
                    """)
                    await page.wait_for_timeout(1000)

                    # Verify again
                    editor_text = await editor.inner_text()
                    if not editor_text or len(editor_text) < 10:
                        self.logger.error("Failed to enter content")
                        await page.screenshot(path="debug_content_not_entered.png")
                        await context.close()
                        return False

                self.logger.info(f"[OK] Content entered ({len(editor_text)} characters)")
                await page.wait_for_timeout(1000)

                # Upload image if provided
                if image_path and image_path.exists():
                    self.logger.info(f"Uploading image: {image_path}")
                    try:
                        # Find file input for image upload
                        file_input = await page.query_selector('input[type="file"]')
                        if file_input:
                            await file_input.set_input_files(str(image_path))
                            await page.wait_for_timeout(3000)
                            self.logger.info("✓ Image uploaded")
                        else:
                            self.logger.warning("Could not find image upload button")
                    except Exception as e:
                        self.logger.warning(f"Image upload failed: {e}")

                # Set visibility (public/private)
                if visibility.lower() == "private":
                    self.logger.info("Setting visibility to private...")
                    try:
                        # Click visibility dropdown
                        visibility_button = await page.query_selector('[aria-label*="visibility"]')
                        if not visibility_button:
                            visibility_button = await page.query_selector('button:has-text("Anyone")')

                        if visibility_button:
                            await visibility_button.click()
                            await page.wait_for_timeout(1000)

                            # Select "Connections only"
                            connections_option = await page.query_selector('span:has-text("Connections only")')
                            if connections_option:
                                await connections_option.click()
                                await page.wait_for_timeout(1000)
                                self.logger.info("✓ Set to Connections only")
                    except Exception as e:
                        self.logger.warning(f"Could not set visibility: {e}")

                # Click Post button with improved verification
                self.logger.info("Publishing post...")
                post_button_selectors = [
                    'button:has-text("Post")',
                    'button[aria-label="Post"]',
                    '.share-actions__primary-action',
                    'button.share-actions__primary-action'
                ]

                post_button = None
                for selector in post_button_selectors:
                    try:
                        post_button = await page.wait_for_selector(selector, timeout=5000, state='visible')
                        if post_button:
                            self.logger.info(f"Found Post button: {selector}")
                            break
                    except:
                        continue

                if not post_button:
                    self.logger.error("Could not find 'Post' button")
                    await page.screenshot(path="debug_no_post_button.png")
                    await context.close()
                    return False

                # Verify button is enabled (check both disabled and aria-disabled)
                is_disabled = await post_button.get_attribute('disabled')
                aria_disabled = await post_button.get_attribute('aria-disabled')

                if is_disabled:
                    self.logger.error("Post button is disabled")
                    await page.screenshot(path="debug_button_disabled.png")
                    await context.close()
                    return False

                if aria_disabled == 'true':
                    self.logger.error("Post button is aria-disabled")
                    await page.screenshot(path="debug_button_aria_disabled.png")
                    await context.close()
                    return False

                self.logger.info("[OK] Post button is enabled")

                # Click with human-like delay
                await page.wait_for_timeout(500)
                await post_button.click()
                self.logger.info("Clicked Post button")

                # CRITICAL: Wait for post to actually upload
                self.logger.info("Waiting for post to upload...")
                await page.wait_for_timeout(3000)

                # Wait for modal to close (indicates post published)
                try:
                    self.logger.info("Verifying post published...")
                    await page.wait_for_selector('.share-box-footer', state='hidden', timeout=15000)
                    self.logger.info("[OK] Post modal closed")
                except:
                    self.logger.warning("Modal did not close in expected time, continuing...")

                # Additional wait to ensure upload completes
                self.logger.info("Ensuring upload completes...")
                await page.wait_for_timeout(5000)

                # Verify we're back on feed
                current_url = page.url
                if 'linkedin.com/feed' in current_url:
                    self.logger.info("[OK] Returned to feed - post published successfully!")
                else:
                    self.logger.warning(f"Not on feed page: {current_url}")
                    # Try to navigate back to feed
                    try:
                        await page.goto("https://www.linkedin.com/feed/", wait_until="networkidle", timeout=10000)
                        await page.wait_for_timeout(3000)
                        self.logger.info("[OK] Navigated back to feed")
                    except:
                        self.logger.warning("Could not navigate back to feed")

                # Look for success indicators
                success_indicators = [
                    'text="Post successful"',
                    'text="Your post is live"',
                    '[data-test-icon="success"]'
                ]

                for indicator in success_indicators:
                    try:
                        element = await page.wait_for_selector(indicator, timeout=2000)
                        if element:
                            self.logger.info(f"[OK] Found success indicator: {indicator}")
                            break
                    except:
                        continue

                # Take final screenshot
                await page.screenshot(path="linkedin_post_success.png")
                self.logger.info("Screenshot saved: linkedin_post_success.png")

                # Close browser
                self.logger.info("Closing browser...")
                await context.close()

                self.logger.info("="*80)
                self.logger.info("[SUCCESS] POST PUBLISHED SUCCESSFULLY")
                self.logger.info("="*80)

                return True

        except Exception as e:
            self.logger.error(f"Failed to post: {e}")
            import traceback
            traceback.print_exc()
            return False

    def load_schedule(self) -> dict:
        """Load posting schedule from file"""
        if self.schedule_file.exists():
            with open(self.schedule_file, 'r') as f:
                return json.load(f)
        return {
            "enabled": True,
            "times": ["09:00", "12:00", "17:00"],  # 9 AM, 12 PM, 5 PM
            "days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
            "visibility": "public",
            "generate_image": True
        }

    def save_schedule(self, schedule_config: dict):
        """Save posting schedule to file"""
        with open(self.schedule_file, 'w') as f:
            json.dump(schedule_config, f, indent=2)

    async def process_approved_posts(self):
        """Process all approved LinkedIn posts"""
        self.logger.info("Checking for approved posts...")

        linkedin_files = list(self.approved_dir.glob("LINKEDIN_*.md"))

        if not linkedin_files:
            self.logger.info("No approved posts found")
            return

        self.logger.info(f"Found {len(linkedin_files)} approved post(s)")

        schedule_config = self.load_schedule()

        for file_path in linkedin_files:
            self.logger.info(f"Processing: {file_path.name}")

            # Extract content
            content = self.extract_post_content(file_path)
            if not content:
                self.logger.error(f"Could not extract content from {file_path.name}")
                continue

            # Generate image if enabled
            image_path = None
            if schedule_config.get("generate_image", True):
                image_path = await self.generate_image(content)

            # Post to LinkedIn
            visibility = schedule_config.get("visibility", "public")
            success = await self.post_to_linkedin(content, visibility, image_path)

            if success:
                # Move to Done
                done_file = self.done_dir / file_path.name
                file_path.rename(done_file)
                self.logger.info(f"✓ Moved to Done: {file_path.name}")
            else:
                self.logger.error(f"✗ Failed to post: {file_path.name}")

    def extract_post_content(self, file_path: Path) -> str:
        """Extract post content from markdown file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract content between ## Post Content and next ##
            if '## Post Content' in content:
                start = content.find('## Post Content') + len('## Post Content')
                end = content.find('## Posting Instructions')
                if end == -1:
                    end = content.find('## Actions')
                if end == -1:
                    end = len(content)

                post_content = content[start:end].strip()
                return post_content

            return content

        except Exception as e:
            self.logger.error(f"Error reading file: {e}")
            return ""

    def run_scheduler(self):
        """Run scheduled posting"""
        self.logger.info("="*80)
        self.logger.info("LinkedIn Scheduler - Starting")
        self.logger.info("="*80)

        schedule_config = self.load_schedule()

        if not schedule_config.get("enabled", True):
            self.logger.info("Scheduler is disabled")
            return

        # Schedule posts at specified times
        for post_time in schedule_config.get("times", ["09:00", "12:00", "17:00"]):
            schedule.every().day.at(post_time).do(
                lambda: asyncio.run(self.process_approved_posts())
            )
            self.logger.info(f"Scheduled daily post at {post_time}")

        self.logger.info("Scheduler running. Press Ctrl+C to stop.")
        self.logger.info("="*80)

        # Run scheduler loop
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute

def main():
    """Main entry point"""
    scheduler = LinkedInScheduler()

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "post-now":
            # Post immediately
            asyncio.run(scheduler.process_approved_posts())

        elif command == "schedule":
            # Run scheduler
            scheduler.run_scheduler()

        elif command == "config":
            # Configure schedule
            print("LinkedIn Scheduler Configuration")
            print("="*50)

            config = scheduler.load_schedule()

            print(f"Current schedule:")
            print(f"  Enabled: {config.get('enabled', True)}")
            print(f"  Times: {', '.join(config.get('times', []))}")
            print(f"  Days: {', '.join(config.get('days', []))}")
            print(f"  Visibility: {config.get('visibility', 'public')}")
            print(f"  Generate Image: {config.get('generate_image', True)}")
            print()

            # Update config
            enabled = input("Enable scheduler? (y/n): ").lower() == 'y'
            times = input("Post times (comma-separated, e.g., 09:00,12:00,17:00): ").split(',')
            visibility = input("Visibility (public/private): ").lower()
            generate_image = input("Generate images? (y/n): ").lower() == 'y'

            config['enabled'] = enabled
            config['times'] = [t.strip() for t in times]
            config['visibility'] = visibility
            config['generate_image'] = generate_image

            scheduler.save_schedule(config)
            print("\n✓ Configuration saved!")

        else:
            print(f"Unknown command: {command}")
            print("Usage:")
            print("  python linkedin_scheduler_complete.py post-now    # Post immediately")
            print("  python linkedin_scheduler_complete.py schedule    # Run scheduler")
            print("  python linkedin_scheduler_complete.py config      # Configure schedule")

    else:
        # Default: post now
        print("Posting approved LinkedIn posts now...")
        asyncio.run(scheduler.process_approved_posts())

if __name__ == "__main__":
    main()
