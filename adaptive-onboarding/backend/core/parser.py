import os
import json
import logging
from groq import AsyncGroq
from api.schemas import ExtractedSkill

from dotenv import load_dotenv

logger = logging.getLogger(__name__)

load_dotenv()

# Re-use client
client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY", "your_key"))
MODEL = os.getenv("LLM_MODEL", "llama-3.1-8b-instant")

async def parse_resume(text: str) -> list[ExtractedSkill]:
    prompt = f"""
    You are an expert technical recruiter AI. Extract all technical and operational skills from the following resume text.
    Return ONLY a valid JSON array of objects. Do not include markdown formatting or reasoning.
    
    Each object must have exactly: 
    - "name": string.
    - "years": integer (if discernible) or null.
    - "context": string (brief summary of how it was used) or null.
    - "confidence": integer 0-100 following this exact logic:
        90-100: 3+ mentions with clear project examples.
        70-89: 2+ mentions.
        40-69: 1 mention with context.
        10-39: Bare mention, no context.
    
    Text: {text}
    """
    
    try:
        completion = await client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1
        )
        content = completion.choices[0].message.content
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].strip()
            
        data = json.loads(content)
        return [ExtractedSkill(**item) for item in data]
    except Exception as e:
        logger.error(f"Failed to parse resume: {e}")
        return []

async def parse_jd(text: str) -> list[str]:
    prompt = f"""
    You are an expert technical recruiter AI. Extract all required skills and qualifications from the following Job Description.
    Return ONLY a valid JSON array of strings. Do not include markdown formatting or reasoning.
    
    Text: {text}
    """
    
    try:
        completion = await client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1
        )
        content = completion.choices[0].message.content
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].strip()
            
        data = json.loads(content)
        return [str(s) for s in data]
    except Exception as e:
        logger.error(f"Failed to parse JD: {e}")
        return []
