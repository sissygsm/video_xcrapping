#########################################################
# Just need to edit FIREFOX_PROFILE, PC_USER & X_USERNAME
#########################################################

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager

import time
import os

# Create downloads directory if it doesn't exist
DOWNLOADS_DIR = "./downloads"
if not os.path.exists(DOWNLOADS_DIR):
    os.makedirs(DOWNLOADS_DIR)

FIREFOX_PROFILE = 'your_profile_code' + '.default-release'
PC_USER = 'your_user'
X_USERNAME = "your_x_username"  # The @ username

def scrap_links_withFirefox(username):
    # Create user-specific directory
    user_dir = os.path.join(DOWNLOADS_DIR, username)
    if not os.path.exists(user_dir):
        os.makedirs(user_dir)

    # Use your Firefox profile
    profile_path = f"C:\\Users\\{PC_USER}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\{FIREFOX_PROFILE}"
    fp = webdriver.FirefoxProfile(profile_path)
    options = webdriver.FirefoxOptions()
    options.profile = fp

    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)

    url = f"https://x.com/{username}/media"

    driver.get(url)
    time.sleep(5)

    tweet_links = []

    keep_adding = True
    while keep_adding:
        keep_adding = False
        links = driver.find_elements(By.TAG_NAME, "a")
        for link in links:
            href = link.get_attribute("href")
            if href and (f"/{username}/status/" in href) and (href not in tweet_links):
                tweet_links.append(href)
                keep_adding = True

        driver.execute_script("""window.scrollTo(0, document.body.scrollHeight);
                            window.scrollTo(document.body.scrollHeight, 0);
                            window.scrollTo(0, document.body.scrollHeight);
                            """)
        time.sleep(3)

    print(f"\nTotal media tweet links found: {len(tweet_links)}")
    driver.quit()
    return tweet_links


def filter_links(tweet_links):
    # Filter by type (videos only)
    video_links = [link for link in tweet_links if "/video/" in link]
    print(f"\nTotal video tweet links found: {len(video_links)}")
    # Cut the link to only show user + video number
    cleaned_links = [link[:-8] for link in video_links]
    return cleaned_links


def save_pending_links(links, username, file="pending_links.txt"):
    """Save a list of links to a pending file, without duplicates"""
    user_dir = os.path.join(DOWNLOADS_DIR, username)
    file_path = os.path.join(user_dir, file)
    existing = set()
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            existing = set([line.strip() for line in f])
    new_links = [l for l in links if l not in existing]
    with open(file_path, "a") as f:
        for link in new_links:
            f.write(link + "\n")
    print(f"{len(new_links)} new links saved to {file_path}")


x_links = scrap_links_withFirefox(username=X_USERNAME)
video_links_only = filter_links(x_links)
save_pending_links(video_links_only, X_USERNAME)
