
import sqlite3
from flask import Flask, render_template, request, redirect, url_for
from flask_cors import CORS
from datetime import datetime

DB_PATH = "gold_prices.db"

# สร้าง Flask app ก่อน
app = Flask(__name__)
CORS(app)  # เปิดให้ API ถูกเรียกใช้จากทุกแหล่งที่มา

# หน้าแรก (Home)
@app.route('/')
def home():
    return render_template('index.html')

# หน้า Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # เพิ่มโค้ดการตรวจสอบ username และ password ที่นี่
        return redirect(url_for('pricegold'))  # ถ้าเข้าสู่ระบบสำเร็จให้ไปที่หน้า Pricegold
    return render_template('login.html')

# หน้า Pricegold (แสดงราคาทองคำ)
@app.route('/pricegold')
def pricegold():
    price = 1900  # สมมุติราคาทองคำ
    return render_template('pricegold.html', price=price)

# หน้า Regis (ลงทะเบียนผู้ใช้ใหม่)
@app.route('/regis', methods=['GET', 'POST'])
def regis():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # เพิ่มโค้ดการบันทึกผู้ใช้ใหม่
        return redirect(url_for('login'))  # เมื่อสมัครเสร็จให้ไปที่หน้า Login
    return render_template('regis.html')

# หน้า TradingGold (ซื้อขายทองคำ)
@app.route('/tradinggold')
def tradinggold():
    return render_template('tradinggold.html')

@app.route('/aboutgold')
def aboutgold():
    return render_template('aboutgold.html')

@app.route('/goldcalculator')
def goldcalculator():
    return render_template('goldcalculator.html')


if __name__ == '__main__':
    app.run(debug=True)

# ฟังก์ชันเชื่อมต่อฐานข้อมูล
def connect_db():
    return sqlite3.connect(DB_PATH)

# ฟังก์ชันสร้างตาราง
def create_table():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS gold_prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT DEFAULT (datetime('now', 'localtime')),
            price REAL NOT NULL
        )
        ''')
        conn.commit()

# ฟังก์ชันเพิ่มราคาทองคำ ณ เวลาปัจจุบัน
def add_gold_price(price):
    with connect_db() as conn:
        cursor = conn.cursor()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute('INSERT INTO gold_prices (timestamp, price) VALUES (?, ?)', (timestamp, price))
        conn.commit()
        print(f"✅ เพิ่มราคาทอง {price} บาท ณ {timestamp}")

# ฟังก์ชันดึงข้อมูลราคาทองคำทั้งหมด
def fetch_gold_prices():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM gold_prices ORDER BY timestamp DESC')
        return cursor.fetchall()

# ฟังก์ชันดึงราคาทองคำล่าสุด
def fetch_latest_gold_price():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM gold_prices ORDER BY timestamp DESC LIMIT 1')
        result = cursor.fetchone()
        return result if result else "❌ ไม่มีข้อมูล"

# เพิ่ม route สำหรับหน้าแรก
@app.route('/')
def home():
    return render_template('index.html')

# เพิ่ม route สำหรับแสดงราคาทองคำล่าสุดใน HTML
@app.route('/latest-gold-price')
def latest_gold_price():
    result = fetch_latest_gold_price()
    if result != "❌ ไม่มีข้อมูล":
        return render_template('latest_gold_price.html', timestamp=result[1], price=result[2])
    else:
        return render_template('latest_gold_price.html', error="ไม่พบราคาทองคำในฐานข้อมูล")

# เพิ่ม route สำหรับแสดงราคาทองคำทั้งหมดใน HTML
@app.route('/all-gold-prices')
def all_gold_prices():
    results = fetch_gold_prices()
    if results:
        return render_template('all_gold_prices.html', gold_prices=results)
    else:
        return render_template('all_gold_prices.html', error="ไม่พบข้อมูลราคาทองคำในฐานข้อมูล")

# ฟังก์ชันรัน Flask app
def run():
    app.run(host='0.0.0.0', port=5000)

# สร้างตารางถ้ายังไม่มี
create_table()

# ทดสอบการเพิ่มข้อมูล
add_gold_price(30800.75)  # เพิ่มข้อมูลใหม่
add_gold_price(30950.00)  # เพิ่มข้อมูลใหม่

# รัน Flask server
if __name__ == '__main__':
    run()
