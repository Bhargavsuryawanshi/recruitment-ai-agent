from google import genai
import os
import json
from .model import JobDescriptionInput, Candidate

# Initialize client (it picks up API key from env var or explicit)
def get_client():
    api_key = os.getenv("GOOGLE_API_KEY")
    # If you use Vertex AI rather than Gemini Developer API, you may pass vertexai=True, project, location, etc.
    return genai.Client(api_key=api_key)

async def call_gemini(prompt: str, is_json: bool = False):
    client = get_client()
    # choose model name; adjust to your target
    model_name = "gemini-2.5-flash"  # or "gemini-2.5-pro", etc.

    try:
        # Use generate_content or stream, depending on needs
        resp = client.models.generate_content(
            model=model_name,
            contents=prompt,
            # optionally configure tools etc. via config param
            # config=types.GenerateContentConfig(...)
        )

        text = resp.text

        if is_json:
            # try to parse JSON within the response
            # optionally, you can instruct Gemini to output *only* JSON
            s = text.strip()
            # strip markdown JSON fences if present
            if s.startswith("```json"):
                s = s[len("```json"):]
            if s.endswith("```"):
                s = s[:-3]
            s = s.strip()
            try:
                return json.loads(s)
            except json.JSONDecodeError:
                # fallback: return None or the raw text
                return None
        else:
            return text

    except Exception as e:
        # you can log the exception or propagate
        print("Error in call_gemini:", e)
        if is_json:
            return None
        return f"Error generating content: {e}"

async def generate_jd(jd_input: JobDescriptionInput) -> str:
    prompt = f"""
    Generate a detailed and professional job description for the following role:
    - Job Title: {jd_input.job_title}
    - Years of Experience: {jd_input.experience}
    - Must-have Skills: {jd_input.skills}
    - Company Name: {jd_input.company_name}
    - Employment Type: {jd_input.employment_type}
    - Industry: {jd_input.industry}
    - Location: {jd_input.location}

    The job description should be engaging and clearly outline the responsibilities and qualifications.
    """
    return await call_gemini(prompt)

async def evaluate_resumes(jd: str, resumes: list) -> list:
    candidates = []
    for resume in resumes:
        prompt = f"""
        You are an expert HR professional. Evaluate the following resume against the provided job description.
        Provide your evaluation **only in a raw JSON format** with the following keys: "score", "missing_skills", "remarks".
        - The "score" must be an integer out of 100.
        - "missing_skills" must be a JSON array of strings.
        - "remarks" must be a brief, one-sentence explanation.

        Job Description:
        ---
        {jd}
        ---

        Resume:
        ---
        {resume['text']}
        ---

        Output only the JSON object, with no other text or markdown formatting.
        """
        result = await call_gemini(prompt, is_json=True)
        
        if result:
            candidates.append(Candidate(
                filename=resume['filename'],
                score=result.get('score', 0),
                missing_skills=result.get('missing_skills', []),
                remarks=result.get('remarks', 'No remarks provided.')
            ))
        else:
            # Handle cases where the AI response was not valid JSON
            candidates.append(Candidate(
                filename=resume['filename'],
                score=0,
                missing_skills=["N/A"],
                remarks="Error processing AI response."
            ))
    
    # Sort candidates by score in descending order
    candidates.sort(key=lambda x: x.score, reverse=True)
    return candidates

async def generate_emails(jd: str, best_candidate: Candidate, other_candidates: list) -> dict:
    # Generate interview email
    interview_prompt = f"""
    Generate a personalized and professional interview invitation email for a top candidate.
    
    Job Description (for context):
    ---
    {jd}
    ---
    
    Candidate's Resume Filename: {best_candidate.filename}
    
    The email should be warm, professional, and express excitement about their qualifications.
    """
    interview_email = await call_gemini(interview_prompt)

    # Generate rejection emails
    rejection_emails = []
    for candidate in other_candidates:
        rejection_prompt = f"""
        Generate a polite and professional rejection email for a candidate who was not selected.
        
        Job Description (for context):
        ---
        {jd}
        ---

        Candidate's Resume Filename: {candidate.filename}

        The email should be respectful, brief, and thank them for their interest.
        """
        rejection_emails.append(await call_gemini(rejection_prompt))
        
    return {"interview_email": interview_email, "rejection_emails": rejection_emails}