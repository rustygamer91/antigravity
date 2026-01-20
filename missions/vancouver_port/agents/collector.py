import os
import time
from datetime import datetime
from playwright.sync_api import sync_playwright

class PPACollector:
    def __init__(self):
        self.url = "https://ppaportal.portlink.co/mt-tm"
        # Ensure we write to the correct data/raw directory relative to the project root
        # Assuming script is in agents/ and data is in data/
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.data_dir = os.path.join(base_dir, "data", "raw")
        os.makedirs(self.data_dir, exist_ok=True)

    def fetch_assignments(self):
        """Fetches the vessel traffic data from PPA portal using Playwright."""
        print(f"[{datetime.now()}] Starting collection from {self.url}...")
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            try:
                page.goto(self.url, timeout=60000)
                # Wait for the grid to load
                page.wait_for_selector(".k-grid-content", timeout=30000)
                
                # Give it a moment for rows to populate
                time.sleep(5) 
                
                content = page.content()
                
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"traffic_{timestamp}.html"
                filepath = os.path.join(self.data_dir, filename)
                
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)
                
                print(f"[{datetime.now()}] Data saved to {filepath}")
                return filepath
                
            except Exception as e:
                print(f"Error fetching data: {e}")
                return None
            finally:
                browser.close()

if __name__ == "__main__":
    collector = PPACollector()
    collector.fetch_assignments()
