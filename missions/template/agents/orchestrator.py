import subprocess
import os
import sys
from datetime import datetime

class Orchestrator:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # venv is at the root Antigravity/venv, while base_dir is Antigravity/missions/vancouver_port
        self.venv_python = os.path.abspath(os.path.join(self.base_dir, "..", "..", "venv", "bin", "python"))
        
        # Agents
        self.collector_script = os.path.join(self.base_dir, "agents", "collector.py")
        self.cleaner_script = os.path.join(self.base_dir, "agents", "cleaner.py")

    def run_pipeline(self):
        print(f"[{datetime.now()}] Starting Pipeline...")
        
        # Step 1: Collector
        print(f"[{datetime.now()}] Running Collector (Agent 1)...")
        try:
            subprocess.run([self.venv_python, self.collector_script], check=True)
            print("Collector finished successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Collector failed: {e}")
            return

        # Step 2: Cleaner
        print(f"[{datetime.now()}] Running Cleaner (Agent 2)...")
        try:
            subprocess.run([self.venv_python, self.cleaner_script], check=True)
            print("Cleaner finished successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Cleaner failed: {e}")
            return

        print(f"[{datetime.now()}] Pipeline Complete.")
        
        # Step 3: Grading & Notification
        self.grade_data()

    def grade_data(self):
        """Grades the data quality and logs it."""
        processed_file = os.path.join(self.base_dir, "data", "processed", "latest.json")
        try:
            import json
            with open(processed_file, "r") as f:
                data = json.load(f)
            
            count = len(data)
            grade = "F"
            if count > 50: grade = "A+"
            elif count > 20: grade = "A"
            elif count > 10: grade = "B"
            elif count > 0: grade = "C"
            
            print(f"[{datetime.now()}] Data Grading: {grade} ({count} vessels found)")
            
            # Here you could enhance to send an alert if grade is F
            
        except Exception as e:
            print(f"Grading failed: {e}")

if __name__ == "__main__":
    orchestrator = Orchestrator()
    orchestrator.run_pipeline()
