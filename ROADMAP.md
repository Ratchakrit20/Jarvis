# Jarvis AI Roadmap

Last Updated: 2026-07-23

---

# Long-Term Goal

Jarvis AI คือระบบผู้ช่วย AI ส่วนตัวแบบ Local ที่สามารถฟัง พูด คิด จำ เรียกใช้เครื่องมือ ช่วยสรุปการประชุม และควบคุมคอมพิวเตอร์แทนผู้ใช้ได้

เป้าหมายระยะยาวไม่ใช่การสร้าง Chatbot แต่เป็น Personal AI Operating System ที่สามารถเพิ่ม Module ใหม่ได้โดยไม่กระทบระบบหลัก

หลักการสำคัญของระบบ:

* Local First
* Modular Architecture
* Privacy First
* Remote Access อย่างปลอดภัย
* สามารถเปลี่ยน STT, TTS, LLM, Tool, Memory และช่องทางรับคำสั่งได้
* ระบบส่วนหนึ่งล้มแล้วต้องไม่ทำให้ทั้ง Jarvis หยุดทำงาน

---

# Overall Architecture

Jarvis แบ่งระบบออกเป็น Module หลักดังนี้:

* Voice Assistant Module
* Agent and Intent Module
* Tool Module
* Memory Module
* Meeting Intelligence Module
* Remote Channel Module
* Desktop Automation Module
* Vision Module
* Home Automation Module

ทุก Module เชื่อมต่อผ่าน Core ของ Jarvis โดยไม่ควรผูกติดกับไฟล์ `jarvis.py` เพียงไฟล์เดียว

---

# Phase 1: Stable Voice Assistant Core

Status: In Progress

เป้าหมายของ Phase 1 คือทำให้ระบบ Voice Assistant ที่มีอยู่ทำงานได้เสถียร ก่อนเพิ่ม Meeting Summary และความสามารถใหม่

Architecture:

Microphone
↓
Voice Activity Detection
↓
Speech To Text
↓
Wake Word Detection
↓
Intent Classification
↓
Memory Retrieval
↓
Agent
↓
Tool Calling
↓
Text To Speech
↓
Speaker

---

## Step 1: Voice Activity Detection

Status: Completed

หน้าที่:

* ตรวจจับเมื่อผู้ใช้เริ่มพูด
* เริ่มอัดเสียงอัตโนมัติ
* ตรวจจับเมื่อผู้ใช้หยุดพูด
* หยุดอัดเสียงและส่งเข้า Speech To Text

สิ่งที่ทำแล้ว:

* เพิ่มระบบ VAD
* ไม่ต้องกด Enter เพื่อเริ่มพูด
* ไม่ต้องกำหนดเวลาอัดเสียงตายตัว
* Jarvis สามารถฟังตามจังหวะการพูดของผู้ใช้ได้

ไฟล์หลัก:

* `app/voice/vad.py`
* `jarvis.py`

---

## Step 2: Wake Word

Status: Completed / Testing

หน้าที่:

* ให้ Jarvis รอคำปลุกก่อนรับคำสั่ง
* ถ้าไม่มีคำว่า “Jarvis” หรือ “จาร์วิส” จะไม่ส่งข้อความเข้า Agent
* ลดการตอบจากเสียงรอบข้างโดยไม่ตั้งใจ
* ตัดคำปลุกออกก่อนส่งคำสั่งจริงเข้า Agent

สิ่งที่ทำแล้ว:

* เพิ่ม Wake Word Detector
* รองรับภาษาไทยและภาษาอังกฤษ
* รองรับคำที่ Whisper ถอดเสียงเพี้ยน เช่น จาวิส ดาวิส และจาวิช
* เพิ่ม Fuzzy Matching
* ตัด Wake Word ออกจากคำสั่งก่อนส่งเข้า Agent

สิ่งที่ต้องทำเพิ่ม:

* เก็บ Log ผลการถอดเสียง Wake Word
* ทดสอบอย่างน้อย 50 ครั้งในสภาพแวดล้อมหลายแบบ
* วัด Detection Rate และ False Activation Rate
* ปรับ Alias และ Fuzzy Threshold จากข้อมูลจริง

เกณฑ์ผ่าน:

* ตรวจจับ Wake Word ได้อย่างน้อย 90%
* การตอบโดยไม่มี Wake Word ต้องเกิดขึ้นน้อยมาก
* เสียงรบกวนทั่วไปต้องไม่เรียก Jarvis โดยไม่ตั้งใจ

ไฟล์หลัก:

* `app/voice/wake_word.py`
* `jarvis.py`

---

## Step 3: Agent Intent and Tool Resolver

Status: Next

เป้าหมาย:

แก้ปัญหา Agent เรียก Tool ผิด เพราะใช้ Keyword Matching กว้างเกินไป

ตัวอย่างปัญหา:

* “วันนี้วันอะไร” ควรเรียก Date Tool
* “วันนี้ฉันทำอะไรไปแล้วบ้าง” ควรค้น Session Memory
* “วันนี้เป็นยังไงบ้าง” อาจเป็น General Chat
* ไม่ควรเรียก Date Tool เพียงเพราะพบคำว่า “วันนี้”

Intent ที่ต้องรองรับ:

* General Chat
* Date Question
* Time Question
* Memory Question
* Tool Action
* Meeting Command
* System Command
* Unknown Intent

