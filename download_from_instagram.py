import os
import random
import json
import instaloader

# أنشئ مجلد للفيديوهات لو مش موجود
os.makedirs("videos", exist_ok=True)

# حسابات إنستجرام اللي عاوزين نسحب منها
accounts = [
    "o_criminal_09",
    "cars_.1m",
    "v8.gallery",
    "xmax_e_d_i_t",
    "full_throttlemedia",
    "grozny_mka"
]

# تحميل الكوكيز من ملف JSON
L = instaloader.Instaloader(
    download_video_thumbnails=False,
    save_metadata=False,
    download_comments=False,
    post_metadata_txt_pattern=""
)

cookies_path = "instagram_cookies.json"
if os.path.exists(cookies_path):
    with open(cookies_path, "r") as f:
        cookies = json.load(f)

    session = L.context._session
    for cookie in cookies:
        session.cookies.set(
            name=cookie["name"],
            value=cookie["value"],
            domain=cookie["domain"],
            path=cookie["path"]
        )
    print("🔐 تم تحميل الكوكيز بنجاح.")
else:
    print("🚫 ملف الكوكيز مش موجود.")
    exit()

# تحميل الفيديوهات
for username in accounts:
    print(f"\n🔍 جاري التحميل من: {username}")
    try:
        profile = instaloader.Profile.from_username(L.context, username)
        posts = list(profile.get_posts())
        video_posts = [post for post in posts if post.is_video]

        if len(video_posts) < 2:
            print(f"❌ مش لاقي فيديوهات كفاية عند: {username}")
            continue

        selected_posts = random.sample(video_posts, 2)

        for i, post in enumerate(selected_posts):
            print(f"⬇️ تحميل فيديو {i+1} من {username}")
            L.download_post(post, target="videos")

            # إعادة التسمية
            for file in os.listdir("videos"):
                if file.endswith(".mp4") and username in file:
                    new_name = f"{username}_{i+1}.mp4"
                    os.rename(f"videos/{file}", f"videos/{new_name}")
                if file.endswith(".txt") and username in file:
                    new_txt = f"{username}_{i+1}.txt"
                    os.rename(f"videos/{file}", f"videos/{new_txt}")

    except Exception as e:
        print(f"🚨 خطأ مع {username}: {e}")

print("\n✅ تم تحميل الفيديوهات بنجاح.")

# عرض الفيديوهات
print("\n📂 محتوى مجلد الفيديوهات:")
video_folder = "videos"
if os.path.exists(video_folder):
    files = os.listdir(video_folder)
    for f in files:
        print("🟢", f)
else:
    print("🚫 مجلد الفيديوهات مش موجود")
