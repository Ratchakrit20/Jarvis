from __future__ import annotations

import ollama

from app.config import OLLAMA_HOST, LLM_MODEL


SYSTEM_PROMPT = """
คุณคือ Jarvis ผู้ช่วยส่วนตัวของผู้ใช้

กฎสำคัญ:
- ตอบเป็นภาษาไทยเท่านั้น
- ห้ามใช้ภาษาจีน อังกฤษ หรือภาษาอื่นปน
- ตอบสั้น ชัดเจน ไม่อธิบายยาว
- ใช้สรรพนาม "ผม" เท่านั้น
- ห้ามใช้ "ค่ะ"
- ห้ามพูดหลายภาษาในประโยคเดียว
- ห้ามพูดว่าตัวเองเป็น AI หรือ model

เป้าหมาย:
- ช่วยงานผู้ใช้ให้เร็วและชัดที่สุด
"""


class OllamaLLM:
    def __init__(
        self,
        model: str = LLM_MODEL,
    ):
        self.model = model

        # สร้าง client ต่อ instance (ปลอดภัยกว่า class variable)
        self.client = ollama.Client(host=OLLAMA_HOST)

    def chat(self, text: str) -> str:
        try:
            response = self.client.chat(
                model=self.model,
                options={
                    "temperature": 0.2
                },   
                messages=[
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT,
                    },
                    {
                        "role": "user",
                        "content": text,
                    },
                ],
            )

            return response["message"]["content"].strip()

        except Exception as e:
            return f"[Ollama Error] {str(e)}"