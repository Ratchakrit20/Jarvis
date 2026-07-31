# Jarvis AI Development Log

Last Updated: 2026-07-05

---

# Current Phase

## Phase 1 : Local Voice Assistant MVP

เป้าหมายของเฟสนี้คือ

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

ให้สามารถทำงานได้ครบแบบ Local

---

# Current Status

## GPU

✅ CUDA ใช้งานได้

- RTX 3060 Laptop
- Torch CUDA

---

## LLM

✅ Ollama

Model

- qwen3:8b
- qwen2.5:7b

ทำงานผ่าน

app/llm/ollama.py

สามารถสนทนาได้แล้ว

---

## Agent

ไฟล์

app/agents/jarvis_agent.py

สถานะ

✅ ใช้งานได้

ทำได้

- สนทนา
- ใช้ Memory
- เรียก Tool
- Tool Fallback
- JSON Tool Calling

---

## Memory

สถานะ

✅ Basic Memory

สามารถ

- จำข้อความผู้ใช้
- จำข้อความ Assistant
- ส่ง Context ให้ LLM

ยังไม่มี

- Long Term Memory
- Semantic Search

---

## Tool Calling

สถานะ

✅ ใช้งานได้

โครงสร้าง

app/tools/

สามารถ

- เปิด YouTube
- เวลา
- วันที่

รองรับ

- ภาษาไทย
- ภาษาอังกฤษ
- คำสะกดผิดบางส่วน
- Alias Matching

ยังไม่มี

- Dynamic Tool Discovery
- Tool Parameter
- Multi-step Tool Calling

---

## STT

ไฟล์

app/voice/stt.py

Model

biodatlab/whisper-th-small-combined

สถานะ

✅ ใช้งานได้

รองรับ

- ภาษาไทย
- ภาษาอังกฤษ

ใช้ GPU

---

## TTS

สถานะ

⚠ กำลังพัฒนา

ปัจจุบัน

Thai

facebook/mms-tts-tha

English

Edge TTS

ปัญหา

- เสียงไทยยังเป็น Robot
- ยังไม่มี Streaming
- ยังไม่มี Voice Personality

---

## Voice Pipeline

สถานะ

✅ ใช้งานได้

Mic

↓

Whisper

↓

Jarvis Agent

↓

TTS

↓

Speaker

สามารถพูดคุยกับ Jarvis ได้แล้ว

---

# Project Progress

Core

██████████░░░░░░░░ 50%

Voice

████████░░░░░░░░░░ 40%

Agent

███████████░░░░░░░ 60%

Tools

███████░░░░░░░░░░░ 35%

Overall

ประมาณ 45%

---

# Completed Today

✓ Ollama เชื่อมต่อสำเร็จ

✓ แก้ปัญหา Client

✓ แก้ Import ทั้งโปรเจกต์

✓ สร้าง Jarvis Agent

✓ Memory

✓ Tool Calling

✓ Tool Resolver

✓ Alias ภาษาไทย

✓ Alias ภาษาอังกฤษ

✓ Voice Pipeline

✓ Whisper STT

✓ MMS TTS

✓ Edge TTS

✓ Auto Language Detection

✓ เปิด YouTube ด้วยเสียง

---

# Current Folder Structure

app/

agents/

core/

llm/

memory/

tools/

voice/

tests/

---

# Next Priority

## Priority 1 (สำคัญที่สุด)

Wake Word

ตัวอย่าง

"Jarvis"

↓

เริ่มฟัง

ไม่ต้องกด Enter

---

## Priority 2

Voice Activity Detection

พูด

↓

หยุดพูด

↓

ส่งเข้า Whisper

อัตโนมัติ

ไม่กำหนดเวลา 5 วินาที

---

## Priority 3

Streaming TTS

Jarvis พูดทันที

ไม่ต้องรอสร้างไฟล์เสียง

---

## Priority 4

Voice Personality

เสียง

- สุภาพ
- นุ่ม
- เหมือนผู้ช่วย

---

## Priority 5

Interrupt Speech

ผู้ใช้พูดแทรก

Jarvis หยุดพูดทันที

---

## Priority 6

Smart Tool Calling

เช่น

"เปิดเพลง"

↓

เปิด Spotify

หรือ

YouTube

ตาม Context

---

## Priority 7

Desktop Automation

เปิดโปรแกรม

ปิดโปรแกรม

ค้นหาไฟล์

เปิดเว็บไซต์

กดเมาส์

กดคีย์บอร์ด

---

## Priority 8

Vision

Screenshot

↓

LLM

↓

ตอบ

---

## Priority 9

Long Term Memory

จำได้หลายวัน

จำผู้ใช้

จำงาน

จำสถานะโปรเจกต์

---

## Priority 10

Plugin System

สามารถเพิ่ม Tool ใหม่

โดยไม่แก้ Agent

---

# Long Term Goal

Jarvis สามารถ

✓ สนทนาด้วยเสียง

✓ จำผู้ใช้

✓ ใช้งานคอมพิวเตอร์แทนผู้ใช้

✓ เปิดโปรแกรม

✓ ทำ Automation

✓ วิเคราะห์ภาพ

✓ เข้าเว็บไซต์

✓ ควบคุม Browser

✓ ใช้หลาย LLM

✓ รองรับ Plugin

✓ ทำงานแบบ Agent จริง

---

# Architecture Target

Microphone

↓

Wake Word

↓

Voice Activity Detection

↓

Speech To Text

↓

Memory

↓

Planner

↓

Agent

↓

Tool Calling

↓

LLM

↓

Text To Speech

↓

Speaker

---

# Notes

เป้าหมายของโปรเจกต์นี้

ไม่ใช่ ChatBot

แต่เป็น

"Personal AI Operating System"

ทุก Module ต้องสามารถเปลี่ยนได้

ทุกส่วนต้อง Modular

ไม่ผูกกับ Model ใด Model หนึ่ง

รองรับการอัปเกรดในอนาคต