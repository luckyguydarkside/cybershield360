import os
import hashlib
import time

# Function to compute the hash of a file
def hash_file(filepath):
    """Generate SHA256 hash of the file."""
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        # Read file in chunks to avoid memory overload
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

# Function to monitor a directory for changes
def monitor_directory(target_dir):
    """Monitor a directory for file changes."""
    file_hashes = {}
    
    while True:
        for filename in os.listdir(target_dir):
            filepath = os.path.join(target_dir, filename)
            if os.path.isfile(filepath):
                current_hash = hash_file(filepath)
                if filename in file_hashes:
                    if file_hashes[filename] != current_hash:
                        print(f"Change detected: {filename}")
                else:
                    print(f"New file added: {filename}")
                file_hashes[filename] = current_hash
        
        # Check for deleted files
        for filename in list(file_hashes.keys()):
            if filename not in os.listdir(target_dir):
                print(f"File removed: {filename}")
                del file_hashes[filename]
        
        # Sleep for a while before checking again
        time.sleep(10)

# Set the directory to monitor
target_directory = '/path/to/monitor'
monitor_directory(target_directory)