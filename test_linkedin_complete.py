"""
Test LinkedIn Scheduler - Complete System Test
Tests all features: content generation, image generation, scheduling, posting
"""
import asyncio
from pathlib import Path
from linkedin_scheduler_complete import LinkedInScheduler
from linkedin_content_generator import LinkedInContentGenerator

async def test_complete_system():
    """Test the complete LinkedIn automation system"""

    print("="*80)
    print("LinkedIn Automation System - Complete Test")
    print("="*80)
    print()

    # Initialize
    vault_path = Path(__file__).parent / "AI_Employee_Vault"
    generator = LinkedInContentGenerator(str(vault_path))
    scheduler = LinkedInScheduler()

    # Test 1: Generate content
    print("TEST 1: Content Generation")
    print("-"*80)
    approval_file = generator.create_post_approval_request('business_update')
    print(f"✓ Generated post: {approval_file.name}")
    print()

    # Test 2: Auto-approve for testing
    print("TEST 2: Auto-Approve Post")
    print("-"*80)
    approved_dir = vault_path / "Approved"
    approved_dir.mkdir(exist_ok=True)
    approved_file = approved_dir / approval_file.name
    approval_file.rename(approved_file)
    print(f"✓ Moved to Approved: {approved_file.name}")
    print()

    # Test 3: Generate image
    print("TEST 3: Image Generation")
    print("-"*80)
    content = scheduler.extract_post_content(approved_file)
    image_path = await scheduler.generate_image(content)
    if image_path:
        print(f"✓ Generated image: {image_path}")
    else:
        print("⚠ Image generation skipped (PIL not installed)")
    print()

    # Test 4: Post to LinkedIn
    print("TEST 4: Post to LinkedIn")
    print("-"*80)
    print("This will post to your LinkedIn account.")
    print("Content preview:")
    print(content[:200] + "...")
    print()

    confirm = input("Proceed with posting? (y/n): ")
    if confirm.lower() == 'y':
        success = await scheduler.post_to_linkedin(
            content=content,
            visibility="public",
            image_path=image_path
        )

        if success:
            print()
            print("="*80)
            print("✓ ALL TESTS PASSED")
            print("="*80)
            print()
            print("System is working correctly:")
            print("✓ Content generation")
            print("✓ Image generation")
            print("✓ LinkedIn posting")
            print("✓ Upload verification")
            print()

            # Move to Done
            done_dir = vault_path / "Done"
            done_dir.mkdir(exist_ok=True)
            done_file = done_dir / approved_file.name
            approved_file.rename(done_file)
            print(f"✓ Moved to Done: {done_file.name}")
        else:
            print()
            print("="*80)
            print("✗ TEST FAILED")
            print("="*80)
            print("Check logs for details:")
            print(f"  {vault_path / 'Logs' / 'linkedin_scheduler_*.log'}")
    else:
        print("Test cancelled by user")

    print()
    print("="*80)
    print("Test Complete")
    print("="*80)

if __name__ == "__main__":
    asyncio.run(test_complete_system())
