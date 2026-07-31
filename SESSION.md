# Jarvis AI Session Log

Created: 2026-07-05
Last Updated: 2026-07-23
Project Structure Reference: `tree /F`

---

# Project

## Jarvis AI

Jarvis AI คือระบบผู้ช่วย AI ส่วนตัวแบบ Local ที่สามารถสนทนาด้วยเสียง ฟังคำสั่ง เรียกใช้เครื่องมือ ช่วยจดจำข้อมูล และตอบกลับผ่านลำโพงได้

ระบบถูกออกแบบให้เป็น Modular Architecture เพื่อให้สามารถเปลี่ยนหรือเพิ่มส่วนประกอบต่าง ๆ ได้ในอนาคต เช่น:

* Speech To Text
* Text To Speech
* Large Language Model
* Agent
* Tool
* Memory
* Meeting Summary
* Remote Channel
* Desktop Automation
* Vision

Jarvis ไม่ใช่เพียง Chatbot แต่เป็นแนวทางของ Personal AI Operating System

---

# Current Project Phase

Phase: Stable Voice Assistant Core

เป้าหมายปัจจุบันคือทำระบบ Voice Assistant ที่มีอยู่ให้เสถียรก่อนเริ่มเพิ่ม Meeting Summary Module และการเชื่อมต่อผ่าน Telegram หรือ LINE

---

# Completed Work

## 2026-07-05

### Voice Pipeline

Status: Completed

ทำระบบ Voice Pipeline ขั้นต้นสำเร็จ

Flow การทำงาน:

Microphone
↓
Speech To Text
↓
Jarvis Agent
↓
Tool Calling
↓
Text To Speech
↓
Speaker

ผลลัพธ์:

* สามารถพูดกับ Jarvis ผ่านไมโครโฟนได้
* Jarvis แปลงเสียงเป็นข้อความได้
* Jarvis ส่งข้อความเข้า Agent ได้
* Agent สามารถสร้างคำตอบได้
* Agent สามารถเรียกใช้ Tool ขั้นพื้นฐานได้
* ระบบสามารถแปลงข้อความเป็นเสียง
* Jarvis สามารถพูดคำตอบออกลำโพงได้

---

### Basic Agent

Status: Completed / Requires Improvement

ทำ Agent ขั้นต้นสำเร็จ

ความสามารถปัจจุบัน:

* รับข้อความจาก Speech To Text
* ตอบคำถามทั่วไปบางประเภท
* ส่งคำสั่งไปยัง Tool Resolver
* ส่งผลลัพธ์กลับเข้าสู่ Text To Speech

ข้อจำกัด:

* Intent ยังไม่ถูกแยกอย่างชัดเจน
* การตอบคำถามทั่วไปยังไม่แม่นยำ
* Tool Resolver ยังใช้ Keyword Matching มากเกินไป
* ยังไม่มี Confidence Score
* ยังไม่มี Router กลางสำหรับเลือก Agent, Tool หรือ Memory

---

### Basic Tool Calling

Status: Completed / Requires Improvement

ทำระบบ Tool Calling ขั้นต้นสำเร็จ

ความสามารถปัจจุบัน:

* เปิด YouTube
* ตรวจวันที่
* ตรวจเวลา
* รองรับคำสั่งภาษาไทย
* รองรับคำสั่งภาษาอังกฤษ
* รองรับ Alias Matching บางส่วน

ข้อจำกัด:

* ยังไม่มี Tool Parameter แบบเต็มรูปแบบ
* Tool Resolver ยังเรียก Tool จาก Keyword เป็นหลัก
* ยังไม่มี Tool Schema แบบ Structured Output
* ยังไม่มี Parameter Validation
* ยังไม่มี Confirmation สำหรับคำสั่งสำคัญ

---

### Speech To Text

Status: Completed

Model:

* `biodatlab/whisper-th-small-combined`

ความสามารถ:

* รองรับภาษาไทย
* รองรับภาษาอังกฤษ
* ใช้งานผ่าน GPU ได้
* บันทึกโมเดลไว้ในเครื่อง
* สามารถทำงานแบบ Local
* ใช้ถอดเสียงคำสั่งจากไมโครโฟนได้

ข้อจำกัด:

* Wake Word บางครั้งถูกถอดเสียงผิด
* ยังไม่ได้ออกแบบสำหรับไฟล์ประชุมที่มีความยาวมาก
* ยังไม่มี Long-Audio Chunking
* ยังไม่มี Timestamp Transcript แบบเต็มรูปแบบ
* ยังไม่มี Speaker Diarization

