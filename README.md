# ESP8266 Blynk Proxy Server

Proxy server สำหรับเชื่อมต่อระหว่างเว็บไซต์กับ Blynk IoT Platform

## ฟีเจอร์
- ควบคุม LED 4 ดวง (V1-V4)
- ตรวจสอบสถานะการเชื่อมต่อ ESP8266
- Real-time updates
- CORS support

## API Endpoints
- `GET /` - หน้าแรก
- `GET /api/get/<pin>` - อ่านค่า Virtual Pin
- `GET /api/update/<pin>/<value>` - อัพเดท Virtual Pin
- `GET /api/status` - ตรวจสอบสถานะ ESP8266
- `GET /api/all-pins` - อ่านค่าทุก Pin
- `GET /api/health` - Health check

## การใช้งาน
1. ตั้งค่า BLYNK_AUTH_TOKEN ในไฟล์ blynk_proxy.py
2. Deploy ไปยัง Render
3. ใช้ URL ที่ได้เป็น PROXY_SERVER ในเว็บไซต์