Flow ใหม่:

User Input
↓
Intent Classifier
↓
เลือกเส้นทางการทำงาน
↓
General Agent / Memory / Tool / Meeting Module
↓
สร้างคำตอบ

สิ่งที่ต้องทำ:

* สร้าง `IntentClassifier`
* ให้ Intent Layer ทำงานก่อน Tool Resolver
* ปรับ Tool Resolver ให้ตรวจทั้งความหมาย ไม่ใช่เฉพาะ Keyword
* เพิ่ม Confidence Score
* ถ้า Confidence ต่ำ ให้ตอบแบบ General Chat หรือขอข้อมูลเพิ่ม
* เพิ่ม Test Cases ภาษาไทยและอังกฤษ
* บันทึก Intent และ Tool ที่ถูกเลือกลง Log

ไฟล์ที่แนะนำ:

* `app/agent/intent_classifier.py`
* `app/agent/router.py`
* `app/tools/resolver.py`
* `tests/test_intent_classifier.py`

เกณฑ์ผ่าน:

* ชุดทดสอบ Intent ถูกต้องอย่างน้อย 90%
* ไม่เรียก Date Tool ผิดเพียงเพราะพบคำว่า “วันนี้”
* Tool ทุกตัวต้องถูกเรียกจาก Intent ที่เหมาะสม

---

## Step 4: TTS Stability

Status: Planned

เป้าหมาย:

ทำให้ Jarvis พูดตอบได้เสถียร แม้อินเทอร์เน็ตขัดข้องหรือ TTS Engine บางตัวใช้งานไม่ได้

สิ่งที่ต้องทำ:

* แยก TTS ออกจาก Main Loop
* สร้าง `TTSRouter`
* เพิ่ม Primary Engine และ Fallback Engine
* ตรวจสถานะอินเทอร์เน็ตก่อนเลือก Online TTS
* ถ้า Online TTS ล้มเหลว ให้เปลี่ยนไป Local TTS อัตโนมัติ
* จำกัดเวลา Timeout
* เพิ่ม Retry แบบมีจำนวนครั้งจำกัด
* เก็บ Error Log
* ระบบต้องตอบเป็นข้อความได้ แม้สร้างเสียงไม่สำเร็จ

ตัวอย่าง Routing:

ภาษาไทย
↓
Thai TTS Primary
↓ ถ้าล้มเหลว
Local Thai TTS Fallback
↓ ถ้ายังล้มเหลว
แสดงเฉพาะข้อความ

ภาษาอังกฤษ
↓
Edge TTS
↓ ถ้าล้มเหลว
Local English TTS
↓ ถ้ายังล้มเหลว
แสดงเฉพาะข้อความ

ไฟล์ที่แนะนำ:

* `app/voice/tts_router.py`
* `app/voice/tts_base.py`
* `app/voice/tts_local.py`
* `app/voice/tts_edge.py`

เกณฑ์ผ่าน:

* TTS Error ต้องไม่ทำให้ Jarvis ปิดตัว
* ระบบต้องเปลี่ยนไปใช้ Fallback อัตโนมัติ
* การสนทนาต้องดำเนินต่อได้ แม้ไม่มีเสียงออกลำโพง

---

## Step 5: Interrupt Speech

Status: Planned

หน้าที่:

* ให้ผู้ใช้พูดแทรกตอน Jarvis กำลังพูดได้
* เมื่อผู้ใช้พูดแทรก Jarvis ต้องหยุด TTS
* จากนั้นกลับไปรับคำสั่งใหม่

แนวทาง:

* แยก TTS Playback ออกจาก Main Loop
* ใช้ Thread, Process หรือ Async Task สำหรับการเล่นเสียง
* ให้ VAD ตรวจจับเสียงระหว่าง Jarvis กำลังพูด
* ลดการตรวจจับเสียงลำโพงของ Jarvis เป็นเสียงผู้ใช้
* เมื่อพบเสียงพูดแทรก ให้ส่ง Stop Signal ไปยัง TTS
* กลับเข้าสู่ Listening State

State ที่แนะนำ:

* IDLE
* LISTENING
* TRANSCRIBING
* THINKING
* SPEAKING
* INTERRUPTED
* ERROR

เกณฑ์ผ่าน:

* หยุดเสียงหลังผู้ใช้พูดแทรกได้อย่างรวดเร็ว
* Jarvis ต้องไม่ค้างอยู่ในสถานะ SPEAKING
* หลังหยุดเสียงต้องรับคำสั่งใหม่ได้ทันที

---

## Step 6: Streaming and Faster Response

Status: Planned

เป้าหมาย:

* ลดเวลารอหลังผู้ใช้พูดจบ
* ให้ Jarvis เริ่มตอบก่อนสร้างเสียงครบทั้งประโยค
* ทำให้การสนทนาเป็นธรรมชาติมากขึ้น

สิ่งที่ต้องทำ:

* วัด Latency ของ VAD, STT, Agent และ TTS แยกกัน
* รองรับ Streaming Response จาก LLM ถ้า Model รองรับ
* แบ่งข้อความเป็นประโยคสั้นก่อนส่งเข้า TTS
* เริ่มเล่นเสียงทันทีเมื่อประโยคแรกพร้อม
* เพิ่ม Queue สำหรับข้อความและเสียง
* ยกเลิก Queue เมื่อผู้ใช้พูดแทรก

