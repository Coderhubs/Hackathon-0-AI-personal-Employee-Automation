#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LinkedIn Cookie-Based Posting Script
Posts to LinkedIn using cookie authentication (no API key needed)
"""

import sys
import io
import requests
import json
import os
import shutil
from datetime import datetime
from pathlib import Path

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def extract_chrome_cookie():
    """Try to extract li_at cookie from Chrome browser"""
    try:
        import browser_cookie3
        cookies = browser_cookie3.chrome(domain_name='.linkedin.com')
        for cookie in cookies:
            if cookie.name == 'li_at':
                print(f"✅ Found li_at cookie from Chrome: {cookie.value[:20]}...")
                return cookie.value
    except ImportError:
        print("⚠️  browser_cookie3 not installed. Install with: pip install browser_cookie3")
    except Exception as e:
        print(f"⚠️  Could not extract cookie from Chrome: {e}")
    return None

def get_cookie_manual():
    """Ask user to paste cookie manually"""
    print("\n" + "="*60)
    print("HOW TO GET YOUR li_at COOKIE:")
    print("="*60)
    print("1. Open Chrome and go to linkedin.com")
    print("2. Press F12 to open DevTools")
    print("3. Go to 'Application' tab")
    print("4. Click 'Cookies' → 'https://www.linkedin.com'")
    print("5. Find 'li_at' cookie and copy its Value")
    print("="*60)
    cookie = input("\nPaste your li_at cookie here: ").strip()
    return cookie if cookie else None

def read_approved_post(approved_folder):
    """Read the first approved post from the folder"""
    approved_path = Path(approved_folder)
    if not approved_path.exists():
        print(f"❌ Approved folder not found: {approved_folder}")
        return None, None

    posts = list(approved_path.glob("*.md"))
    if not posts:
        print(f"❌ No approved posts found in {approved_folder}")
        return None, None

    post_file = posts[0]
    print(f"📄 Reading post: {post_file.name}")

    with open(post_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract post content between "## Post Content" and "## Posting Instructions"
    lines = content.split('\n')
    post_lines = []
    in_content = False

    for line in lines:
        if line.strip() == "## Post Content":
            in_content = True
            continue
        if line.strip().startswith("## ") and in_content:
            break
        if in_content and line.strip():
            post_lines.append(line)

    post_text = '\n'.join(post_lines).strip()
    return post_text, post_file

def post_to_linkedin(cookie, post_text):
    """Post to LinkedIn using cookie authentication"""

    # LinkedIn API endpoint
    url = "https://www.linkedin.com/voyager/api/contentcreation/normShares"

    # Create session
    session = requests.Session()
    session.cookies.set('li_at', cookie, domain='.linkedin.com')

    # First, get CSRF token by making a request to LinkedIn
    try:
        # Get the feed page to extract CSRF token
        feed_response = session.get('https://www.linkedin.com/feed/', headers={
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'accept-language': 'en-US,en;q=0.9',
        })

        if feed_response.status_code != 200:
            print(f"Failed to access LinkedIn feed. Status: {feed_response.status_code}")
            print("Your cookie might be expired or invalid.")
            return False

        # Extract CSRF token from cookies - LinkedIn sets this as JSESSIONID
        csrf_token = None
        for cookie_obj in session.cookies:
            if cookie_obj.name == 'JSESSIONID':
                csrf_token = cookie_obj.value.strip('"')
                print(f"Got CSRF token from JSESSIONID: {csrf_token[:20]}...")
                break

        if not csrf_token:
            # Try to extract from page HTML
            import re
            match = re.search(r'"clientPageInstanceId":"([^"]+)"', feed_response.text)
            if match:
                csrf_token = match.group(1)
                print(f"Got CSRF token from page: {csrf_token[:20]}...")
            else:
                print("Could not find CSRF token. Using default...")
                csrf_token = "ajax:0123456789012345678"

    except Exception as e:
        print(f"Error getting CSRF token: {e}")
        csrf_token = "ajax:0123456789012345678"
        print("Using default CSRF token...")

    # Headers with CSRF token
    headers = {
        'authority': 'www.linkedin.com',
        'accept': 'application/vnd.linkedin.normalized+json+2.1',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json; charset=UTF-8',
        'csrf-token': csrf_token,
        'origin': 'https://www.linkedin.com',
        'referer': 'https://www.linkedin.com/feed/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'x-li-lang': 'en_US',
        'x-restli-protocol-version': '2.0.0'
    }

    # Payload for creating a post
    payload = {
        "visibleToConnectionsOnly": False,
        "externalAudienceProviders": [],
        "commentaryV2": {
            "text": post_text,
            "attributes": []
        },
        "origin": "FEED",
        "allowedCommentersScope": "ALL"
    }

    print("\n" + "="*60)
    print("POSTING TO LINKEDIN...")
    print("="*60)
    print(f"Post text ({len(post_text)} chars):")
    print("-"*60)
    print(post_text[:200] + "..." if len(post_text) > 200 else post_text)
    print("-"*60)

    try:
        response = session.post(url, headers=headers, json=payload, timeout=30)

        print(f"\n📡 Response Status: {response.status_code}")

        if response.status_code in [200, 201]:
            print("✅ POST SUCCESSFUL!")
            print(f"Response: {response.text[:200]}")
            return True
        else:
            print(f"❌ POST FAILED!")
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text[:500]}")
            return False

    except Exception as e:
        print(f"❌ Error posting to LinkedIn: {e}")
        return False

def move_to_done(post_file, done_folder):
    """Move the posted file to Done folder"""
    done_path = Path(done_folder)
    done_path.mkdir(parents=True, exist_ok=True)

    # Add timestamp to filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    new_name = f"POSTED_{timestamp}_{post_file.name}"
    destination = done_path / new_name

    shutil.move(str(post_file), str(destination))
    print(f"✅ Moved to: {destination}")

def main():
    print("="*60)
    print("LINKEDIN COOKIE-BASED POSTER")
    print("="*60)

    # Paths
    base_path = Path(__file__).parent
    approved_folder = base_path / "AI_Employee_Vault" / "Approved"
    done_folder = base_path / "AI_Employee_Vault" / "Done"

    # Step 1: Get cookie
    print("\nStep 1: Getting LinkedIn cookie...")

    cookie = None

    # Priority 1: Check for .linkedin_session file
    session_file = base_path / ".linkedin_session"
    if session_file.exists():
        try:
            with open(session_file, 'r') as f:
                cookie = f.read().strip()
            if cookie:
                print(f"Using cookie from .linkedin_session file: {cookie[:20]}...")
        except Exception as e:
            print(f"Could not read .linkedin_session file: {e}")

    # Priority 2: Check for command-line argument
    if not cookie and len(sys.argv) > 1:
        cookie = sys.argv[1].strip()
        print(f"Using cookie from command line: {cookie[:20]}...")

    # Priority 3: Try automatic extraction from Chrome
    if not cookie:
        cookie = extract_chrome_cookie()

    if not cookie:
        print("\n" + "="*60)
        print("NO COOKIE FOUND - MANUAL STEPS REQUIRED")
        print("="*60)
        print("HOW TO GET YOUR li_at COOKIE:")
        print("1. Open Chrome and go to linkedin.com")
        print("2. Press F12 to open DevTools")
        print("3. Go to 'Application' tab")
        print("4. Click 'Cookies' -> 'https://www.linkedin.com'")
        print("5. Find 'li_at' cookie and copy its Value")
        print("\nThen either:")
        print('- Save to .linkedin_session file in project root')
        print('- Or run: python linkedin_cookie_post.py "YOUR_COOKIE_HERE"')
        print("="*60)
        return

    # Step 2: Read approved post
    print("\n📄 Step 2: Reading approved post...")
    post_text, post_file = read_approved_post(approved_folder)

    if not post_text:
        print("❌ No post content found. Exiting.")
        return

    # Step 3: Post to LinkedIn
    print("\n🚀 Step 3: Posting to LinkedIn...")
    success = post_to_linkedin(cookie, post_text)

    # Step 4: Move to Done if successful
    if success:
        print("\n📦 Step 4: Moving to Done folder...")
        move_to_done(post_file, done_folder)
        print("\n" + "="*60)
        print("✅ ALL DONE! Post published successfully!")
        print("="*60)
    else:
        print("\n❌ Posting failed. File remains in Approved folder.")
        print("Check your cookie and try again.")

if __name__ == "__main__":
    main()
