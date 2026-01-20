# 🌌 Antigravity: Agentic Intelligence Framework

Welcome to **Antigravity**. This is a modular framework for building **AI Agents** that monitor the world, extract intelligence, and present it in a beautiful glassmorphism dashboard.

## 🚀 Quick Start (For your Friend)

### 1. Prerequisities
You need Python installed.
```bash
# Clone or Unzip this repository
cd Antigravity

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
playwright install chromium
```

---

## 🚢 Mission 1: Vancouver Port Watcher
This mission is already built and active. It monitors vessel traffic, detects congestion, and identifies market leaders.

**To Run:**
```bash
./venv/bin/python missions/vancouver_port/web/app.py
```
*Access the dashboard at: `http://localhost:8080`*

---

## 📱 How to Use on Mobile
Since the dashboard runs on your laptop, you can't open `localhost` on your phone directly.

**Option A: The Easy Way (Ngrok)**
1.  Install [ngrok](https://ngrok.com/).
2.  Run the dashboard in one terminal (step above).
3.  In a new terminal, run:
    ```bash
    ngrok http 8080
    ```
4.  Ngrok will give you a link (e.g., `https://random-name.ngrok-free.app`). Send that to your phone!

**Option B: Local WiFi**
1.  Find your laptop's local IP (e.g., `192.168.1.5`).
2.  Modify `web/app.py` to run with `host='0.0.0.0'`.
3.  Open `http://192.168.1.5:8080` on your phone.

---

## 🛠 Create a New Mission (Daily Problem Solving)
Want to solve a new problem like "Crypto Arbitrage" or "SF Housing"?

1.  **Run the Factory Tool:**
    ```bash
    python tools/new_mission.py crypto_tracker
    ```
    *This creates a new folder `missions/crypto_tracker` with a full working Skeleton (Agents + Dashboard).*

2.  **Edit the Agent:**
    -   Go to `missions/crypto_tracker/agents/collector.py`.
    -   Change the `url` to your new data source (e.g., CoinGecko).

3.  **Run your New Mission:**
    ```bash
    ./venv/bin/python missions/crypto_tracker/web/app.py
    ```

## 🎁 Share a Static/Zero-Gravity Dashboard
Want to send the dashboard to a friend **without** them needing Python?

1.  **Bake the Dashboard:**
    ```bash
    ./venv/bin/python tools/bake.py vancouver_port
    ```
2.  **Send the File:**
    -   Go to `missions/vancouver_port/output/index.html`.
    -   Email/Direct Message this file.
    -   Or upload it to your website/S3. It works standalone!

## 🤖 Automate it for Free (GitHub Actions)
You mentioned wanting a **Dynamic Dashboard** updated by a **Daily Cron Job** for **Free**.
I have included a `.github/workflows/daily_mission.yml` file that does exactly this.

**To Enable:**
1.  Push this code to a GitHub Repository.
2.  Go to **Settings > Pages**.
3.  Set Source to `gh-pages` branch.

**The Result:**
-   Every day at 8:00 AM, GitHub will wake up.
-   It will run the collector, clean the data, and bake the dashboard.
-   It will deploy the result to `https://<your-username>.github.io/Antigravity`.
-   **Cost: $0.**

## 📂 Project Structure
-   `missions/` - Where your solutions live.
    -   `vancouver_port/` (The original)
    -   `template/` (The blueprint)
-   `tools/` - Utilities like `new_mission.py`.
-   `data/` - (Legacy/Shared data paths).