เกณฑ์ผ่าน:

* ระบุได้ว่า Latency ส่วนใหญ่มาจาก Module ใด
* Jarvis เริ่มตอบเร็วขึ้นอย่างเห็นได้ชัด
* ไม่เล่นเสียงเก่าหลังผู้ใช้ส่งคำสั่งใหม่

---

## Step 7: Stability, Logging and Recovery

Status: Planned

เป้าหมาย:

ทำให้ Jarvis สามารถรันต่อเนื่องได้โดยไม่ต้องเปิดโปรแกรมใหม่บ่อย ๆ

สิ่งที่ต้องทำ:

* เพิ่ม Central Logging
* แยก Log ตาม Module
* เพิ่ม Exception Handler ระดับ Module
* เพิ่ม Health Check
* เพิ่ม Automatic Recovery สำหรับ Module ที่ล้ม
* เพิ่ม Config File แทนการเขียนค่าคงที่ใน Code
* เพิ่ม `.env` สำหรับ Secret
* เพิ่ม Unit Test และ Integration Test
* เพิ่ม Startup Check สำหรับ Model, Microphone, Speaker และ Internet
* บันทึก Latency และ Error Rate

ไฟล์ที่แนะนำ:

* `app/core/config.py`
* `app/core/logger.py`
* `app/core/health.py`
* `app/core/state.py`
* `config/settings.yaml`
* `.env`

เกณฑ์จบ Phase 1:

* Jarvis สนทนาด้วยเสียงต่อเนื่องได้
* Wake Word ทำงานตามเกณฑ์
* Intent Routing ผ่านชุดทดสอบ
* TTS ล้มแล้วระบบไม่ปิด
* Interrupt Speech ใช้งานได้
* Error ของ Module หนึ่งไม่ทำให้ระบบทั้งหมดหยุด
* มี Log เพียงพอสำหรับหาสาเหตุเมื่อเกิดปัญหา

---

# Phase 2: Meeting Intelligence Module

Status: Planned

เป้าหมาย:

ให้ผู้ใช้อัดไฟล์เสียงในห้องประชุมด้วยโทรศัพท์ จากนั้นอัปโหลดไฟล์ผ่าน LINE Bot หรือ Telegram Bot เพื่อให้ Jarvis ที่ทำงานอยู่บนเครื่องส่วนตัวรับไฟล์ ถอดเสียง และสร้างสรุปการประชุมโดยอัตโนมัติ

Jarvis ไม่จำเป็นต้องอยู่ในห้องประชุม และผู้ใช้ไม่จำเป็นต้องนำคอมพิวเตอร์ไปที่ทำงาน

---

## Meeting Workflow

ผู้ใช้อัดเสียงการประชุมด้วยโทรศัพท์
↓
ส่งไฟล์เข้า LINE Bot หรือ Telegram Bot
↓
Bot ตรวจสอบผู้ส่งและประเภทไฟล์
↓
ดาวน์โหลดไฟล์ไปยังพื้นที่ชั่วคราว
↓
สร้าง Meeting Job
↓
จัดการและแปลงรูปแบบเสียง
↓
แบ่งไฟล์เสียงเป็นช่วง
↓
Speech To Text
↓
รวม Transcript
↓
ทำความสะอาด Transcript
↓
สร้าง Meeting Summary
↓
บันทึกผลลัพธ์
↓
ส่งสรุปกลับผ่าน Bot

---

## Step 1: Meeting File Processor

Status: Planned

หน้าที่:

* รับไฟล์เสียงที่อัดจากโทรศัพท์
* ตรวจสอบว่าเป็นไฟล์ที่รองรับ
* แปลงไฟล์ให้อยู่ในรูปแบบมาตรฐาน
* เตรียมไฟล์สำหรับ Speech To Text

รูปแบบไฟล์ที่ควรรองรับ:

* MP3
* M4A
* WAV
* OGG
* AAC

สิ่งที่ต้องทำ:

* ตรวจสอบนามสกุลและ MIME Type
* จำกัดขนาดไฟล์
* ตรวจสอบความยาวเสียง
* แปลงเป็น Mono
* ปรับ Sample Rate ให้เหมาะกับ STT
* Normalize ระดับเสียง
* แบ่งไฟล์ยาวเป็น Chunk
* ลบ Temporary File หลังงานเสร็จตามนโยบาย

ไฟล์ที่แนะนำ:

* `app/meeting/audio_processor.py`
* `app/meeting/audio_chunker.py`
* `app/meeting/file_validator.py`

---

## Step 2: Meeting Speech To Text

Status: Planned

เป้าหมาย:

ถอดเสียงประชุมที่มีความยาวมากกว่าคำสั่งเสียงทั่วไป

สิ่งที่ต้องทำ:

* แยก Meeting STT ออกจาก Voice Command STT
* รองรับไฟล์เสียงยาว
* ประมวลผลเสียงเป็น Chunk
* บันทึก Timestamp ของแต่ละช่วง
* รองรับภาษาไทย ภาษาอังกฤษ และการพูดสลับภาษา
* รวมผล Transcript ตามลำดับเวลา
* รองรับการทำงานต่อหลังบาง Chunk ล้มเหลว
* เก็บ Transcript ดิบไว้สำหรับตรวจสอบ

โครงสร้างผลลัพธ์ตัวอย่าง:

```json
{
  "meeting_id": "meeting_20260723_001",
  "language": ["th", "en"],
  "duration_seconds": 3600,
  "segments": [
    {
      "start": 0.0,
      "end": 12.5,
      "text": "เริ่มประชุมเรื่องแผนงานไตรมาสหน้า"
    }
  ]
}
```

ไฟล์ที่แนะนำ:

* `app/meeting/transcriber.py`
* `app/meeting/transcript_merger.py`
* `app/meeting/models.py`

---

## Step 3: Transcript Cleanup

Status: Planned

หน้าที่:

* แก้ช่องว่างและเครื่องหมายวรรคตอน
* ลดคำซ้ำจากการพูด
* รวมประโยคที่ขาดออกจากกัน
* แยกหัวข้อเบื้องต้น
* รักษาข้อความต้นฉบับไว้ควบคู่กับข้อความที่ทำความสะอาดแล้ว

สิ่งที่ต้องระวัง:

* ห้ามเปลี่ยนความหมายของผู้พูด
* ห้ามสร้างชื่อ คน ตัวเลข หรือข้อสรุปที่ไม่มีในเสียง
* ส่วนที่ฟังไม่ชัดต้องระบุว่าไม่แน่ชัด
* ควรเก็บ Timestamp ไว้เพื่อย้อนกลับไปตรวจเสียงได้

ไฟล์ที่แนะนำ:

* `app/meeting/transcript_cleaner.py`

---

## Step 4: Meeting Summarizer

Status: Planned

หน้าที่:

สร้างสรุปที่นำไปใช้ทำงานต่อได้ ไม่ใช่เพียงย่อข้อความทั้งหมด

รูปแบบสรุปหลัก:

### ข้อมูลการประชุม

* ชื่อการประชุม
* วันที่
* ระยะเวลา
* ผู้เข้าร่วม หากระบุได้
* ภาษาในการประชุม

### Executive Summary

สรุปภาพรวมของการประชุมแบบสั้น

### Key Discussion Points

ประเด็นสำคัญที่มีการพูดถึง

### Decisions

ข้อสรุปหรือสิ่งที่ตัดสินใจแล้ว

### Action Items

แต่ละรายการควรประกอบด้วย:

* งานที่ต้องทำ
* ผู้รับผิดชอบ
* กำหนดเวลา
* สถานะ
* Timestamp อ้างอิง

### Risks and Blockers

ปัญหา ความเสี่ยง หรือสิ่งที่ขัดขวางงาน

### Open Questions

คำถามหรือประเด็นที่ยังไม่มีข้อสรุป

### Next Meeting

ข้อมูลการประชุมครั้งถัดไป หากมีการระบุ

ระดับสรุปที่ควรรองรับ:

* Quick Summary
* Standard Meeting Notes
* Detailed Summary
* Action Items Only
* Executive Summary

ไฟล์ที่แนะนำ:

* `app/meeting/summarizer.py`
* `app/meeting/summary_templates.py`

---

## Step 5: Long Meeting Processing

Status: Planned

เหตุผล:

Transcript ของการประชุมยาวอาจเกิน Context Window ของโมเดล และไม่ควรส่งทั้งหมดเข้าโมเดลในครั้งเดียว

แนวทาง:

1. แบ่ง Transcript ตามเวลาและหัวข้อ
2. สรุปแต่ละส่วน
3. รวม Partial Summaries
4. สร้าง Final Summary
5. ตรวจหารายการซ้ำ
6. เชื่อม Action Item กับ Timestamp ต้นฉบับ

Flow:

Transcript Chunks
↓
Chunk Summaries
↓
Topic Merge
↓
Decision and Action Extraction
↓
Final Meeting Summary

ไฟล์ที่แนะนำ:

* `app/meeting/chunk_summarizer.py`
* `app/meeting/summary_merger.py`

---

## Step 6: Meeting Storage and Search

Status: Planned

หน้าที่:

* เก็บไฟล์เสียง Transcript และ Summary
* ค้นการประชุมย้อนหลัง
* ให้ Jarvis ตอบคำถามจากการประชุมเก่า
* ป้องกันข้อมูลการประชุมสูญหาย

ข้อมูลที่ต้องจัดเก็บ:

* Meeting ID
* ชื่อการประชุม
* วันที่ประชุม
* วันที่อัปโหลด
* ผู้ส่งไฟล์
* Path ของไฟล์เสียง
* Transcript ดิบ
* Transcript ที่ทำความสะอาดแล้ว
* Summary
* Decisions
* Action Items
* Processing Status
* Error Message

คำสั่งในอนาคต:

* “สรุปประชุมล่าสุดให้หน่อย”
* “เมื่อวานทีมตัดสินใจเรื่องอะไร”
* “งานของฉันจากสามการประชุมล่าสุดมีอะไรบ้าง”
* “ค้นการประชุมที่พูดถึง Project Alpha”
* “เปิด Transcript ตรงที่พูดเรื่องงบประมาณ”

ไฟล์ที่แนะนำ:

* `app/meeting/repository.py`
* `app/meeting/search.py`
* `data/meetings/`

---

## Step 7: Meeting Job Queue

Status: Planned

เหตุผล:

การถอดเสียงและสรุปไฟล์ยาวใช้เวลานาน Bot ไม่ควรรอให้ทุกขั้นตอนเสร็จภายใน Request เดียว

หน้าที่:

* สร้าง Job เมื่อได้รับไฟล์
* ส่งข้อความตอบรับทันที
* ประมวลผลไฟล์เบื้องหลังบนเครื่อง Jarvis
* ติดตามสถานะ
* Retry เมื่อบางขั้นตอนล้มเหลว
* ส่งผลกลับเมื่อเสร็จ
* ป้องกันการประมวลผลไฟล์เดิมซ้ำ

สถานะของ Job:

* RECEIVED
* VALIDATING
* PREPROCESSING
* TRANSCRIBING
* SUMMARIZING
* COMPLETED
* FAILED
* CANCELLED

ตัวอย่างข้อความตอบรับ:

> รับไฟล์ประชุมแล้ว หมายเลขงาน: MTG-20260723-001

คำสั่งตรวจสอบสถานะ:

* “สถานะ MTG-20260723-001”
* “ยกเลิก MTG-20260723-001”
* “ส่งสรุปงานล่าสุดอีกครั้ง”

ไฟล์ที่แนะนำ:

* `app/jobs/meeting_job.py`
* `app/jobs/queue.py`
* `app/jobs/worker.py`

---

# Phase 3: Remote Channel Integration

Status: Planned

เป้าหมาย:

ให้ผู้ใช้สามารถเข้าถึง Jarvis จากที่ทำงานผ่านโทรศัพท์ โดยเครื่องที่รัน Jarvis ยังคงอยู่ที่บ้านหรือสถานที่อื่น

Architecture:

LINE / Telegram
↓
Channel Adapter
↓
Authentication
↓
Command and File Router
↓
Jarvis Core
↓
Meeting Worker / Agent / Tool
↓
Response Formatter
↓
LINE / Telegram

---

## Step 1: Channel Abstraction

Status: Planned

เป้าหมาย:

ไม่ให้ Meeting Module ผูกติดกับ LINE หรือ Telegram โดยตรง

Interface ที่แต่ละ Channel ต้องรองรับ:

* รับข้อความ
* รับไฟล์
* ดาวน์โหลดไฟล์
* ตรวจสอบผู้ส่ง
* ส่งข้อความ
* ส่งไฟล์
* แบ่งข้อความยาว
* แสดงสถานะงาน
* จัดการ Error

ไฟล์ที่แนะนำ:

* `app/channels/base.py`
* `app/channels/router.py`
* `app/channels/models.py`

---

## Step 2: Telegram Bot MVP

Status: Planned

เป้าหมาย:

เริ่มด้วย Channel หนึ่งตัวเพื่อทดสอบระบบตั้งแต่ต้นจนจบ โดยแนะนำให้ทำ Telegram Bot MVP ก่อน แล้วค่อยเพิ่ม LINE Bot ผ่าน Interface เดียวกัน

ความสามารถ MVP:

* รับข้อความ
* รับไฟล์เสียง
* รับ Voice Message
* ดาวน์โหลดไฟล์เข้า Meeting Inbox
* สร้าง Meeting Job
* แจ้งสถานะประมวลผล
* ส่ง Summary กลับเป็นข้อความ
* ส่ง Summary แบบ Markdown หรือไฟล์
* รองรับคำสั่งตรวจสถานะ

คำสั่งตัวอย่าง:

* `/start`
* `/help`
* `/status`
* `/meetings`
* `/latest`
* `/cancel`
* `/delete`

ไฟล์ที่แนะนำ:

* `app/channels/telegram/bot.py`
* `app/channels/telegram/handlers.py`
* `app/channels/telegram/formatter.py`

---

## Step 3: LINE Bot Adapter

Status: Planned

เป้าหมาย:

เพิ่ม LINE เป็นช่องทางรับไฟล์และคำสั่ง โดยใช้ Meeting Module และ Job Queue ชุดเดิม

ความสามารถ:

* รับข้อความจากผู้ใช้
* รับไฟล์เสียงหรือไฟล์แนบ
* ส่งข้อความตอบรับ
* แจ้งสถานะ Job
* ส่ง Meeting Summary
* ส่ง Action Items แบบย่อ
* แจ้ง Error อย่างเข้าใจง่าย

ไฟล์ที่แนะนำ:

* `app/channels/line/bot.py`
* `app/channels/line/handlers.py`
* `app/channels/line/formatter.py`

---

## Step 4: Remote Commands

Status: Planned

คำสั่งที่ควรรองรับ:

* “สรุปไฟล์นี้”
* “สรุปแบบละเอียด”
* “เอาเฉพาะ Action Items”
* “สถานะงานล่าสุด”
* “สรุปประชุมล่าสุด”
* “ค้นประชุมเรื่องงบประมาณ”
* “ลบไฟล์ประชุมล่าสุด”
* “ส่ง Transcript ให้ฉัน”
* “ถามจากการประชุมล่าสุดว่าใครรับผิดชอบงานนี้”

ตัวอย่าง Flow:

ผู้ใช้ส่งไฟล์เสียง
↓
Bot ถามรูปแบบสรุป หรือใช้ค่าเริ่มต้น
↓
Jarvis สร้าง Job
↓
Bot แจ้ง Job ID
↓
Jarvis ประมวลผล
↓
Bot ส่ง Summary
↓
ผู้ใช้ถามต่อจาก Summary ได้

---

## Step 5: Authentication and Security

Status: Planned

เหตุผล:

