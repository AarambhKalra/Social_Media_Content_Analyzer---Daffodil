import os
import re
from typing import Optional

from google import genai

# Default Gemini model for summarization (can be overridden via GEMINI_MODEL)
# Using gemini-3-flash-preview as it's a current available model
DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-3-flash-preview")


def _get_gemini_client() -> "genai.Client":
    """Configure and return a Gemini API client, or raise if unavailable."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not set")
    return genai.Client(api_key=api_key)


def analyze_social_media_content(
    text: str,
    model: str = DEFAULT_MODEL,
    max_tokens: int = 512,
) -> dict:
    """Analyze social media content and provide engagement improvement suggestions.

    - Reads `GEMINI_API_KEY` from the environment.
    - Returns a dictionary with 'analysis' and 'suggestions' keys.
    - On any configuration/network/API error, an exception is raised.
    """
    if not text:
        raise ValueError("Text content is required for analysis")

    client = _get_gemini_client()

    prompt = (
        "You are a social media marketing expert. Analyze the following social media post content.\n\n"
        "Provide your response in EXACTLY this format:\n\n"
        "ANALYSIS:\n"
        "[Provide a brief analysis covering: tone, message clarity, target audience, and overall content quality]\n\n"
        "SUGGESTIONS:\n"
        "[Provide specific, actionable suggestions to improve engagement. Include recommendations for: hashtags, call-to-action, timing, content structure, visual elements, and any other engagement strategies. Be detailed and specific.]\n\n"
        "Content to analyze:\n\n"
        f"{text}\n\n"
        "Remember: Always include both ANALYSIS and SUGGESTIONS sections. Make suggestions detailed and actionable."
    )

    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config={
            "max_output_tokens": max_tokens,
            "temperature": 0.7,
        },
    )

    result_text = getattr(response, "text", "") or ""
    result_text = result_text.strip()
    if not result_text:
        raise RuntimeError("Gemini did not return any analysis")

    # Parse the response into analysis and suggestions
    # Try multiple formats that Gemini might use
    result_lower = result_text.lower()
    
    # Look for "SUGGESTIONS:" marker (case-insensitive)
    # Find the position of "suggestions:" case-insensitively
    suggestions_match = re.search(r'suggestions:', result_text, re.IGNORECASE)
    
    if suggestions_match:
        suggestions_pos = suggestions_match.start()
        analysis_part = result_text[:suggestions_pos]
        suggestions_part = result_text[suggestions_match.end():].strip()
        
        # Remove "ANALYSIS:" prefix if present (case-insensitive)
        analysis_match = re.search(r'analysis:', analysis_part, re.IGNORECASE)
        if analysis_match:
            analysis = analysis_part[analysis_match.end():].strip()
        else:
            analysis = analysis_part.strip()
        
        suggestions = suggestions_part
    # Look for numbered list or bullet points that might indicate suggestions
    elif "2." in result_text or "•" in result_text or "-" in result_text:
        # Try to split on common patterns
        lines = result_text.split("\n")
        analysis_lines = []
        suggestion_lines = []
        found_suggestion_marker = False
        
        for line in lines:
            line_lower = line.lower().strip()
            if "suggestion" in line_lower or "improvement" in line_lower or "recommendation" in line_lower:
                found_suggestion_marker = True
            if found_suggestion_marker:
                suggestion_lines.append(line)
            else:
                analysis_lines.append(line)
        
        analysis = "\n".join(analysis_lines).replace("ANALYSIS:", "").strip()
        suggestions = "\n".join(suggestion_lines).strip()
    else:
        # If no clear structure, try to split roughly in half or use full text
        # Look for common section separators
        if "\n\n" in result_text:
            parts = result_text.split("\n\n", 1)
            analysis = parts[0].replace("ANALYSIS:", "").strip()
            suggestions = parts[1].strip() if len(parts) > 1 else ""
        else:
            analysis = result_text.replace("ANALYSIS:", "").strip()
            suggestions = ""

    # Clean up analysis (remove any remaining markers)
    analysis = re.sub(r"^analysis:\s*", "", analysis, flags=re.IGNORECASE).strip()
    
    # Ensure we have content
    if not analysis:
        analysis = result_text
    
    if not suggestions:
        # If no suggestions found, try to extract from full response
        # Look for common suggestion keywords
        suggestion_keywords = ["hashtag", "call to action", "cta", "improve", "recommend", "suggest", "try", "consider"]
        lines = result_text.split("\n")
        suggestion_lines = []
        for line in lines:
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in suggestion_keywords):
                suggestion_lines.append(line)
        if suggestion_lines:
            suggestions = "\n".join(suggestion_lines).strip()
        else:
            suggestions = ""

    return {
        "analysis": analysis,
        "suggestions": suggestions,
        "full_response": result_text
    }
