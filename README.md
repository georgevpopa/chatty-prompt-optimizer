🚀 Chatty - Universal Prompt Optimizer
Takes messy, unstructured user input and compiles it into perfect, model-specific AI prompts using a Hybrid Architecture (LLM Extraction + Rule Engine Compilation).

Chatty Interface

🧠 How It Works
Instead of just asking an AI to rewrite a prompt (which is slow, expensive, and non-deterministic), Chatty uses a Hybrid Architecture:

Intent Extraction (Lightweight LLM): A fast, cheap model (llama-3.1-8b-instant via Groq) parses the user's raw input and extracts structured JSON data (Task, Context, Constraints, Persona, Format).
Rule Engine Compilation (Deterministic): A Python rule engine takes that JSON and compiles it into a perfectly structured prompt, applying model-specific heuristics (e.g., XML tags for Anthropic Claude, Markdown headers for OpenAI GPT).
Intent Anchoring: The original user request is appended to the final prompt to prevent "intent drift" caused by the LLM rewriting the core meaning.
✨ Features
Web Interface: Clean, dark-themed UI to generate and copy prompts instantly.
API Endpoint: FastAPI backend for programmatic access.
Model Optimization: Dynamically format prompts for OpenAI or Anthropic architectures.
Cost Efficient: Uses Groq's free tier for the parsing step, meaning zero API costs for basic usage.
Fault Tolerant: Built-in sanitization handles LLM JSON hallucinations gracefully.
📋 Prerequisites
Python 3.8 or higher
A Groq API Key (Free tier available)
🛠️ Installation & Setup
Clone the repository:
git clone https://github.com/georgevpopa/chatty-prompt-optimizer.gitcd chatty-prompt-optimizer
Create and activate a virtual environment:
Windows (PowerShell):
powershell

python -m venv venv
.\venv\Scripts\Activate.ps1
macOS / Linux:
bash

python -m venv venv
source venv/bin/activate
Install dependencies:
bash

pip install -r requirements.txt
Set your API Key:
Windows (PowerShell):
powershell

$env:GROQ_API_KEY="gsk_your_key_here"
macOS / Linux:
bash

export GROQ_API_KEY="gsk_your_key_here"
🚀 Running the App
Start the FastAPI server:

bash

uvicorn main:app --reload
Web Interface: Open your browser and go to http://127.0.0.1:8000
API Docs (Swagger): Go to http://127.0.0.1:8000/docs
💻 Usage
Via Web UI
Enter your messy, unstructured prompt in the left text area (e.g., "I need a blog post about python dicts, make it sound like a pirate, dont use complex words...").
Select your Target AI Model (OpenAI or Anthropic).
Click ⚡ Generate Perfect Prompt.
Copy the optimized prompt from the right panel!
Via API (cURL / PowerShell)
Send a POST request to /optimize:

powershell

# PowerShell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/optimize" -Method Post -ContentType "application/json" -Body '{"raw_input": "write a python script for sorting, must be fast", "target_model": "openai"}'
Expected JSON Response:

json

{
  "optimized_prompt": "**Role:** expert\n\n**Instruction:** write the following: a python script for sorting\n\n## Context\nNot specified\n\n## Constraints\n- must be fast\n\n**Output Format:** code\n\n**Original User Request (Anchor):** a python script for sorting"
}
☁️ Deployment
This app is ready to deploy on platforms like Render, Railway, or Fly.io.

Push your code to GitHub.
Connect the repository to your deployment platform.
Set the Start Command to:
bash

uvicorn main:app --host 0.0.0.0 --port $PORT
Add your environment variable in the platform's dashboard:
Key: GROQ_API_KEY
Value: your_groq_key
📁 Project Structure
text

.
├── main.py           # FastAPI app, endpoints, and HTML server
├── optimizer.py      # Core logic: LLM extraction & Rule engine compilation
├── index.html        # Web UI (Served by FastAPI)
├── requirements.txt  # Python dependencies
├── .gitignore        # Ignores venv and cache files
└── README.md         # You are here!
📜 License
This project is open source and available under the MIT License.