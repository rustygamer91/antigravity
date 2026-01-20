import json
import os
import glob
from bs4 import BeautifulSoup
from datetime import datetime

class DataCleaner:
    def __init__(self):
        # Determine paths relative to this script
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.raw_dir = os.path.join(base_dir, "data", "raw")
        self.processed_dir = os.path.join(base_dir, "data", "processed")
        os.makedirs(self.processed_dir, exist_ok=True)

    def get_latest_file(self):
        files = glob.glob(os.path.join(self.raw_dir, "*.html"))
        if not files:
            return None
        return max(files, key=os.path.getctime)

    def clean_data(self, file_path=None):
        """Cleans and extracts data from raw HTML."""
        if not file_path:
            file_path = self.get_latest_file()
            if not file_path:
                print("No raw files found.")
                return

        print(f"Processing {file_path}...")
        
        with open(file_path, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        # Find the rows in the grid
        # Kendo grids often have multiple tables (header vs content). 
        # We want the content table usually in .k-grid-content
        rows = soup.select(".k-grid-content table tbody tr")
        
        cleaned_data = []
        
        for row in rows:
            cells = row.find_all("td")
            if not cells:
                continue
                
            # Mapping based on observation
            # 0: Status
            # 1: Order Time
            # 2: Vessel Name
            # 3: ETD
            # 4: ETA
            # 5: From
            # 6: To
            # 7: Ordering Agency
            # 8: Billing Agency
            
            try:
                entry = {
                    "status": cells[0].get_text(strip=True),
                    "order_time": cells[1].get_text(strip=True),
                    "vessel_name": cells[2].get_text(strip=True),
                    "etd": cells[3].get_text(strip=True),
                    "eta": cells[4].get_text(strip=True),
                    "location_from": cells[5].get_text(strip=True),
                    "location_to": cells[6].get_text(strip=True),
                    "agency": cells[7].get_text(strip=True),
                    "flag": cells[13].get_text(strip=True) if len(cells) > 13 else ""
                }
                cleaned_data.append(entry)
            except IndexError:
                continue

        output_path = os.path.join(self.processed_dir, "latest.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(cleaned_data, f, indent=4)
        
        print(f"Saved {len(cleaned_data)} entries to {output_path}")
        return output_path

if __name__ == "__main__":
    cleaner = DataCleaner()
    cleaner.clean_data()