---

### Text To Speech

Status: Completed / Requires Stabilization

Engine:

* Thai: `facebook/mms-tts-tha`
* English: Edge TTS

ความสามารถ:

* แปลงข้อความเป็นเสียงได้
* พูดตอบกลับผ่านลำโพงได้
* เลือก Engine ตามภาษาได้ในระดับพื้นฐาน

ปัญหาปัจจุบัน:

* เสียงภาษาไทยยังมีลักษณะคล้ายหุ่นยนต์
* Edge TTS ต้องพึ่งพาการเชื่อมต่ออินเทอร์เน็ต
* Edge TTS อาจเชื่อมต่อไม่ได้
* ยังไม่มี Streaming TTS
* ยังไม่มี Voice Personality
* ยังไม่มี TTS Router ที่สมบูรณ์
* ยังไม่มี Local Fallback สำหรับทุกภาษา
* ยังไม่สามารถยกเลิกเสียงกลางประโยคได้อย่างสมบูรณ์

---

### Basic Memory

Status: Completed / Requires Improvement

ความสามารถปัจจุบัน:

* รองรับ Memory ขั้นพื้นฐาน
* สามารถส่ง Context บางส่วนให้ Agent ได้

ข้อจำกัด:

* ยังไม่มี Session Summary ที่เป็นระบบ
* ยังไม่มี Long-Term Memory
* ยังไม่มี Semantic Search
* ยังไม่แยกประเภท Memory
* ยังไม่สามารถตอบคำถามย้อนหลังได้แม่นยำ
* ยังไม่เชื่อมโยง Memory กับ Project หรือ Meeting

---

# 2026-07-07

## Phase 1 Step 1: Voice Activity Detection

Status: Completed

ทำระบบ Voice Activity Detection สำเร็จ

หน้าที่:

* Jarvis รอฟังเสียงจากไมโครโฟน
* ตรวจจับเมื่อผู้ใช้เริ่มพูด
* เริ่มอัดเสียงอัตโนมัติ
* ตรวจจับเมื่อผู้ใช้หยุดพูด
* หยุดอัดเสียงอัตโนมัติ
* ส่งไฟล์เสียงเข้าสู่ Whisper

Flow:

Jarvis รอฟัง
↓
ผู้ใช้เริ่มพูด
↓
VAD เริ่มอัด
↓
ผู้ใช้หยุดพูด
↓
VAD หยุดอัด
↓
ส่งเสียงเข้า Speech To Text

ผลลัพธ์:

* ไม่ต้องกด Enter ก่อนพูด
* ไม่ต้องกำหนดเวลาอัดเสียงตายตัว
* Jarvis เริ่มและหยุดอัดตามจังหวะการพูด
* Voice Pipeline มีความเป็นธรรมชาติมากขึ้น

ไฟล์ที่เพิ่ม:

* `app/voice/vad.py`

ไฟล์ที่แก้:

* `jarvis.py`

ข้อจำกัด:

* ยังไม่ได้ทดสอบในสภาพแวดล้อมที่มีเสียงรบกวนมาก
* อาจตรวจจับเสียงลำโพงของ Jarvis เป็นเสียงผู้ใช้
* ต้องปรับเพิ่มก่อนทำ Interrupt Speech

---

## Phase 1 Step 2: Wake Word

Status: Completed / Testing

ทำระบบ Wake Word Detection สำเร็จ

หน้าที่:

* Jarvis จะไม่ตอบทุกเสียงที่ได้ยิน
* Jarvis จะรับคำสั่งเมื่อพบ Wake Word
* ถ้าไม่มี Wake Word ระบบจะข้ามข้อความ
* ถ้ามี Wake Word ระบบจะตัดคำปลุกออก
* ส่งเฉพาะคำสั่งจริงเข้าสู่ Agent

Wake Word ตัวอย่าง:

* จาร์วิส
* Jarvis

Flow:

Microphone
↓
Voice Activity Detection
↓
Speech To Text
↓
Wake Word Detection
↓
ไม่มี Wake Word → ข้ามข้อความ
↓
พบ Wake Word → ตัดคำปลุกออก
↓
ส่งคำสั่งเข้า Agent
↓
Text To Speech ตอบกลับ

