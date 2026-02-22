# Set environment variable GOOGLE_API_KEY to Google key.

from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage, SystemMessage

model = init_chat_model("gemini-2.5-flash", model_provider="google_genai")

system_message = SystemMessage(content="Give one line answer")

while True:
    prompt = input("Enter prompt [q to quit] :")
    if prompt.lower() == 'q':
        break
    response = model.invoke([system_message, HumanMessage(content=prompt)])
    print(response.content)