การประชุมอาจมีข้อมูลภายในบริษัท ข้อมูลลูกค้า หรือข้อมูลที่เป็นความลับ จึงต้องออกแบบความปลอดภัยก่อนเปิดใช้งานจริง

สิ่งที่ต้องทำ:

* ใช้ Allowlist ของ User ID
* ปฏิเสธผู้ใช้ที่ไม่ได้รับอนุญาต
* เก็บ Token และ Secret ใน `.env`
* ห้ามเขียน Secret ลง Git
* จำกัดขนาดและประเภทไฟล์
* เปลี่ยนชื่อไฟล์ก่อนบันทึก
* ป้องกัน Path Traversal
* ตรวจไฟล์ซ้ำ
* จำกัดจำนวนงานต่อผู้ใช้
* เพิ่ม Rate Limit
* เพิ่ม Audit Log
* ลบ Temporary File หลังประมวลผล
* รองรับคำสั่งลบไฟล์ Transcript และ Summary
* กำหนด Retention Policy
* พิจารณาเข้ารหัสข้อมูลที่จัดเก็บ
* ไม่เปิด Port ของ Jarvis ตรงสู่อินเทอร์เน็ตโดยไม่มีระบบป้องกัน

ไฟล์ที่แนะนำ:

* `app/security/auth.py`
* `app/security/file_security.py`
* `app/security/rate_limit.py`
* `app/security/audit.py`

---

## Step 6: Remote Deployment

Status: Planned

เป้าหมาย:

ทำให้เครื่อง Jarvis รับงานจาก Bot ได้ตลอดเวลาตามที่ผู้ใช้ต้องการ

สิ่งที่ต้องทำ:

* แยก Bot Service และ Worker Service
* ตั้งให้ Service เริ่มทำงานอัตโนมัติหลังเปิดเครื่อง
* เพิ่ม Health Check
* เพิ่ม Automatic Restart
* เพิ่มระบบตรวจพื้นที่ Disk
* แจ้งเตือนเมื่อ Model โหลดไม่ได้
* แจ้งเตือนเมื่อพื้นที่เก็บข้อมูลใกล้เต็ม
* เพิ่ม Backup ของ Metadata และ Summary
* ป้องกันเครื่อง Sleep ขณะมี Job
* กำหนดเวลาที่อนุญาตให้ประมวลผล

ทางเลือกการทำงาน:

### Local Home Machine

* Jarvis รันบนเครื่องส่วนตัว
* Bot รับไฟล์และส่งเข้าเครื่องนั้น
* ใช้ GPU ในเครื่องประมวลผล
* ข้อมูลหลักอยู่ในเครื่องผู้ใช้

### Private Server

* รัน Bot หรือ Queue บน Server
* ส่ง Job ไปยังเครื่อง Worker
* เหมาะเมื่อจำเป็นต้องรับไฟล์ตลอดเวลา
* ต้องเพิ่มการรักษาความปลอดภัยมากขึ้น

สำหรับ MVP ควรเริ่มจาก Local Home Machine ก่อน เพื่อลดความซับซ้อนและรักษาแนวคิด Local First

---

# Phase 4: Tool Parameters and General Tools

Status: Planned

เป้าหมาย:

ทำให้ Tool Calling รับ Parameter ได้ ไม่ใช่เพียงเปิด Tool แบบตายตัว

ตัวอย่าง:

* “เปิด YouTube เพลง Taylor Swift”
* “ค้นหา Google เรื่อง AI Agent”
* “เปิดเว็บ GitHub”
* “เปิด Spotify เพลงนี้”
* “สรุปการประชุม MTG-20260723-001 แบบสั้น”
* “ส่ง Action Items ของประชุมล่าสุดเข้า Telegram”

สิ่งที่ต้องทำ:

* เพิ่ม Parameter Extractor
* ปรับ Tool Schema
* เพิ่ม Tool Metadata
* ให้ Agent ส่ง Structured Output
* ตรวจสอบ Parameter ก่อนเรียก Tool
* เพิ่ม Fallback เมื่อ Parameter ไม่ครบ
* เพิ่ม Confirmation สำหรับคำสั่งสำคัญ

---

# Phase 5: Long-Term Memory

Status: Planned

เป้าหมาย:

ให้ Jarvis จำข้อมูลข้ามวันและเชื่อมโยงข้อมูลจากการประชุมเข้ากับงานของผู้ใช้

ประเภท Memory:

* User Preference
* Project State
* Task History
* Meeting History
* Decisions
* Action Items
* People and Teams
* Deadlines

ความสามารถ:

* จำโปรเจกต์ที่กำลังทำ
* จำสิ่งที่ตัดสินใจในการประชุม
* รวม Action Items จากหลายการประชุม
* ติดตามว่างานใดเสร็จแล้ว
* ตอบคำถามย้อนหลัง
* สรุปงานรายวันหรือรายสัปดาห์

สิ่งที่ต้องทำ:

* เพิ่ม Long-Term Memory Storage
* เพิ่ม Session Summary
* เพิ่ม Semantic Search
* แยก Memory ตามประเภท
* เชื่อม Meeting ID กับ Project
* ให้ Agent ดึงเฉพาะ Memory ที่เกี่ยวข้องก่อนตอบ
* เพิ่มระบบแก้ไขและลบ Memory

---

# Phase 6: Desktop Automation

Status: Planned

เป้าหมาย:

