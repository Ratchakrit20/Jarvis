# Project Rules

## Coding Style

- Python 3.11
- Type Hint ทุกฟังก์ชัน
- มี Docstring ทุก Class
- ไม่มี Global Variable
- ใช้ Class เป็นหลัก
- Function ไม่เกิน 50 บรรทัด (ถ้าเป็นไปได้)

---

## Logging

ทุก Module ต้องมี Logger

ห้าม print() ยกเว้น main.py

---

## Error Handling

ห้าม

```
except:
```

ต้องระบุ Exception เสมอ

---

## Config

ห้าม Hardcode

ทุกอย่างต้องอยู่ config.py

---

## Folder

หนึ่งไฟล์ทำหน้าที่เดียว

---

## Agent

Agent ห้ามเรียกกันเอง

ทุก Agent ผ่าน Router เท่านั้น

---

## Memory

ห้ามเขียน SQLite ตรง ๆ

ทุกอย่างผ่าน Memory Manager

---

## LLM

ห้ามเรียก Ollama ตรง

ทุกอย่างผ่าน llm/

---

## Voice

Microphone

↓

STT

↓

Router

↓

LLM

↓

TTS

↓

Speaker

---

## Commit

feat:

fix:

refactor:

docs: