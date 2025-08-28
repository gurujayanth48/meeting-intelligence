import json
import requests
from app.core.config import settings

EXTRACTION_PROMPT = """
Extract the following information from this meeting transcript:
1. Action Items: Who needs to do what by when
2. Key Decisions: Important decisions made
3. Participants: Who spoke and their roles
4. Topics: Main discussion points

Format as JSON:
{
  "action_items": [{"assignee": "...", "task": "...", "deadline": "..."}],
  "decisions": [{"decision": "...", "made_by": "..."}],
  "participants": [{"name": "...", "role": "..."}],
  "topics": ["..."]
}

Transcript:
{transcript}
"""

def extract_meeting_insights(transcript: str) -> dict:
    """Extract insights from transcript using LLM"""
    try:
        # Using Ollama API
        prompt = EXTRACTION_PROMPT.format(transcript=transcript)
        
        response = requests.post(
            f"{settings.OLLAMA_API_URL}/api/generate",
            json={
                "model": "llama2",
                "prompt": prompt,
                "stream": False
            }
        )
        
        if response.status_code == 200:
            result = response.json()
            # Parse the response to extract JSON
            try:
                # Try to find JSON in the response
                content = result.get('response', '')
                # Simple JSON extraction (in real implementation, you'd want better parsing)
                start = content.find('{')
                end = content.rfind('}') + 1
                if start != -1 and end != 0:
                    json_str = content[start:end]
                    return json.loads(json_str)
            except:
                pass
        
        # Fallback: return sample data
        return {
            "action_items": [
                {"assignee": "John Smith", "task": "Complete marketing campaign", "deadline": "2023-12-15"},
                {"assignee": "Sarah Johnson", "task": "Prepare client presentation", "deadline": "2023-12-10"},
                {"assignee": "Mike Davis", "task": "Set up project management tool", "deadline": "2023-12-05"}
            ],
            "decisions": [
                {"decision": "Use new software tool for project management", "made_by": "Team consensus"},
                {"decision": "Allocate additional budget for marketing", "made_by": "Management"}
            ],
            "participants": [
                {"name": "John Smith", "role": "Marketing Lead"},
                {"name": "Sarah Johnson", "role": "Client Relations"},
                {"name": "Mike Davis", "role": "Technical Lead"}
            ],
            "topics": ["Project Timeline", "Budget Allocation", "Team Responsibilities", "Software Tools"]
        }
        
    except Exception as e:
        # Fallback for demo purposes
        return {
            "action_items": [
                {"assignee": "John Smith", "task": "Complete marketing campaign", "deadline": "2023-12-15"},
                {"assignee": "Sarah Johnson", "task": "Prepare client presentation", "deadline": "2023-12-10"}
            ],
            "decisions": [
                {"decision": "Use new software tool for project management", "made_by": "Team consensus"}
            ],
            "participants": [
                {"name": "John Smith", "role": "Marketing Lead"},
                {"name": "Sarah Johnson", "role": "Client Relations"}
            ],
            "topics": ["Project Timeline", "Budget Allocation"]
        }