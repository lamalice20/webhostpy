import http.server as server
import socketserver as socket
import os
import argparse
import os
import sys
import requests
import zipfile
import shutil


# Configuration
GITHUB_OWNER = "lamalice20"
GITHUB_REPO = "webhostpy"
DOWNLOAD_PATH = "C:\\webhostpy\\UpdateFolder\\.update.zip"
EXTRACT_PATH = "C:\\webhostpy\\UpdateFolder\\update_temp"


def get_latest_release():
    """Fetch the latest release from GitHub API."""
    url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/releases/latest"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        zip_url = data["zipball_url"]
        return zip_url
    else:
        print("Failed to fetch the latest release.")
        return None

def download_and_extract(zip_url):
    """Download the latest release and extract it."""
    response = requests.get(zip_url, stream=True)
    if response.status_code == 200:
        with open(DOWNLOAD_PATH, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        
        print("Download complete. Extracting files...")
        with zipfile.ZipFile(DOWNLOAD_PATH, "r") as zip_ref:
            zip_ref.extractall(EXTRACT_PATH)
        
        os.remove(DOWNLOAD_PATH)  # Clean up zip file
        print("Extraction complete.")
        return True
    else:
        print("Failed to download the update.")
        return False

def replace_old_files():
    """Replace old files with the new version."""
    # Find the extracted folder (GitHub names it dynamically)
    extracted_folders = os.listdir(EXTRACT_PATH)
    if len(extracted_folders) == 1:
        update_folder = os.path.join(EXTRACT_PATH, extracted_folders[0])

        for item in os.listdir(update_folder):
            s = os.path.join(update_folder, item)
            d = os.path.join(os.getcwd(), item)

            if os.path.isdir(s):
                if os.path.exists(d):
                    shutil.rmtree(d)
                shutil.copytree(s, d)
            else:
                shutil.copy2(s, d)

        shutil.rmtree(EXTRACT_PATH)  # Clean up extracted files
        print("Update applied successfully.")
    else:
        print("Error: Unexpected folder structure in update.")


# create function to start server 
def start_server():
    # Ask for the server port
    port = int(input('Enter the server port: '))

    # Ask for the server host
    host = input('Enter the server host: ')

    # Define the server address
    address = (host, port)

    # Create a function to handle http requests
    handler = server.SimpleHTTPRequestHandler

    # Create a function to respond and start
    resp = socket.TCPServer(address, handler)

    # Execute the server start
    try:
        os.system("cls")
        print(f'Server opened the link : http://{host}:{port}/')
        resp.serve_forever()
    except KeyboardInterrupt:
        print('Server closed')
        
# Create the parser for look if have --{command} in the start command

parse = argparse.ArgumentParser()

parse.add_argument("--start", action="store_true", help="Startup command for the server")
parse.add_argument("--update", action="store_true", help="update oldest files to the latest files")
args = parse.parse_args()

if args.start:
    start_server()

if args.update:
    print("Checking for updates...")
    zip_url = get_latest_release()
    if zip_url and download_and_extract(zip_url):
        replace_old_files()
        print("Update complete. Exiting application.")
        sys.exit(0)  # Quitte proprement après la mise à jour
