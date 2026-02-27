#!/usr/bin/env python3
"""
Beta.mr Procurement Monitor
Checks beta.mr for new announcements and sends WhatsApp notifications
"""

import requests
from bs4 import BeautifulSoup
import json
import os
import sys
from datetime import datetime
from urllib.parse import urljoin

# Configuration
BETA_URL = "https://www.beta.mr/"
STATE_FILE = "last_state.json"
WHATSAPP_PHONE = os.environ.get('WHATSAPP_PHONE', '')  # Your phone number with country code
WHATSAPP_API_KEY = os.environ.get('WHATSAPP_API_KEY', '')  # CallMeBot API key

def fetch_announcements():
    """Fetch current announcements from beta.mr"""
    try:
        print(f"[{datetime.now()}] Fetching {BETA_URL}...")
        response = requests.get(BETA_URL, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        announcements = {}
        
        # Find all announcement links
        # Format: /beta/offre/title/ID or /beta/annonces_specials/ID
        links = soup.find_all('a', href=True)
        
        for link in links:
            href = link['href']
            
            # Match announcement patterns
            if '/beta/offre/' in href or '/beta/annonces_specials/' in href:
                # Extract ID from URL (last number)
                parts = href.strip('/').split('/')
                if parts[-1].isdigit():
                    announcement_id = parts[-1]
                    title = link.get_text(strip=True)
                    
                    # Skip if title is too short (likely not the main title)
                    if len(title) > 10:
                        full_url = urljoin(BETA_URL, href)
                        announcements[announcement_id] = {
                            'title': title,
                            'url': full_url,
                            'first_seen': datetime.now().isoformat()
                        }
        
        print(f"Found {len(announcements)} announcements")
        return announcements
        
    except Exception as e:
        print(f"Error fetching announcements: {e}")
        return None

def load_previous_state():
    """Load the previous state from file"""
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading state: {e}")
    return {}

def save_state(announcements):
    """Save current state to file"""
    try:
        with open(STATE_FILE, 'w', encoding='utf-8') as f:
            json.dump(announcements, f, ensure_ascii=False, indent=2)
        print(f"State saved: {len(announcements)} announcements")
    except Exception as e:
        print(f"Error saving state: {e}")

def send_whatsapp_message(message):
    """Send WhatsApp message using CallMeBot API"""
    if not WHATSAPP_PHONE or not WHATSAPP_API_KEY:
        print("WhatsApp credentials not configured. Message:")
        print(message)
        return False
    
    try:
        # CallMeBot API endpoint
        url = f"https://api.callmebot.com/whatsapp.php"
        params = {
            'phone': WHATSAPP_PHONE,
            'text': message,
            'apikey': WHATSAPP_API_KEY
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            print("✓ WhatsApp message sent successfully")
            return True
        else:
            print(f"Failed to send WhatsApp: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"Error sending WhatsApp: {e}")
        return False

def format_announcement_message(new_announcements):
    """Format new announcements for WhatsApp"""
    count = len(new_announcements)
    
    if count == 0:
        return None
    
    # Build message
    message = f"🔔 *{count} Nouvelle(s) annonce(s) sur beta.mr*\n\n"
    
    # Limit to first 5 to avoid message being too long
    for i, (ann_id, details) in enumerate(list(new_announcements.items())[:5], 1):
        title = details['title'][:80]  # Truncate long titles
        url = details['url']
        message += f"{i}. {title}\n{url}\n\n"
    
    if count > 5:
        message += f"... et {count - 5} autre(s)\n\n"
    
    message += f"Vérifié le: {datetime.now().strftime('%d/%m/%Y à %H:%M')}"
    
    return message

def main():
    """Main monitoring logic"""
    print("=" * 60)
    print("Beta.mr Procurement Monitor")
    print("=" * 60)
    
    # Fetch current announcements
    current = fetch_announcements()
    
    if current is None:
        print("Failed to fetch announcements. Exiting.")
        sys.exit(1)
    
    # Load previous state
    previous = load_previous_state()
    
    # Find new announcements
    new_ids = set(current.keys()) - set(previous.keys())
    
    if new_ids:
        print(f"\n🎯 Found {len(new_ids)} NEW announcement(s)!")
        
        new_announcements = {aid: current[aid] for aid in new_ids}
        
        # Print new announcements
        for ann_id, details in new_announcements.items():
            print(f"  - [{ann_id}] {details['title'][:60]}...")
        
        # Send WhatsApp notification
        message = format_announcement_message(new_announcements)
        if message:
            send_whatsapp_message(message)
    else:
        print("\n✓ No new announcements")
    
    # Save current state
    save_state(current)
    
    print("\n" + "=" * 60)
    print(f"Monitoring complete at {datetime.now()}")
    print("=" * 60)

if __name__ == "__main__":
    main()
