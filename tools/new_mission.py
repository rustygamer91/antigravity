import os
import shutil
import sys
import argparse

def create_mission(mission_name):
    # Paths
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    template_dir = os.path.join(root_dir, "missions", "template")
    mission_dir = os.path.join(root_dir, "missions", mission_name)
    
    if os.path.exists(mission_dir):
        print(f"Error: Mission '{mission_name}' already exists.")
        return

    # If template doesn't exist, we use vancouver_port as a fallback source (or we should have created a template)
    # For now, let's assume we will create a 'template' folder next. 
    # Or we can copy from vancouver_port and clean it up (a bit hacky but works for "reuse").
    # Let's demand a template exists.
    if not os.path.exists(template_dir):
        print(f"Error: Template directory not found at {template_dir}")
        print("Please ensure the framework is fully set up.")
        return

    print(f"Creating mission '{mission_name}'...")
    shutil.copytree(template_dir, mission_dir)
    
    print(f"Mission '{mission_name}' created successfully at missions/{mission_name}")
    print("\nNext steps:")
    print(f"1. cd missions/{mission_name}")
    print("2. Review agents/collector.py to set your data source.")
    print("3. ./venv/bin/python web/app.py (Adjust path to venv as needed)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scaffold a new Antigravity Mission")
    parser.add_argument("name", help="Name of the new mission (e.g., crypto_tracker)")
    args = parser.parse_args()
    
    create_mission(args.name)
