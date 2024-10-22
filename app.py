from flask import Flask, request, jsonify, render_template
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

app = Flask(__name__)

# إعداد Selenium
chrome_options = Options()
chrome_options.add_argument("--headless")  # تشغيل Chrome بدون واجهة رسومية
service = Service('path/to/chromedriver')  # تأكد من وضع مسار ChromeDriver الصحيح
driver = webdriver.Chrome(service=service, options=chrome_options)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    driver.get("https://www.facebook.com/")
    time.sleep(2)

    # تسجيل الدخول
    driver.find_element(By.ID, "email").send_keys(email)
    driver.find_element(By.ID, "pass").send_keys(password)
    driver.find_element(By.NAME, "login").click()
    time.sleep(5)

    # التأكد من تسجيل الدخول
    if "home" in driver.current_url:
        # استرجاع الصفحات
        pages = driver.find_elements(By.XPATH, "//div[@class='page']")
        pages_list = [{"id": page.get_attribute("data-id"), "name": page.text} for page in pages]
        return jsonify({"success": True, "pages": pages_list})

    return jsonify({"success": False})

@app.route('/start-bot', methods=['POST'])
def start_bot():
    data = request.json
    selected_page = data.get('page')

    # فتح صفحة الرسائل
    driver.get(f"https://www.facebook.com/{selected_page}/inbox")
    time.sleep(5)  # الانتظار حتى يتم تحميل الصفحة

    # الرد على الرسائل
    messages = driver.find_elements(By.XPATH, "//div[contains(@class, 'message')]")
    for message in messages:
        print(message.text)  # عرض الرسائل (يمكن تعديل الكود للرد)

        # هنا يمكنك إضافة شرط للرد على الرسالة إذا كانت تحتاج لرد
        if "استفسار" in message.text:
            reply_box = message.find_element(By.XPATH, "//textarea[contains(@class, 'reply')]")
            reply_box.send_keys("شكراً لاستفسارك!")
            reply_box.send_keys('\n')  # إرسال الرد

    # فتح صفحة المنشورات
    driver.get(f"https://www.facebook.com/{selected_page}/posts")
    time.sleep(5)

    # الرد على التعليقات
    comments = driver.find_elements(By.XPATH, "//div[contains(@class, 'comment')]")
    for comment in comments:
        print(comment.text)  # عرض التعليقات (يمكن تعديل الكود للرد)

        # الرد على التعليق إذا كان يحتوي على كلمة معينة
        if "سؤال مهم" in comment.text:
            reply_button = comment.find_element(By.XPATH, ".//button[contains(text(), 'رد')]")
            reply_button.click()
            time.sleep(1)  # الانتظار حتى يتم فتح مربع الرد
            
            # كتابة الرد
            reply_box = comment.find_element(By.XPATH, ".//textarea")
            reply_box.send_keys("شكرًا على سؤالك، سأجيب عليك قريبًا!")
            reply_box.send_keys('\n')  # إرسال الرد

    return jsonify({"success": True})

if __name__ == '__main__':
    app.run(debug=True)