ตัวอย่าง:

ผู้ใช้พูด:

> วันนี้วันอะไร

ผลลัพธ์:

Jarvis ไม่ตอบ เพราะไม่มี Wake Word

ผู้ใช้พูด:

> จาร์วิส วันนี้วันอะไร

ผลลัพธ์:

Jarvis รับคำสั่งและตอบกลับ

---

### Wake Word Alias

รองรับคำที่ Whisper อาจถอดเสียงเพี้ยน เช่น:

* จาร์วิส
* จาวิส
* ดาวิส
* จาวิช
* เจวิส
* Jarvis

สิ่งที่ทำแล้ว:

* เพิ่ม Wake Word Alias
* เพิ่ม Fuzzy Matching
* ตัด Wake Word ออกจากคำสั่งก่อนส่งเข้า Agent

ไฟล์ที่เพิ่ม:

* `app/voice/wake_word.py`

ไฟล์ที่แก้:

* `jarvis.py`

ข้อจำกัด:

* ยังไม่มีผลทดสอบจำนวนมาก
* ยังไม่วัด Detection Rate
* ยังไม่วัด False Positive
* ยังไม่วัด False Negative
* Alias ยังมาจากการสังเกตเบื้องต้น
* Fuzzy Threshold ยังต้องปรับจากข้อมูลจริง

---

# Current Observation

ระบบ Voice Assistant ขั้นพื้นฐานสามารถทำงานตั้งแต่ต้นจนจบได้แล้ว

Jarvis สามารถ:

* รอฟังเสียงจากไมโครโฟน
* ตรวจจับเมื่อผู้ใช้เริ่มพูด
* เริ่มอัดเสียงอัตโนมัติ
* ตรวจจับเมื่อผู้ใช้หยุดพูด
* หยุดอัดเสียงอัตโนมัติ
* แปลงเสียงเป็นข้อความ
* ตรวจสอบ Wake Word
* ตัด Wake Word ออกจากคำสั่ง
* ส่งคำสั่งเข้าสู่ Agent
* เรียก Tool ขั้นพื้นฐาน
* สร้างข้อความตอบกลับ
* แปลงข้อความเป็นเสียง
* พูดตอบผ่านลำโพง
* ทำงานต่อได้ในบางกรณีที่ TTS ล้มเหลว

---

# Current Known Issues

## 1. Agent Intent ยังไม่แม่นยำ

Status: Next Priority

Agent ยังตอบคำถามทั่วไปได้ไม่ดี เพราะ Tool Resolver ใช้ Keyword Matching กว้างเกินไป

ตัวอย่าง:

> วันนี้วันอะไร

ผลลัพธ์ที่ถูกต้อง:

* เรียก Date Tool

ตัวอย่าง:

> นายทำอะไรไปแล้วบ้างวันนี้

ผลลัพธ์ที่ถูกต้อง:

* ค้น Session Memory หรือ Project Context
* ไม่ควรเรียก Date Tool เพียงอย่างเดียว

ตัวอย่าง:

> วันนี้เป็นยังไงบ้าง

ผลลัพธ์ที่ถูกต้อง:

* ควรเป็น General Chat
* ไม่ควรเรียก Date Tool โดยอัตโนมัติ

สาเหตุ:

* Tool Resolver ใช้ Keyword Matching มากเกินไป
* คำว่า “วันนี้” ถูกตีความเป็น Date Tool เสมอ
* ยังไม่มี Intent Layer
* ยังไม่มี Confidence Score
* ยังไม่มี Router กลาง
* Memory Retrieval ยังไม่ชัดเจน
* Agent ยังแยก General Chat, Memory และ Tool Action ไม่ได้ดี

แนวทางแก้:

1. เพิ่ม Intent Classifier ก่อน Tool Resolver

2. แยก Intent อย่างน้อยดังนี้:

   * General Chat
   * Memory Question
   * Date Question
   * Time Question
   * Tool Action
   * Meeting Command
   * System Command
   * Unknown Intent

3. เพิ่ม Confidence Score

4. ถ้า Confidence ต่ำ ให้ส่งเข้า General Agent

5. ห้ามเรียก Tool จาก Keyword เพียงคำเดียว

6. เพิ่ม Test Dataset จากประโยคที่ใช้งานจริง

7. เพิ่ม Log ของ Intent และ Tool ที่เลือก

8. เพิ่ม Session Memory Summary

