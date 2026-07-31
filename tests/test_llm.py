from app.llm.ollama import OllamaLLM

llm = OllamaLLM()

while True:

    text = input("> ")

    if text == "exit":
        break

    print()

    print(llm.chat(text))

    print()