ให้ Jarvis ใช้งานคอมพิวเตอร์แทนผู้ใช้ได้

ความสามารถหลัก:

* เปิดและปิดโปรแกรม
* เปิดเว็บไซต์
* ค้นหาไฟล์
* ใช้คีย์บอร์ดและเมาส์
* เปิดโฟลเดอร์
* จัดการหน้าต่าง
* ทำงานซ้ำ ๆ อัตโนมัติ
* นำ Action Items จากการประชุมไปสร้างงานบนระบบอื่น

สิ่งที่ต้องทำ:

* เพิ่ม Desktop Tool Layer
* เพิ่ม Allowlist
* แยกคำสั่งอันตรายออกจากคำสั่งปกติ
* เพิ่ม Confirmation ก่อนลบไฟล์ ปิดโปรแกรม หรือส่งข้อมูล
* เพิ่ม Dry Run Mode
* เพิ่ม Audit Log

---

# Phase 7: Vision

Status: Planned

เป้าหมาย:

ให้ Jarvis มองเห็นหน้าจอและเข้าใจสิ่งที่เกิดขึ้นบนคอมพิวเตอร์

ความสามารถหลัก:

* Screenshot
* วิเคราะห์ภาพหน้าจอ
* อธิบายสิ่งที่เห็น
* ช่วยแก้ Error จากภาพ
* ใช้ Vision ร่วมกับ Desktop Automation
* อ่านเอกสารหรือ Slide ที่เกี่ยวข้องกับการประชุม

---

# Phase 8: Multi-Agent

Status: Planned

เป้าหมาย:

แยก Jarvis ออกเป็นหลาย Agent ตามหน้าที่ เมื่อระบบมีขนาดใหญ่พอ

ตัวอย่าง Agent:

* Planner Agent
* Tool Agent
* Memory Agent
* Vision Agent
* Desktop Agent
* Voice Agent
* Meeting Agent
* Summary Agent
* Remote Channel Agent

เหตุผล:

* ลดความซับซ้อนของ Agent ตัวเดียว
* แยกการทดสอบแต่ละส่วน
* จำกัดสิทธิ์ของแต่ละ Agent
* เพิ่มความเสถียรเมื่อ Module ใด Module หนึ่งมีปัญหา

หมายเหตุ:

ไม่ควรรีบทำ Multi-Agent ก่อน Core, Meeting Pipeline และ Remote Channel มี Interface ที่ชัดเจน

---

# Phase 9: Home Automation

Status: Planned

เป้าหมาย:

ให้ Jarvis เชื่อมต่อกับอุปกรณ์ภายในบ้านหรือระบบ IoT

ความสามารถหลัก:

* สั่งเปิดและปิดไฟ
* ควบคุมอุปกรณ์
* เชื่อมต่อ Smart Home API
* สั่งงานด้วยเสียงผ่าน Wake Word
* ตรวจสถานะเครื่องที่รัน Meeting Worker

---

# Meeting MVP Scope

เวอร์ชันแรกควรทำเฉพาะสิ่งจำเป็นเพื่อให้ใช้งานจริงได้เร็วที่สุด

MVP ต้องทำได้:

1. ผู้ใช้อัดเสียงประชุมด้วยโทรศัพท์
2. ผู้ใช้ส่งไฟล์ผ่าน Telegram Bot
3. Bot ตรวจสอบ User ID
4. Bot ดาวน์โหลดไฟล์
5. Jarvis แปลงไฟล์เป็นรูปแบบมาตรฐาน
6. Jarvis แบ่งไฟล์เป็น Chunk
7. Jarvis ถอดเสียงด้วย STT
8. Jarvis สร้าง Summary
9. Jarvis แยก Decisions และ Action Items
10. Bot ส่งผลกลับ
11. Jarvis เก็บ Meeting ID, Transcript และ Summary
12. ผู้ใช้เรียกดูประชุมล่าสุดได้

สิ่งที่ยังไม่จำเป็นใน MVP:

* Speaker Diarization ที่แม่นยำสูง
* Real-Time Meeting Transcription
* เชื่อม Calendar
* เชื่อม Task Manager
* Multi-Agent
* Dashboard แบบเต็มรูปแบบ
* LINE Bot พร้อมกับ Telegram ตั้งแต่วันแรก
* การควบคุม Desktop จากระยะไกล

---

# Suggested Project Structure

```text
app/
├── agent/
│   ├── intent_classifier.py
│   ├── router.py
│   └── agent.py
├── channels/
│   ├── base.py
│   ├── router.py
│   ├── telegram/
│   │   ├── bot.py
│   │   ├── handlers.py
│   │   └── formatter.py
│   └── line/
│       ├── bot.py
│       ├── handlers.py
│       └── formatter.py
├── core/
│   ├── config.py
│   ├── logger.py
│   ├── health.py
│   └── state.py
├── jobs/
│   ├── queue.py
│   ├── worker.py
│   └── meeting_job.py
├── meeting/
│   ├── audio_processor.py
│   ├── audio_chunker.py
│   ├── file_validator.py
│   ├── transcriber.py
│   ├── transcript_merger.py
│   ├── transcript_cleaner.py
│   ├── summarizer.py
│   ├── chunk_summarizer.py
│   ├── summary_merger.py
│   ├── repository.py
│   └── search.py
├── memory/
│   ├── session_memory.py
│   ├── long_term_memory.py
│   └── semantic_search.py
├── security/
│   ├── auth.py
│   ├── file_security.py
│   ├── rate_limit.py
│   └── audit.py
├── tools/
│   ├── resolver.py
│   ├── registry.py
│   └── schemas.py
└── voice/
    ├── vad.py
    ├── wake_word.py
    ├── stt.py
    ├── tts_router.py
    └── playback.py

config/
├── settings.yaml
└── prompts/

data/
├── meetings/
├── transcripts/
├── summaries/
├── jobs/
└── logs/

tests/
├── test_intent_classifier.py
├── test_meeting_pipeline.py
├── test_channel_auth.py
├── test_file_validator.py
└── test_tts_fallback.py

jarvis.py
.env
.gitignore
```