9. สร้าง Router กลางสำหรับ Agent, Tool, Memory และ Meeting Module

ไฟล์ที่แนะนำ:

* `app/agent/intent_classifier.py`
* `app/agent/router.py`
* `app/tools/resolver.py`
* `tests/test_intent_classifier.py`

เกณฑ์ผ่าน:

* Intent Test ถูกต้องอย่างน้อย 90%
* คำว่า “วันนี้” ไม่ทำให้ Date Tool ถูกเรียกโดยอัตโนมัติ
* General Chat, Memory Question และ Tool Action ถูกแยกได้
* Unknown Intent ต้องไม่ทำให้ระบบล่ม

---

## 2. TTS ยังไม่เสถียรเต็มที่

Status: Planned

พบว่า Edge TTS อาจเกิด Error เมื่อเชื่อมต่อ Server ไม่ได้

ตัวอย่าง Error:

```text
Cannot connect to host speech.platform.bing.com:443
```

สิ่งที่ทำแล้ว:

* เพิ่ม `safe_speak()` ใน `jarvis.py`
* TTS Error ไม่ทำให้ Jarvis ปิดตัวทันที
* ระบบสามารถทำงานต่อได้ แม้รอบนั้นไม่มีเสียงออกลำโพง

ข้อจำกัด:

* ยังไม่มี TTS Router ที่ชัดเจน
* ยังไม่มี Local Fallback ที่สมบูรณ์
* ยังไม่มี Timeout Management
* ยังไม่มี Retry Policy
* ยังไม่มี Streaming
* ยังไม่มีระบบยกเลิก Playback
* เสียงภาษาไทยยังไม่เป็นธรรมชาติ

แนวทางแก้:

1. แยก TTS ออกจาก Main Loop
2. สร้าง TTS Base Interface
3. สร้าง TTS Router
4. กำหนด Primary Engine และ Fallback Engine
5. เพิ่ม Timeout
6. เพิ่ม Retry แบบจำกัดจำนวนครั้ง
7. เปลี่ยนไป Local TTS เมื่อ Online TTS ล้มเหลว
8. ให้ระบบตอบข้อความได้ แม้พูดไม่ได้
9. เพิ่ม Error Log
10. เตรียม Playback Controller สำหรับ Interrupt Speech

ไฟล์ที่แนะนำ:

* `app/voice/tts_base.py`
* `app/voice/tts_router.py`
* `app/voice/tts_edge.py`
* `app/voice/tts_local.py`
* `app/voice/playback.py`

เกณฑ์ผ่าน:

* TTS Error ต้องไม่ทำให้ Jarvis ปิดตัว
* เปลี่ยนไปใช้ Fallback ได้อัตโนมัติ
* Jarvis ต้องรับคำสั่งรอบถัดไปได้
* ไม่มีเสียงเก่าค้างอยู่ใน Queue

---

## 3. Wake Word ยังต้องจูนเพิ่ม

Status: In Progress

ปัญหา:

* Whisper อาจถอดคำว่า Jarvis ผิด
* Alias ยังไม่ครอบคลุม
* Fuzzy Matching อาจกว้างเกินไปหรือแคบเกินไป
* ยังไม่มีข้อมูลทดสอบเพียงพอ

แนวทางแก้:

1. ทดสอบ Wake Word อย่างน้อย 50 ครั้ง
2. ทดสอบภาษาไทยและภาษาอังกฤษ
3. ทดสอบในห้องเงียบ
4. ทดสอบในห้องที่มีเสียงรบกวน
5. บันทึกข้อความที่ Whisper ถอดออกมา
6. เพิ่ม Alias จากผลการทดสอบจริง
7. ปรับ Fuzzy Threshold
8. วัด Detection Rate
9. วัด False Positive
10. วัด False Negative

เกณฑ์ผ่าน:

* ตรวจจับ Wake Word ได้อย่างน้อย 90%
* ไม่ตอบเสียงทั่วไปโดยไม่มี Wake Word
* ไม่ถูกเรียกจากคำที่คล้ายกันง่ายเกินไป

---

## 4. Interrupt Speech ยังไม่มี

Status: Planned

ปัญหา:

* ผู้ใช้ต้องรอจน Jarvis พูดจบ
* ไม่สามารถยกเลิกเสียงกลางประโยค
* VAD อาจตรวจจับเสียงจากลำโพงเป็นเสียงผู้ใช้

เป้าหมาย:

* ผู้ใช้พูดแทรกตอน Jarvis กำลังพูดได้
* Jarvis หยุด TTS ทันที
* ยกเลิกเสียงที่รออยู่ใน Queue
* กลับไปรับคำสั่งใหม่

แนวทาง:

1. แยก Playback ออกจาก Main Loop
2. ใช้ Thread, Process หรือ Async Task
3. เพิ่ม Playback Controller
4. เพิ่ม Stop Event
5. ให้ VAD ทำงานระหว่างสถานะ SPEAKING
6. ป้องกัน Echo จากลำโพง
7. ยกเลิก TTS Queue เมื่อมีคำสั่งใหม่
8. กลับเข้าสู่ Listening State

State ที่แนะนำ:

* IDLE
* LISTENING
* TRANSCRIBING
* THINKING
* SPEAKING
* INTERRUPTED
* ERROR

---

## 5. Logging และ Error Recovery ยังไม่เป็นระบบ

Status: Planned

ปัญหา:

* Log กระจายอยู่หลายจุด
* ยังไม่มี Module Health Check
* ยังไม่มี Central State
* ยังวิเคราะห์สาเหตุของ Error ได้ยาก
* Module บางตัวอาจทำให้ Main Loop หยุด

แนวทาง:

1. เพิ่ม Central Logger
2. แยก Log ตาม Module
3. เพิ่ม Error Code
4. เพิ่ม Global Exception Handler
5. เพิ่ม Module-Level Exception Handler
6. เพิ่ม Health Check
7. เพิ่ม State Manager
8. เพิ่ม Startup Validation
9. ตรวจ Model, Microphone, Speaker และ Internet
10. เพิ่ม Automatic Recovery
11. เพิ่ม Config File
12. ย้าย Secret ไปไว้ใน `.env`

ไฟล์ที่แนะนำ:

* `app/core/config.py`
* `app/core/logger.py`
* `app/core/health.py`
* `app/core/state.py`
* `config/settings.yaml`
* `.env`

---

# Current Phase Summary

## Phase 1: Stable Voice Assistant Core

### Completed

* Voice Pipeline
* Speech To Text
* Basic Text To Speech
* Basic Agent
* Basic Tool Calling
* Basic Memory
* Voice Activity Detection
* Wake Word Detection
* Wake Word Alias
* Basic Fuzzy Matching
* Basic TTS Error Handling ด้วย `safe_speak()`

### In Progress

* Wake Word Reliability Testing

### Next

* Agent Intent and Tool Resolver
* TTS Router and Fallback
* Interrupt Speech
* Streaming and Faster Response
* Central Logging
* State Management
* Health Check
* Error Recovery

---

# Updated Work Priority

## Priority 1: Improve Agent Intent and Tool Resolver

เหตุผล:

* เป็นปัญหาหลักของ Agent ในปัจจุบัน
* เป็นแกนกลางของ Voice Assistant
* Meeting Module จะต้องใช้ Intent Routing
* Telegram และ LINE จะส่งทั้งข้อความ คำสั่ง และไฟล์เข้ามา
* ถ้า Router ยังไม่แม่น คำสั่งอาจถูกส่งผิด Module

งานหลัก:

1. สร้าง Intent Classifier
2. สร้าง Agent Router
3. แก้ Tool Resolver
4. เพิ่ม Confidence Score
5. เพิ่ม Intent Test Dataset
6. เพิ่ม Session Memory Summary
7. เพิ่ม Logging ของ Intent และ Tool

---

## Priority 2: Stabilize Text To Speech

งานหลัก:

1. สร้าง TTS Base Interface
2. สร้าง TTS Router
3. แยก Edge TTS
4. แยก Local TTS
5. เพิ่ม Fallback
6. เพิ่ม Timeout
7. เพิ่ม Retry
8. เพิ่ม Playback Controller
9. เพิ่ม Error Log

---

## Priority 3: Test Wake Word Reliability

งานหลัก:

1. ทดสอบอย่างน้อย 50 ครั้ง
2. เก็บ Transcript จาก Whisper
3. เพิ่ม Alias
4. ปรับ Fuzzy Threshold
5. วัด Detection Rate
6. วัด False Positive
7. วัด False Negative

---

## Priority 4: Interrupt Speech

งานหลัก:

