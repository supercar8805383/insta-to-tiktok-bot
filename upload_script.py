import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# إعداد Selenium
options = Options()
options.add_argument("--headless")  # لو عايز تشوف المتصفح شيل السطر ده
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=options)

# فتح TikTok
driver.get("https://www.tiktok.com/")

# تحميل الكوكيز من ملف cookies.json
with open("cookies.json", "r") as f:
    cookies = json.load(f)

# إضافة الكوكيز للمتصفح
for cookie in cookies:
    driver.add_cookie({
        "name": cookie["name"],
        "value": cookie["value"],
        "domain": cookie["domain"],
        "path": cookie.get("path", "/")
    })

# تحديث الصفحة بعد إضافة الكوكيز
driver.get("https://www.tiktok.com/upload")

time.sleep(10)  # وقت كافي لتحميل صفحة الرفع

print("✅ تم تسجيل الدخول وجاهز للرفع")

driver.quit()
