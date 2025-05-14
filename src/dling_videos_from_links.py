#########################################################
# Just need to edit FIREFOX_PROFILE & X_USERNAME
#########################################################

from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError

import time
import os
import sys

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

    while links:
        link = links.pop()
        video_id = link.split("/")[-1] # Get the digits from the link
        output_path = os.path.join(user_dir, f"{video_id}.%(ext)s")

        ydl_opts = {
            'cookiesfrombrowser': ('firefox', FIREFOX_PROFILE),
            'outtmpl': output_path,
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4',
            'noplaylist': True
        }
        print()
        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([link])
        except DownloadError as e:
            print(f"Error downloading {link}: {e}")
            links.append(link)
            with open(file_path, "w") as f:
                f.write("\n".join(links) + "\n")
            print("❌ Download stopped due to error. Watch your downloads while you wait...")
            return

    if os.path.exists(file_path):
        os.remove(file_path) 


download_pending_links(username=X_USERNAME)
