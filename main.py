from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import google.generativeai as genai
import os

app = FastAPI()

# Setup templates folder for HTML rendering
templates = Jinja2Templates(directory="templates")

# Configure Google Gemini API Key
# (Neenga ungaloda actual Gemini API key-ah inga podalam illa environment variable-ah set panalam)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "response": None})

@app.post("/", response_class=HTMLResponse)
async def generate_answer(request: Request, prompt: str = Form(...)):
    try:
        # Using Gemini model to generate content
        model = genai.GenerativeModel('gemini-1.5-flash')
        gemini_response = model.generate_content(f"Explain this clearly for a student: {prompt}")
        result_text = gemini_response.text
    except Exception as e:
        result_text = f"An error occurred: {e}"

    return templates.TemplateResponse("index.html", {"request": request, "response": result_text, "user_prompt": prompt})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
