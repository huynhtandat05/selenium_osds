import time
import getpass
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

# ============================
# 1. CẤU HÌNH TRÌNH DUYỆT
# ============================
options = Options()
options.add_argument("--disable-notifications")
driver = webdriver.Chrome(options=options)
driver.maximize_window()

# ============================
# 2. ĐĂNG NHẬP FACEBOOK
# ============================
driver.get("https://www.facebook.com/")
time.sleep(2)

email = input("👉 Nhập Email: ")
password = getpass.getpass("👉 Nhập Mật khẩu: ")

driver.find_element(By.ID, "email").send_keys(email)
pwd_field = driver.find_element(By.ID, "pass")
pwd_field.send_keys(password)
pwd_field.send_keys(Keys.ENTER)

print("🔑 Đang đăng nhập... vui lòng chờ 10 giây.")
time.sleep(10)

# ============================
# 3. CUỘN TRANG ĐỂ LOAD BÀI VIẾT
# ============================
print("📜 Đang cuộn trang để tải thêm bài viết...")

for i in range(5):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    print(f"--> Đã cuộn lần {i+1}")
    time.sleep(3)

# ============================
# 4. THU THẬP BÀI VIẾT
# ============================
print("📥 Bắt đầu thu thập bài viết...")

posts = driver.find_elements(By.XPATH, "//div[@role='article']")
print(f"🔎 Tìm thấy {len(posts)} bài viết.")

data = []

for p in posts:
    try:
        # Người đăng
        try:
            author = p.find_element(By.XPATH, ".//h2//span").text
        except:
            author = "Không rõ"

        if not author.strip():
            continue

        # Nội dung
        try:
            content = p.find_element(By.XPATH, ".//div[@dir='auto']").text.strip()
        except:
            content = "Không có nội dung"

        # Thống kê (like, comment, share)
        stats = []
        try:
            for s in p.find_elements(By.XPATH, ".//span"):
                txt = s.text.strip()
                if txt and any(k in txt for k in ["Thích", "Bình luận", "Chia sẻ"]):
                    stats.append(txt)
        except:
            pass

        data.append({
            "Người đăng": author,
            "Nội dung": content,
            "Thống kê": ", ".join(stats)
        })

        print(f"✅ Lấy bài viết từ: {author}")

    except Exception as e:
        print("⚠️ Lỗi khi xử lý bài viết:", e)

# ============================
# 5. LƯU FILE EXCEL
# ============================
if data:
    df = pd.DataFrame(data)
    df.to_excel("Facebook_Posts.xlsx", index=False)
    print("\n💾 Đã lưu dữ liệu vào file: Facebook_Posts.xlsx")
else:
    print("❌ Không có dữ liệu nào được thu thập.")

driver.quit()
