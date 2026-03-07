from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
model = init_chat_model("gemini-2.5-flash",
                        model_provider="google-genai",
                        temperature=0.9)
response = model.invoke(
      [HumanMessage(content="Write a short story about Moon")])
print(response.content)
