# Create key using https://aistudio.google.com/apikey
# Set environment variable GOOGLE_API_KEY to Gemini API key

from google import genai

client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="What is the capital of India. Just give name only"
)

print(response.text)
