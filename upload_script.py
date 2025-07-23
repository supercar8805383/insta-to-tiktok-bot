import os
import time
import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

VIDEO_FOLDER = "videos"
COOKIES_FILE = "tiktok_cookies.pkl"

def get_videos_to_upload():
    videos = []
    for file in os.listdir(VIDEO_FOLDER):
        if file.endswith(".mp4"):
            base_name = file[:-4]
            txt_file = f"{base_name}.txt"
            txt_path = os.path.join(VIDEO_FOLDER, txt_file)
            caption = ""
            if os.path.exists(txt_path):
                with open(txt_path, "r", encoding="utf-8") as f:
                    caption = f.read().strip()
            videos.append((os.path.join(VIDEO_FOLDER, file), caption))
    return videos

def setup_browser():
    options = Options()
    options.add_argument("--headless=new")  # احذف السطر ده لو عاوز تشوف المتصفح قدامك
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.tiktok.com/upload")

    # تحميل الكوكيز
    if os.path.exists(COOKIES_FILE):
        with open(COOKIES_FILE, "rb") as f:
            cookies = pickle.load(f)
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.get("https://www.tiktok.com/upload")
        time.sleep(5)
    else:
        print("❌ ملف الكوكيز غير موجود!")
        driver.quit()
        exit()

    return driver

def upload_video(driver, video_path, caption):
    print(f"⬆️ رفع الفيديو: {video_path}")
    upload_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//input[@type="file"]'))
    )
    upload_input.send_keys(os.path.abspath(video_path))

    print("📝 وضع الوصف...")
    caption_box = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, '//div[contains(@data-e2e,"caption")]'))
    )
    caption_box.click()
    time.sleep(1)
    caption_box.send_keys(Keys.CONTROL, 'a')  # تحديد الكل
    caption_box.send_keys(Keys.BACKSPACE)
    caption_box.send_keys(caption)

    print("✅ نشر الفيديو...")
    post_button = WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((By.XPATH, '//button[contains(@data-e2e,"post-button")]'))
    )
    post_button.click()

    print("⌛️ انتظار الانتهاء...")
    time.sleep(15)  # انتظر شوية لحد ما الفيديو يترفع

    print("🗑 حذف الفيديو بعد الرفع...")
    os.remove(video_path)
    txt_path = video_path.replace(".mp4", ".txt")
    if os.path.exists(txt_path):
        os.remove(txt_path)

def main():
    videos = get_videos_to_upload()
    if not videos:
        print("📭 لا يوجد فيديوهات للرفع.")
        return

    driver = setup_browser()

    for video_path, caption in videos:
        upload_video(driver, video_path, caption)

    driver.quit()
    print("🚀 تم رفع كل الفيديوهات بنجاح!")

if __name__ == "__main__":
    main()