1. แยก Playback ออกจาก Main Loop
2. เพิ่ม Stop Event
3. ให้ VAD ฟังระหว่าง Jarvis พูด
4. หยุด TTS เมื่อผู้ใช้พูด
5. ยกเลิก Audio Queue
6. รับคำสั่งใหม่ทันที

---

## Priority 5: Core Stability

งานหลัก:

1. Central Logging
2. State Management
3. Health Check
4. Error Recovery
5. Startup Validation
6. Config Management
7. Unit Test
8. Integration Test
9. Latency Measurement

---

# Next Project Phase

## Phase 2: Meeting Intelligence Module

Status: Planned

เริ่มทำหลังจาก Stable Voice Assistant Core ผ่านเกณฑ์ขั้นต่ำ

เป้าหมาย:

ให้ผู้ใช้อัดเสียงการประชุมด้วยโทรศัพท์ แล้วส่งไฟล์เสียงผ่าน Telegram Bot หรือ LINE Bot ไปยังเครื่องที่รัน Jarvis เพื่อให้ระบบ:

* รับไฟล์เสียง
* ตรวจสอบไฟล์
* แปลงรูปแบบเสียง
* แบ่งไฟล์เป็นช่วง
* ถอดเสียง
* สร้าง Transcript
* สรุปประเด็นสำคัญ
* แยก Decisions
* แยก Action Items
* บันทึกผล
* ส่งสรุปกลับไปยังโทรศัพท์

Meeting Flow:

โทรศัพท์อัดเสียง
↓
ส่งไฟล์ผ่าน Telegram หรือ LINE
↓
Jarvis รับไฟล์
↓
File Validation
↓
Audio Processing
↓
Audio Chunking
↓
Speech To Text
↓
Transcript Cleanup
↓
Meeting Summary
↓
Decisions and Action Items
↓
Meeting Storage
↓
ส่งผลกลับผ่าน Bot

---

# Planned Meeting MVP

## Step 1: Meeting File Processor

* รับ MP3, M4A, WAV, OGG และ AAC
* ตรวจ MIME Type
* จำกัดขนาดไฟล์
* ตรวจความยาวเสียง
* แปลงเป็นรูปแบบมาตรฐาน
* Normalize เสียง
* แบ่งไฟล์เป็น Chunk
* ลบ Temporary File หลังใช้งาน

---

## Step 2: Long-Audio Transcription

* แยกจาก Voice Command STT
* รองรับไฟล์เสียงยาว
* รองรับภาษาไทยและภาษาอังกฤษ
* รองรับการพูดสลับภาษา
* เก็บ Timestamp
* รวม Transcript
* Retry เฉพาะ Chunk ที่ล้มเหลว

---

## Step 3: Transcript Cleanup

* แก้เครื่องหมายวรรคตอน
* ลดคำซ้ำ
* รวมประโยค
* แบ่งหัวข้อ
* เก็บ Raw Transcript
* เก็บ Clean Transcript
* รักษา Timestamp
* ห้ามเปลี่ยนความหมายต้นฉบับ

---

## Step 4: Meeting Summarizer

สร้างผลลัพธ์ดังนี้:

* Meeting Information
* Executive Summary
* Key Discussion Points
* Decisions
* Action Items
* Owners
* Deadlines
* Risks
* Blockers
* Open Questions
* Next Meeting

---

## Step 5: Meeting Storage

จัดเก็บ:

* Meeting ID
* ชื่อการประชุม
* วันที่ประชุม
* วันที่อัปโหลด
* ผู้ส่งไฟล์
* Audio Path
* Raw Transcript
* Clean Transcript
* Summary
* Decisions
* Action Items
* Processing Status
* Error Message

---

## Step 6: Meeting Job Queue

สถานะที่ต้องรองรับ:

* RECEIVED
* VALIDATING
* PREPROCESSING
* TRANSCRIBING
* SUMMARIZING
* COMPLETED
* FAILED
* CANCELLED

---

# Phase 3: Remote Channel Integration

Status: Planned

เป้าหมาย:

ให้ผู้ใช้ส่งไฟล์ประชุมและสั่งงาน Jarvis จากโทรศัพท์ได้ โดยไม่ต้องนำคอมพิวเตอร์ไปที่ทำงาน

ลำดับการพัฒนา:

1. สร้าง Channel Interface
2. ทำ Telegram Bot MVP
3. เพิ่ม User Allowlist
4. เพิ่ม File Security
5. เพิ่ม Job Status
6. ตั้ง Worker ให้ทำงานต่อเนื่อง
7. เพิ่ม LINE Bot หลัง Telegram เสถียร

