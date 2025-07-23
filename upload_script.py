import instaloader
import os
import random
import shutil

# إنشاء فولدر للتخزين المؤقت
DOWNLOAD_DIR = "downloads"
if os.path.exists(DOWNLOAD_DIR):
    shutil.rmtree(DOWNLOAD_DIR)
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# الصفحات المطلوبة
profiles = [
    "o_criminal_09",
    "cars_.1m",
    "v8.gallery",
    "xmax_e_d_i_t",
    "full_throttlemedia",
    "grozny_mka"
]

# تحميل الفيديوهات
L = instaloader.Instaloader(dirname_pattern=DOWNLOAD_DIR + "/{profile}",
                             download_videos=True,
                             download_video_thumbnails=False,
                             download_comments=False,
                             post_metadata_txt_pattern="",
                             save_metadata=False)

for profile_name in profiles:
    print(f"🔄 جاري تحميل المشاركات من {profile_name}...")
    posts = instaloader.Profile.from_username(L.context, profile_name).get_posts()
    
    # جمع كل الفيديوهات
    video_posts = [post for post in posts if post.is_video]
    random.shuffle(video_posts)
    
    selected = video_posts[:2]  # ناخد 2 فقط عشوائي
    
    for i, post in enumerate(selected):
        print(f"⬇️ تحميل الفيديو {i+1} من {profile_name}")
        try:
            L.download_post(post, target=profile_name)
        except Exception as e:
            print(f"❌ فشل تحميل الفيديو من {profile_name}: {e}")

print("✅ تم تحميل كل الفيديوهات.")
