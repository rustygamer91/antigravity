import os
import sys
import argparse
from flask import render_template

def bake_mission(mission_name):
    # Setup Paths
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    mission_dir = os.path.join(root_dir, "missions", mission_name)
    web_dir = os.path.join(mission_dir, "web")
    
    if not os.path.exists(web_dir):
        print(f"Error: Mission web directory not found at {web_dir}")
        return

    # Add mission web dir to sys.path to import app
    sys.path.append(web_dir)
    
    try:
        from app import app, load_data, generate_intelligence
        
        print(f"Baking mission '{mission_name}'...")
        
        with app.app_context():
            # 1. Load Data
            vessels = load_data()
            print(f"Loaded {len(vessels)} vessels.")
            
            # 2. Run Intelligence
            intel = generate_intelligence(vessels)
            print(f"Generated {len(intel)} insights.")
            
            # 3. Render Template
            # We assume the template is 'dashboard.html' as per standard Antigravity structure
            html_content = render_template('dashboard.html', vessels=vessels, intelligence=intel)
            
            # 4. Save to Output
            output_dir = os.path.join(mission_dir, "output")
            os.makedirs(output_dir, exist_ok=True)
            output_file = os.path.join(output_dir, "index.html")
            
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(html_content)
                
            print(f"✅ Success! Dashboard baked to: {output_file}")
            print(f"You can now share this file or upload it to any static host.")
            
    except ImportError as e:
        print(f"Error importing app from {web_dir}: {e}")
    except Exception as e:
        print(f"Error baking dashboard: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bake Antigravity Mission to Static HTML")
    parser.add_argument("name", help="Name of the mission (e.g., vancouver_port)")
    args = parser.parse_args()
    
    bake_mission(args.name)
