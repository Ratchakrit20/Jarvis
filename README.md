# 🤖 JarvisAI

JarvisAI คือผู้ช่วย AI ส่วนตัว (Personal AI Assistant) ที่ได้รับแรงบันดาลใจจาก Jarvis ใน Iron Man

เป้าหมายของโปรเจกต์นี้คือสร้าง AI Assistant ที่สามารถสนทนาด้วยเสียงภาษาไทย ทำงานบนเครื่องของผู้ใช้ (Local First) และสามารถขยายความสามารถผ่านระบบ Agent ได้

---

# เป้าหมายของโปรเจกต์

JarvisAI จะสามารถ

- 🎤 สนทนาด้วยเสียงภาษาไทย
- 🧠 จดจำข้อมูลผู้ใช้ (Memory)
- 💬 สนทนาผ่าน LLM
- 🔧 เรียกใช้ Agent ต่าง ๆ
- 🌐 ค้นหาข้อมูลบนอินเทอร์เน็ต
- 📈 วิเคราะห์หุ้น
- 📅 จัดการตารางงาน
- 📂 เปิดโปรแกรมใน Windows
- 📧 ส่ง Email
- 👁 วิเคราะห์ภาพจากกล้อง
- 🖥 ควบคุมคอมพิวเตอร์
- 🔌 รองรับ Plugin และ MCP Server

## คำสั่ง Web ที่ใช้งานได้

```text
จาร์วิส เปิดเพลง Numb Linkin Park
จาร์วิส เปิด Facebook
จาร์วิส เปิดไอจี
จาร์วิส ค้นหาในกูเกิลเรื่อง AI Agent
```

การเล่นเพลงจะเปิดผลลัพธ์แรกจาก YouTube โดยตรง หากค้นหาไม่ได้จะเปิดหน้าผลการค้นหาแทน

---

# Architecture

```
Microphone
      │
      ▼
 Voice Activity Detection
      │
      ▼
Speech To Text
      │
      ▼
 Intent Router
      │
 ┌────┴─────────────┐
 │                  │
 ▼                  ▼
Agent          General Chat
 │                  │
 └──────┬───────────┘
        ▼
      Memory
        ▼
       LLM
        ▼
 Text To Speech
        ▼
     Speaker
```

---

# Technology Stack

| Component | Technology |
|------------|------------|
| Programming | Python 3.11 |
| LLM | Ollama (Qwen3 8B) |
| STT | Whisper (Thai) |
| TTS | MMS Thai (เปลี่ยนเป็น Kokoro ภายหลัง) |
| Voice Detection | Silero VAD |
| Embedding | Nomic Embed |
| Memory | SQLite |
| Agent | Python |
| Vision | Florence2 / Qwen-VL (Future) |

---

# Project Structure

```
JarvisAI/

agents/
config/
core/
llm/
memory/
plugins/
tools/
voice/

jarvis.py

README.md
DEVELOPMENT.md
requirements.txt
```

---

# Features Roadmap

## Phase 1

- [ ] Voice Assistant
- [ ] Wake Word
- [ ] STT
- [ ] TTS
- [ ] Ollama

---

## Phase 2

- [ ] Memory
- [ ] Agent Router
- [ ] Stock Agent
- [ ] Weather
- [ ] News
- [ ] Windows Control

---

## Phase 3

- [ ] Vision
- [ ] Browser Agent
- [ ] Coding Agent
- [ ] MCP Client
- [ ] Plugin System

---

# Requirements

- Windows 11
- Python 3.11
- RTX3060 6GB+
- Ollama
- CUDA

## Installation and recovery

For a fresh clone, model download, dependency installation, and troubleshooting,
see [SETUP.md](SETUP.md).

---

# Current Model

LLM

```
qwen3:8b
```

Speech Recognition

```
Whisper Thai
```

Speech Synthesis

```
MMS Thai
```

---

# License

MIT
