import os
import google.generativeai as genai

GEMINI_API_KEY = "AIzaSyCVQM4930V4nLP8h7TF2IG9QrKr7zhFHPw"

genai.configure(api_key=GEMINI_API_KEY)

# Create the model
generation_config = {
  "temperature": 0.1,
  "top_p": 0.95,
  "top_k": 30,
  "max_output_tokens": 1000,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-2.0-flash-exp",
  generation_config=generation_config,
)

chat_session = model.start_chat(
  history=[
  ]
)

response = chat_session.send_message("Làm thế nào để chuẩn bị cho môn học kiến trúc máy tính cuối kỳ?")
print(response.text)