
import os
from flask import Flask, render_template, request, jsonify
from datetime import datetime

# Set explicit template and static folder paths relative to app.py
base_dir = os.path.abspath(os.path.dirname(__file__))
app = Flask(
    __name__,
    template_folder=os.path.join(base_dir, 'templates'),
    static_folder=os.path.join(base_dir, 'static')
)

# Temporary in-memory database store
user_data = {
    "water_logs": [],           # Historical water logs with timestamps
    "sleep_logs": [],           # Historical sleep logs with timestamps
    "mood_logs": [],            # Mood entries with timestamps
    "journal_entries": []       # Journal entries with timestamps
}

# ==========================================
# Page Routes (Template Rendering)
# ==========================================

@app.route('/')
def home():
    """Landing / Welcome page (Bloom.html)"""
    return render_template('Bloom.html')

@app.route('/questions')
def questions():
    """Onboarding questions page (questions.html)"""
    return render_template('questions.html')

@app.route('/dashboard')
def dashboard():
    """Main interactive plant dashboard (dashboard.html)"""
    return render_template('dashboard.html')

@app.route('/hydration')
def hydration():
    """Hydration tracker module (hydration.html)"""
    current_water = sum(log['glasses'] for log in user_data["water_logs"] if log['date'] == datetime.now().strftime('%Y-%m-%d'))
    return render_template('hydration.html', water=current_water, logs=user_data["water_logs"])

@app.route('/sleeptracker')
def sleeptracker():
    """Sleep tracker module (sleeptracker.html)"""
    today_logs = [log for log in user_data["sleep_logs"] if log['date'] == datetime.now().strftime('%Y-%m-%d')]
    current_sleep = today_logs[0]['hours'] if today_logs else 0
    return render_template('sleeptracker.html', sleep=current_sleep, logs=user_data["sleep_logs"])

@app.route('/mood')
def mood():
    """Mood tracker module (mood.html)"""
    return render_template('mood.html')

@app.route('/breather')
def breather():
    """Breathing exercise module (breather.html)"""
    return render_template('breather.html')

@app.route('/journal')
def journal():
    """Plant journal module (journal.html)"""
    return render_template('journal.html', entries=user_data["journal_entries"])

@app.route('/metrics')
def metrics():
    """Metrics dashboard showing all logged data"""
    return render_template('metrics.html', 
                          water_logs=user_data["water_logs"],
                          sleep_logs=user_data["sleep_logs"],
                          mood_logs=user_data["mood_logs"],
                          journal_entries=user_data["journal_entries"])


# ==========================================
# API Endpoints (Handling Frontend POST Data)
# ==========================================

@app.route('/api/water', methods=['POST'])
def save_water():
    data = request.get_json() or {}
    glasses = data.get('glasses', 0)
    water_entry = {
        'glasses': glasses,
        'date': datetime.now().strftime('%Y-%m-%d'),
        'time': datetime.now().strftime('%H:%M:%S'),
        'timestamp': datetime.now().isoformat()
    }
    user_data["water_logs"].append(water_entry)
    total_today = sum(log['glasses'] for log in user_data["water_logs"] if log['date'] == water_entry['date'])
    return jsonify({"status": "success", "water": total_today, "logs": user_data["water_logs"]})

@app.route('/api/sleep', methods=['POST'])
def save_sleep():
    data = request.get_json() or {}
    hours = data.get('hours', 0)
    sleep_entry = {
        'hours': hours,
        'date': datetime.now().strftime('%Y-%m-%d'),
        'time': datetime.now().strftime('%H:%M:%S'),
        'timestamp': datetime.now().isoformat()
    }
    user_data["sleep_logs"].append(sleep_entry)
    return jsonify({"status": "success", "sleep": hours, "logs": user_data["sleep_logs"]})

@app.route('/api/mood', methods=['POST'])
def save_mood():
    data = request.get_json() or {}
    if data.get('mood'):
        mood_entry = {
            'mood': data.get('mood'),
            'note': data.get('note', ''),
            'date': datetime.now().strftime('%Y-%m-%d'),
            'time': datetime.now().strftime('%H:%M:%S'),
            'timestamp': datetime.now().isoformat()
        }
        user_data["mood_logs"].append(mood_entry)
    return jsonify({"status": "success", "total_logs": len(user_data["mood_logs"])})

@app.route('/api/journal', methods=['POST'])
def save_journal():
    data = request.get_json() or {}
    text = data.get('text', '').strip()
    if text:
        journal_entry = {
            'text': text,
            'date': datetime.now().strftime('%Y-%m-%d'),
            'time': datetime.now().strftime('%H:%M:%S'),
            'timestamp': datetime.now().isoformat()
        }
        user_data["journal_entries"].insert(0, journal_entry)
        return jsonify({"status": "success", "entries": user_data["journal_entries"]})
    return jsonify({"status": "error", "message": "Entry cannot be empty"}), 400


# ==========================================
# App Execution
# ==========================================
if __name__ == '__main__':
    # Local development server: http://127.0.0.1:5000/
    app.run(debug=True)