from flask import Flask, render_template, jsonify
import threading

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

def monitor_directory(path):
    change_handle = win32file.FindFirstChangeNotification(
        path,
        0,
        win32con.FILE_NOTIFY_CHANGE_FILE_NAME 
        | win32con.FILE_NOTIFY_CHANGE_DIR_NAME 
        | win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES 
        | win32con.FILE_NOTIFY_CHANGE_SIZE 
        | win32con.FILE_NOTIFY_CHANGE_LAST_WRITE 
        | win32con.FILE_NOTIFY_CHANGE_SECURITY
    )

    try:
        while True:
            result = win32file.WaitForSingleObject(change_handle, 500)
            if result == win32con.WAIT_OBJECT_0:
                # Detect and respond to changes
                alerts.append("Change detected in directory")
                win32file.FindNextChangeNotification(change_handle)
    except KeyboardInterrupt:
        pass
    finally:
        win32file.FindCloseChangeNotification(change_handle)

if __name__ == '__main__':
    threading.Thread(target=start_flask_app).start()
    monitor_directory("C:\\path\\to\\monitor")
