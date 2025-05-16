#########################################################
# Just need to edit FIREFOX_PROFILE & X_USERNAME
#########################################################

from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError

import time
import os

# Create downloads directory if it doesn't exist
DOWNLOADS_DIR = "./downloads"
if not os.path.exists(DOWNLOADS_DIR):
    os.makedirs(DOWNLOADS_DIR)

FIREFOX_PROFILE = 'your_profile_code' + '.default-release'
X_USERNAME = "your_x_username"  # The @ username


def download_pending_links(username, file="pending_links.txt"):
    user_dir = os.path.join(DOWNLOADS_DIR, username)
    file_path = os.path.join(user_dir, file)

    links = []
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            links = [line.strip() for line in f]

    # Get the url id number to name the mp4 file
    output_path = os.path.join(user_dir, f'%(original_url.-19:)s.%(ext)s')
    ydl_opts = {
        'cookiesfrombrowser': ('firefox', FIREFOX_PROFILE),
        'outtmpl': output_path,
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
        'noplaylist': True
    }
    BATCH_SIZE = 50  # X/Twitter Rate-limit links to download 
    while links:
        len_batch = min(BATCH_SIZE, len(links))
        batch = [links.pop() for _ in range(len_batch)]
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download(batch)
        
        with open(file_path, "w") as f:
            f.write("\n".join(links) + "\n")
            
        if links is []:
            print(f"All batchs downloaded.")
            break
        print(f"Batch downloaded. Rate-limit exceeded -> Wait 10 min or end script")
        time.sleep(600)  # 10min = 600seg

    if os.path.exists(file_path):
        os.remove(file_path)


download_pending_links(username=X_USERNAME)