เหตุผลที่เริ่ม Telegram ก่อน:

* ทำ MVP ได้ง่ายกว่า
* รองรับไฟล์และข้อความได้ตรงไปตรงมา
* ทดสอบระบบ End-to-End ได้เร็ว
* ลดความซับซ้อนจากการทำสอง Channel พร้อมกัน

---

# Future Phases

## Phase 4: Tool Parameters

* Structured Tool Calling
* Parameter Extractor
* Tool Schema
* Parameter Validation
* Tool Confirmation

## Phase 5: Long-Term Memory

* Project Memory
* Meeting History
* Action Item Memory
* Semantic Search
* Session Summary
* User Preference

## Phase 6: Desktop Automation

* เปิดและปิดโปรแกรม
* เปิดเว็บไซต์
* ค้นหาไฟล์
* ควบคุมเมาส์และคีย์บอร์ด
* จัดการหน้าต่าง
* Confirmation สำหรับคำสั่งสำคัญ

## Phase 7: Vision

* Screenshot
* วิเคราะห์หน้าจอ
* อ่าน Error
* อ่านเอกสาร
* ใช้ร่วมกับ Desktop Automation

## Phase 8: Multi-Agent

* Planner Agent
* Tool Agent
* Memory Agent
* Voice Agent
* Meeting Agent
* Vision Agent
* Desktop Agent

## Phase 9: Home Automation

* Smart Home API
* เปิดและปิดไฟ
* ควบคุมอุปกรณ์
* ตรวจสถานะเครื่อง Jarvis

---

# Immediate Next Task

งานถัดไปที่ควรเริ่มทันที:

## Build Intent Classifier and Agent Router

ลำดับงาน:

1. รวบรวมประโยคคำสั่งที่ใช้งานจริง
2. แบ่งประโยคตาม Intent
3. สร้าง Intent Enum
4. สร้าง Intent Result Model
5. สร้าง Intent Classifier
6. เพิ่ม Confidence Score
7. สร้าง Agent Router
8. ปรับ Tool Resolver
9. เพิ่ม Unit Test
10. ทดสอบกับ Voice Pipeline

ตัวอย่าง Intent:

```text
GENERAL_CHAT
MEMORY_QUESTION
DATE_QUESTION
TIME_QUESTION
TOOL_ACTION
MEETING_COMMAND
SYSTEM_COMMAND
UNKNOWN
```

เกณฑ์เสร็จ:

* Intent Test ผ่านอย่างน้อย 90%
* คำว่า “วันนี้” ไม่เรียก Date Tool โดยอัตโนมัติ
* Memory Question ถูกส่งไป Memory
* Tool Action ถูกส่งไป Tool Resolver
* Meeting Command พร้อมรองรับในอนาคต
* Unknown Intent ไม่ทำให้ Jarvis ล่ม

---

# 2026-07-31

## Phase 1 Core Completion and Roadmap Update

Status: Core MVP Code Complete / Hardware Acceptance Pending

งานที่ทำ:

* เพิ่ม `Intent` และ `IntentResult` เป็นโมเดลกลาง
* เพิ่ม `IntentClassifier` แบบ deterministic สำหรับคำสั่งหลัก
* เพิ่ม `AgentRouter` ให้จำแนก Intent ก่อนเลือก Tool
* รองรับ General Chat, Memory, Date, Time, Tool, System, Meeting และ Network Intent
* เพิ่ม Confidence Score และ Reason ในผลจำแนก
* ป้องกันคำถาม “วันนี้เราคุยอะไรกัน” ไม่ให้เรียก Date Tool
* ปรับ `JarvisAgent` ไม่ให้ส่งข้อความผู้ใช้ซ้ำเข้า LLM
* แก้ `except:` แบบกว้างใน JSON parsing
* เพิ่ม Dependency Injection ให้ Agent ทดสอบได้ง่ายขึ้น
* เพิ่ม Central Logging สำหรับ Intent, Tool, STT, Wake Word, TTS และ Main Loop
* ปรับ TTS Router เป็น Lazy Loading
* เพิ่ม `TTSError` flow และให้ระบบทำงานต่อเมื่อไม่มีเสียง
* แก้ Edge TTS busy loop และลบ Temporary Audio หลังใช้งาน
* แยก Exit Command Helper ออกจาก Voice Dependencies
* เพิ่ม Automated Test สำหรับ Intent, Router, Wake Word และ Exit Command

