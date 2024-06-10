import win32file
import win32con
import threading
from flask import Flask, render_template, jsonify
import numpy as np
from sklearn.ensemble import RandomForestClassifier

# Flask setup
app = Flask(__name__)
alerts = []

@app.route('/')
def index():
    return render_template('index.html', alerts=alerts)

@app.route('/api/alerts')
def get_alerts():
    return jsonify(alerts)

def start_flask_app():
    app.run(debug=True, use_reloader=False)

# Dummy model for illustration (replace with your trained model)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(np.random.rand(1000, 10), np.random.randint(2, size=1000))

def extract_features(change):
    # Dummy feature extraction (replace with actual logic)
    return np.random.rand(1, 10)

def monitor_directory(path):
    change_handle = win32file.FindFirstChangeNotification(
        path,
        0,
        win32con.FILE_NOTIFY_CHANGE_FILE_NAME | win32con.FILE_NOTIFY_CHANGE_DIR_NAME | win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES | win32con.FILE_NOTIFY_CHANGE_SIZE | win32con.FILE_NOTIFY_CHANGE_LAST_WRITE | win32con.FILE_NOTIFY_CHANGE_SECURITY
    )

    try:
        while True:
            result = win32file.WaitForSingleObject(change_handle, 500)
            if result == win32con.WAIT_OBJECT_0:
                features = extract_features("change event details")
                prediction = model.predict(features)
                
                if prediction == 1:  # If ransomware detected
                    alerts.append("Ransomware activity detected!")
                    # Implement prevention logic here (e.g., blocking access)
                
                win32file.FindNextChangeNotification(change_handle)
    except KeyboardInterrupt:
        pass
    finally:
        win32file.FindCloseChangeNotification(change_handle)

if __name__ == '__main__':
    threading.Thread(target=start_flask_app).start()
    monitor_directory("C:\\Users\\yongj\\Documents")
