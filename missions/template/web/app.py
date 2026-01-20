import os
import json
from flask import Flask, render_template

app = Flask(__name__)

# Determine paths relative to this script
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "latest.json")

def load_data():
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

from datetime import datetime, timedelta

def generate_intelligence(vessels):
    insights = []
    
    # 1. Congestion Analysis
    location_counts = {}
    location_vessels = {} 
    
    for v in vessels:
        loc = v.get('location_to', 'Unknown')
        location_counts[loc] = location_counts.get(loc, 0) + 1
        if loc not in location_vessels: location_vessels[loc] = []
        location_vessels[loc].append(v.get('vessel_name', 'Unknown'))
    
    # Sort locations by count
    sorted_locs = sorted(location_counts.items(), key=lambda x: x[1], reverse=True)
    if sorted_locs:
        top_loc, count = sorted_locs[0]
        if count >= 3:
            # Evidence: Get names of vessels at this location
            proof_list = location_vessels.get(top_loc, [])[:3] 
            insights.append({
                "type": "congestion",
                "icon": "⚠️",
                "title": "Congestion Alert",
                "message": f"{top_loc} is experiencing heavy traffic with <strong style='color:white'>{count} vessels</strong> scheduled.",
                "color": "#f59e0b",
                "proof": proof_list # ["Vessel A", "Vessel B"...]
            })

    # 2. Market Dominance
    agency_counts = {}
    total_vessels = len(vessels)
    if total_vessels > 0:
        for v in vessels:
            agency = v.get('agency', 'Unknown')
            agency_counts[agency] = agency_counts.get(agency, 0) + 1
        
        sorted_agencies = sorted(agency_counts.items(), key=lambda x: x[1], reverse=True)
        if sorted_agencies:
            top_agency, count = sorted_agencies[0]
            share = round((count / total_vessels) * 100)
            
            # Evidence: Top 3 agencies for context
            proof_stats = [f"{k}: {v}" for k, v in sorted_agencies[:3]]
            
            insights.append({
                "type": "market",
                "icon": "ℹ️",
                "title": "Market Leader",
                "message": f"{top_agency} is managing <strong style='color:white'>{share}%</strong> of active port traffic ({count} vessels).",
                "color": "#38bdf8",
                "proof": proof_stats
            })

    # 3. Operational Pulse (Arrivals in 24h)
    arrivals_24h = []
    now = datetime.now()
    for v in vessels:
        eta_str = v.get('eta', '')
        if eta_str:
            try:
                # Format: DD/MM/YYYY HH:MM
                eta_dt = datetime.strptime(eta_str, "%d/%m/%Y %H:%M")
                if 0 <= (eta_dt - now).total_seconds() <= 86400: # 24 hours
                    arrivals_24h.append(f"{v.get('vessel_name')} ({eta_dt.strftime('%H:%M')})")
            except ValueError:
                continue
                
    if len(arrivals_24h) > 5:
        insights.append({
            "type": "surge",
            "icon": "⚡",
            "title": "High Activity",
            "message": f"Surge in arrivals: <strong style='color:white'>{len(arrivals_24h)} vessels</strong> expected in the next 24 hours.",
            "color": "#10b981",
            "proof": arrivals_24h[:4] # Show first 4
        })
    else:
        insights.append({
            "type": "steady",
            "icon": "✅",
            "title": "Steady Operations",
            "message": f"Port flow is normal with {len(arrivals_24h)} arrivals in 24h.",
            "color": "#94a3b8",
            "proof": arrivals_24h if arrivals_24h else ["No immediate arrivals"]
        })

    return insights

@app.route('/')
def dashboard():
    vessels = load_data()
    intelligence = generate_intelligence(vessels)
    return render_template('dashboard.html', vessels=vessels, intelligence=intelligence)

if __name__ == '__main__':
    # Run slightly differently to allow external access if needed, or just default
    # Port 5000/5001 might be taken or blocked. Using 8080.
    app.run(debug=True, port=8080)
