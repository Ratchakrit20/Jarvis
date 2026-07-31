# tests/test_agent.py

from app.agents.jarvis_agent import JarvisAgent

agent = JarvisAgent()

while True:
    text = input("> ")
    print(agent.chat(text))