import os

def scan_file(file_path, malware_signatures):
    try:
        with open(file_path, 'rb') as file:
            content = file.read()
            for signature in malware_signatures:
                if signature in content:
                    print(f"Malicious file detected: {file_path}")
                    return True
    except Exception as e:
        print(f"Error scanning {file_path}: {e}")
    return False

def scan_directory(directory_path, malware_signatures):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            scan_file(file_path, malware_signatures)

if __name__ == "__main__":
    # Example malware signatures (replace with real signatures)
    malware_signatures = ["malware_signature1", "malware_signature2", "malware_signature3"]

    # Directory to scan (replace with the target directory)
    target_directory = "/path/to/scan"

    print(f"Scanning directory: {target_directory}")
    scan_directory(target_directory, malware_signatures)
    print("Scan complete.")