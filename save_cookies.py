from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import json

# إعداد Selenium مع وضع المتصفح المرئي
options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

# افتح صفحة تسجيل دخول TikTok
driver.get("https://www.tiktok.com/login")

print("📌 سجل الدخول يدويًا خلال المتصفح اللي فتح...")
print("⏳ بعد تسجيل الدخول، هانتظر 60 ثانية قبل حفظ الكوكيز...")

time.sleep(60)  # استنى عشان تسجل دخول يدوي

# احفظ الكوكيز
cookies = driver.get_cookies()
with open("cookies.json", "w") as f:
    json.dump(cookies, f)

print("✅ تم حفظ الكوكيز في cookies.json")

driver.quit()