---

# Current Known Issues

## 1. Agent ตอบคำถามทั่วไปไม่ดีพอ

สาเหตุ:

* Tool Resolver ใช้ Keyword Matching กว้างเกินไป
* ยังไม่มี Intent Layer
* Memory Retrieval ยังไม่ชัดเจน

แนวทางแก้:

* ทำ Intent Classifier ก่อน Tool Parameter
* เพิ่ม Confidence Score
* เพิ่ม Test Dataset จากประโยคที่ใช้จริง
* แยก General Chat, Memory Question และ Tool Action ให้ชัดเจน

---

## 2. Thai TTS ยังไม่เป็นธรรมชาติและไม่เสถียร

สาเหตุ:

* Local Thai TTS ยังมีเสียงแบบหุ่นยนต์
* Edge TTS ต้องใช้อินเทอร์เน็ต
* ยังไม่มี Engine Fallback ที่สมบูรณ์

แนวทางแก้:

* แยก TTSRouter
* เพิ่ม Local Fallback
* เพิ่ม Timeout และ Error Recovery
* ทำ Interrupt Speech ก่อน Streaming แบบเต็มรูปแบบ

---

## 3. Wake Word ยังต้องจูน

แนวทางแก้:

* เก็บ Log จากการใช้งานจริง
* เพิ่ม Alias จากข้อมูลจริง
* วัด False Positive และ False Negative
* ทดสอบในห้องเงียบและห้องที่มีเสียงรบกวน

---

## 4. ไฟล์ประชุมอาจมีขนาดใหญ่

แนวทางแก้:

* จำกัดขนาดไฟล์
* แบ่งเสียงเป็น Chunk
* ใช้ Job Queue
* แจ้งสถานะผู้ใช้
* ลบ Temporary File
* ตรวจพื้นที่ Disk ก่อนเริ่มงาน

---

## 5. ข้อมูลประชุมอาจเป็นความลับ

แนวทางแก้:

* ใช้ User Allowlist
* เก็บข้อมูลแบบ Local
* ไม่เปิดเผย Bot ให้บุคคลทั่วไป
* เก็บ Secret ใน `.env`
* เพิ่ม Retention Policy
* เพิ่มคำสั่งลบข้อมูล
* ใช้ Audit Log

---

# Current Priority

## Stage A: Stabilize Jarvis Core

1. แก้ Agent Intent และ Tool Resolver
2. ทำ TTS Router และ Fallback
3. ทดสอบ Wake Word ให้ได้ตามเกณฑ์
4. ทำ Interrupt Speech
5. เพิ่ม Logging, State Management และ Error Recovery
6. วัด Latency และปรับความเร็ว

## Stage B: Build Meeting MVP

7. สร้าง Meeting File Processor
8. ทำ Long-Audio Transcription
9. ทำ Transcript Cleanup
10. ทำ Meeting Summarizer
11. แยก Decisions และ Action Items
12. เพิ่ม Meeting Storage
13. เพิ่ม Job Queue

## Stage C: Remote Access

14. สร้าง Channel Interface
15. ทำ Telegram Bot MVP
16. เพิ่ม Authentication และ File Security
17. ตั้ง Worker ให้รันต่อเนื่องบนเครื่อง Jarvis
18. เพิ่มคำสั่งตรวจสอบสถานะและเรียกดูการประชุม
19. ทดสอบการส่งไฟล์จากโทรศัพท์นอกเครือข่ายบ้าน
20. เพิ่ม LINE Bot Adapter หลัง Telegram ใช้งานเสถียร

## Stage D: Expansion

21. เพิ่ม Tool Parameters
22. เชื่อม Meeting Summary กับ Long-Term Memory
23. เพิ่ม Desktop Automation
24. เพิ่ม Vision
25. พิจารณา Multi-Agent
26. เพิ่ม Home Automation

---

# Recommended Next Task

งานถัดไปที่ควรทำทันที:

## Improve Agent Intent and Tool Resolver

เหตุผล:

* เป็นปัญหาหลักของ Core ในปัจจุบัน
* Meeting Module จะต้องใช้ Intent Routing เช่นกัน
* Remote Bot จะส่งทั้งข้อความ คำสั่ง และไฟล์เข้ามา
* ถ้า Router ยังไม่แม่น คำสั่งจาก Bot อาจถูกส่งไปผิด Module

หลังจาก Intent Layer ใช้งานได้ ให้ทำตามลำดับนี้:

1. TTS Stability
2. Wake Word Reliability
3. Interrupt Speech
4. Core Logging and Recovery
5. Meeting File Processor
6. Long-Audio Transcription
7. Meeting Summarizer
8. Telegram Bot Integration
