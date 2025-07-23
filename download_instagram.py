import os
import random
import requests
from bs4 import BeautifulSoup

INSTAGRAM_ACCOUNTS = [
    "https://www.instagram.com/o_criminal_09",
    "https://www.instagram.com/cars_.1m",
    "https://www.instagram.com/v8.gallery",
    "https://www.instagram.com/xmax_e_d_i_t",
    "https://www.instagram.com/full_throttlemedia",
    "https://www.instagram.com/grozny_mka"
]

OUTPUT_DIR = "videos"
os.makedirs(OUTPUT_DIR, exist_ok=True)

headers = {
    "User-Agent": "Mozilla/5.0"
}

def get_video_links(profile_url):
    res = requests.get(profile_url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    scripts = soup.find_all("script")
    for script in scripts:
        if "window._sharedData" in script.text:
            shared_data = script.string.split("= ", 1)[1].rstrip(";")
            break
    else:
        print(f"❌ No shared data found in {profile_url}")
        return []

    import json
    data = json.loads(shared_data)
    posts = data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges']

    video_links = []
    for post in posts:
        node = post["node"]
        if node["is_video"]:
            shortcode = node["shortcode"]
            video_links.append(f"https://www.instagram.com/p/{shortcode}/")

    return video_links

def download_video(video_url, filename):
    try:
        from yt_dlp import YoutubeDL
    except ImportError:
        print("❌ Please install yt_dlp: pip install yt_dlp")
        return

    ydl_opts = {
        'outtmpl': os.path.join(OUTPUT_DIR, filename),
        'quiet': True,
        'format': 'mp4',
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

# تحميل 2 فيديو عشوائي من كل حساب
for profile_url in INSTAGRAM_ACCOUNTS:
    print(f"📥 Fetching from {profile_url}")
    links = get_video_links(profile_url)
    selected = random.sample(links, min(2, len(links)))
    for i, video_link in enumerate(selected):
        filename = f"{profile_url.split('/')[-2]}_{i}.mp4"
        print(f"🎬 Downloading {video_link} → {filename}")
        download_video(video_link, filename)
