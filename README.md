#  Recruitment AI Agent

An intelligent web application built with FastAPI and Google Gemini to automate and streamline the initial stages of the recruitment process. This tool helps HR professionals by automatically generating job descriptions, scoring resumes against them, and drafting communication emails.

### live Demo
**[Link to your live application hosted on Render]**

---

## ✅ Core Features

*   **Dynamic Job Description (JD) Module**:
    *   **Upload**: Extract JD text from `PDF` or `DOCX` files.
    *   **Manual Input**: Paste a JD directly into a textarea.
    *   **AI Generation**: Create a new JD from scratch by providing key details (title, skills, experience, etc.).
*   **Bulk Resume Uploader**:
    *   Upload up to 10 resumes (`PDF` or `DOCX`) at once.
*   **AI-Powered Candidate Matching**:
    *   **Scoring**: Each resume is assigned a relevance score out of 100 based on the JD.
    *   **Skill Analysis**: Identifies key skills from the JD that are missing in the resume.
    *   **Concise Remarks**: Provides a brief, human-like summary of the candidate's fit.
*   **Automated Email Generation**:
    *   **Interview Invitation**: Auto-generates a personalized email for the top-matched candidate.
    *   **Rejection Email**: Auto-generates polite rejection emails for other candidates.
*   **Simple & Clean Frontend**:
    *   A straightforward user interface built with HTML and Jinja2 templates.
    *   Visually highlights the best-matched candidate for quick identification.

---

## 🛠️ Tech Stack

*   **Backend**: FastAPI
*   **AI/LLM**: Google Gemini 2.5 Flash
*   **Frontend**: Jinja2, HTML, CSS
*   **Server**: Uvicorn
*   **Deployment**: Render

---

## 🚀 Setup Instructions

Follow these steps to get the project running on your local machine.

#### 1. Clone the Repository
```bash
git clone https://github.com/Bhargavsuryawanshi/recruitment-ai-agent.git
cd recruitment-ai-agent
```

#### 2. Create and Activate a Virtual Environment
*   **On macOS/Linux:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
*   **On Windows:**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```

#### 3. Install Dependencies
All required packages are listed in `requirements.txt`.
```bash
pip install -r requirements.txt
```

#### 4. Set Up Environment Variables
Create a file named `.env` in the root directory of the project. This file will hold your secret API key.

Add the following line to your `.env` file:
```
GOOGLE_API_KEY='your-google-api-key-here'
```
---

## 🏃 How to Run the Project Locally

#### 1. Start the FastAPI Server
With your virtual environment activated, run the following command in your terminal:
```bash
uvicorn app.main:app --reload
```
The `--reload` flag automatically restarts the server whenever you make changes to the code.

#### 2. Access the Application
Open your web browser and navigate to:
**`http://127.0.0.1:8000`**

#### 3. View the API Documentation
FastAPI automatically generates interactive API documentation. You can access it at:
**`http://127.0.0.1:8000/docs`**

---

## 🤖 Description of the AI Logic

This application's intelligence is driven by the **Google Gemini 2.5 Flash** model. The interaction with the AI is managed through carefully crafted prompts sent from the FastAPI backend.

1.  **Job Description Generation**: When the user opts to generate a JD, the backend collects the form inputs (job title, skills, etc.) and embeds them into a prompt that instructs Gemini to act as a senior recruiter and write a comprehensive job description.

2.  **Resume Evaluation**: This is the core AI task. For each resume, a detailed prompt is sent to the Gemini API. This prompt includes:
    *   The full text of the job description.
    *   The full text extracted from one candidate's resume.
    *   A strict instruction to return its analysis **only in a JSON format**. This JSON object must contain three specific keys: `score` (an integer), `missing_skills` (a list of strings), and `remarks` (a short string). This structured output is crucial for reliably parsing the data and displaying it on the frontend.

3.  **Email Generation**: After identifying the best-matched candidate, two types of prompts are sent:
    *   One prompt asks Gemini to write a warm, personalized interview invitation for the top candidate.
    *   Another prompt is used in a loop for the other candidates to generate a polite and respectful rejection email.

---

## 🧠 Explanation of Model Choice: Gemini 2.5 Flash

For this project, I chose **Google's Gemini 2.5 Flash** model. This decision was based on a balance of performance, speed, and cost-efficiency, which are critical for a real-world web application.

*   **Speed and Low Latency**: "Flash" is specifically optimized for speed, making it ideal for interactive applications where users expect a fast response. When a user uploads resumes, they get the analysis back in seconds, not minutes.

*   **Cost-Effectiveness**: As a lightweight model, Gemini 2.5 Flash is significantly more affordable to run than larger models like Gemini 2.5 Pro or GPT-5. This makes it a practical choice for a tool that might process hundreds of resumes a day.

*   **Large Context Window**: Despite its speed, Gemini 2.5 Flash has a massive 1-million-token context window. This is a huge advantage for this specific task, as it can easily handle very long and detailed job descriptions and resumes without any risk of losing context or truncating information.

*   **Excellent Instruction Following**: The model has proven to be highly reliable at following specific instructions, such as returning its output in a clean, raw JSON format. This is vital for the stability of the application, as it prevents errors that could arise from parsing unstructured text.

In summary, Gemini 2.5 Flash provides the perfect blend of capabilities for this recruitment agent. It delivers the high-quality analysis needed for the task while ensuring the application remains fast, responsive, and economical to operate.

---