ผลทดสอบ:

* Automated Test ใหม่ผ่าน 9/9 เคส
* Python syntax validation ผ่าน
* ยังไม่ได้รับรองคุณภาพไมโครโฟน, Wake Word และ TTS บน Hardware จริงใน Session นี้

ไฟล์สำคัญที่เพิ่ม:

* `app/core/intents.py`
* `app/core/commands.py`
* `app/agents/intent_classifier.py`
* `app/agents/router.py`
* `tests/test_intent_classifier.py`
* `tests/test_core_voice.py`

## Phase 1 Acceptance Remaining

ก่อนติดป้าย Stable Release ต้องทำบนเครื่องจริง:

1. รัน `scripts/doctor.py`
2. ทดสอบ Voice Pipeline แบบ End-to-End
3. ทดสอบ Wake Word อย่างน้อย 50 ครั้ง
4. บันทึก Detection Rate, False Positive และ False Negative
5. ทดสอบ Thai TTS และ Edge TTS ทั้งกรณี Online/Offline
6. ตรวจ Log หลังรันต่อเนื่อง

Interrupt Speech และ Streaming ถูกย้ายไป Phase 1.1 เพื่อไม่ขวาง Module ธุรกิจถัดไป

## New Planned Track: Home Network Anomaly Detection

Status: Added to Roadmap / Not Implemented

เป้าหมาย:

* รับจำนวนอุปกรณ์ที่เชื่อม Wi-Fi
* รับปริมาณการใช้งานเครือข่ายและเว็บไซต์/โดเมนเท่าที่ Router รองรับ
* ตรวจอุปกรณ์ใหม่และพฤติกรรมผิดปกติ
* สร้าง Risk Score, Confidence, Evidence และคำแนะนำ
* ให้ Jarvis อธิบายผลโดยไม่สร้างข้อเท็จจริงหรือคะแนนเอง

หลักการพัฒนา:

1. ตรวจแหล่งข้อมูลจาก Router ก่อน
2. สร้าง Mock Collector และ SQLite Storage
3. เริ่มด้วย Explainable Rule Engine
4. เก็บ Baseline 2–4 สัปดาห์
5. เพิ่ม Anomaly Detection หลังมีข้อมูลเพียงพอ

## Next Session Decision

หลัง Phase 1 ผ่าน Hardware Acceptance ให้เลือก:

* Phase 2A: Meeting Intelligence
* Phase 2B: Home Network Anomaly Detection

ถ้า Router ยังไม่สามารถส่งข้อมูลที่ต้องการได้ ให้เริ่ม Meeting Intelligence ก่อน ระหว่างนั้นจึงสำรวจหรือเปลี่ยน Network Data Source

---

## 2026-07-31: Web Tools Expansion

Status: Completed

เพิ่มความสามารถ:

* `play_youtube_song` รับชื่อเพลง ค้นหา YouTube ผลลัพธ์แรกผ่าน `yt-dlp` และเปิดวิดีโอโดยตรง
* ถ้า Direct Lookup ล้มเหลว ระบบเปิดหน้าค้นหา YouTube เป็น Fallback
* `open_facebook` เปิด Facebook ใน Default Browser
* `open_instagram` เปิด Instagram ใน Default Browser
* `search_google` แยกคำค้นหาจากภาษาไทยหรืออังกฤษและเปิด Google Results
* เพิ่ม Alias สำหรับ Facebook, FB, Instagram, IG, เฟซบุ๊ก, เฟส, อินสตาแกรม และไอจี
* ปรับ Intent Classifier ให้ Web Commands ผ่าน Tool Route
* เพิ่ม `yt-dlp` ใน `requirements.txt` และ Installation Doctor

ตัวอย่างคำสั่งที่รองรับ:

* “จาร์วิส เปิดเพลง Shape of You”
* “จาร์วิส เล่นเพลง Numb Linkin Park”
* “จาร์วิส เปิด Facebook”
* “จาร์วิส เปิดไอจี”
* “จาร์วิส ค้นหาในกูเกิลเรื่อง AI Agent”

ผลทดสอบ:

* Automated Test รวมผ่าน 14/14 เคส
* Tests ไม่เปิด Browser จริง โดยใช้ Mock ตรวจ URL และ Routing
