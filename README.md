# AI-Powered Test Case Generator MVP

This is an incredibly lightweight validation prototype designed to run completely locally, synchronously passing User Stories through an LLM using LangChain, enforcing the "5-Lens" output schema with Pydantic, and rendering the results in a pure Next.js table.

## Prerequisites

- Node.js (for Next.js frontend)
- Python 3.10+ (for FastAPI backend)
- An active OpenAI API Key

## Setup Backend

1. Navigate to the backend directory:
   `cd backend`
2. Create and activate a virtual environment (optional but recommended):
   `python -m venv venv`
   `venv\Scripts\activate` (on Windows) or `source venv/bin/activate` (Mac/Linux)
3. Install dependencies:
   `pip install -r requirements.txt`
4. Set your OpenAI API Key:
   Create a `.env` file in the `backend` folder and add:
   `OPENAI_API_KEY=sk-your-key-here`
5. Start the backend:
   `uvicorn main:app --reload`
6. Swagger docs are available at `http://127.0.0.1:8000/docs`.

## Setup Frontend

1. Navigate to the frontend directory:
   `cd frontend`
2. Install dependencies:
   `npm install`
3. Start the Next.js development server:
   `npm run dev`
4. Visit `http://localhost:3000` to interact with the UI.

## Testing the Application

1. Open `http://localhost:3000` in your browser.
2. Paste a User Story into the textarea.
3. Click "Generate Test Cases" and wait a few seconds while LangChain processes the 5-Lens prompt.
4. The generated structured test cases will populate the grid.
