import win32file
import win32con

# Monitor directory for changes
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
                # Detect and respond to changes
                print("Change detected in directory")
                win32file.FindNextChangeNotification(change_handle)
    except KeyboardInterrupt:
        pass
    finally:
        win32file.FindCloseChangeNotification(change_handle)

# Start monitoring
monitor_directory("C:\\Users\\yongj")
