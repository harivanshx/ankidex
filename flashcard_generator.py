"""
AI-Powered Flashcard Generation Module
Uses Google Gemini to generate Q&A flashcards from text
"""

import json
import os
import google.generativeai as genai


def configure_gemini(api_key: str = None):
    """
    Configure the Gemini API with the provided key.
    
    Args:
        api_key: Gemini API key (or uses GEMINI_API_KEY env var)
    """
    key = api_key or os.getenv("GEMINI_API_KEY")
    if not key:
        raise ValueError("Gemini API key is required. Set GEMINI_API_KEY environment variable or pass api_key parameter.")
    genai.configure(api_key=key)


def generate_flashcards(text: str, num_cards: int = 10, api_key: str = None) -> list:
    """
    Generate flashcards from text using Gemini AI.
    
    Args:
        text: Source text to generate flashcards from
        num_cards: Number of flashcards to generate
        api_key: Optional Gemini API key
        
    Returns:
        List of dictionaries with 'question' and 'answer' keys
    """
    configure_gemini(api_key)
    
    model = genai.GenerativeModel('gemini-pro')
    
    prompt = f"""You are an expert educator creating flashcards for students.

Analyze the following text and create {num_cards} high-quality flashcards for studying.

Rules:
1. Each flashcard should have a clear, specific question
2. Answers should be concise but complete
3. Focus on key concepts, definitions, and important facts
4. Questions should test understanding, not just recall
5. Avoid yes/no questions

Return your response as a valid JSON array with this exact format:
[
  {{"question": "What is...?", "answer": "The answer is..."}},
  {{"question": "How does...?", "answer": "It works by..."}}
]

Text to analyze:
{text}

Return ONLY the JSON array, no other text."""

    try:
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Clean up response if it has markdown code blocks
        if response_text.startswith("```"):
            lines = response_text.split("\n")
            response_text = "\n".join(lines[1:-1])
        
        flashcards = json.loads(response_text)
        
        # Validate structure
        validated_cards = []
        for card in flashcards:
            if isinstance(card, dict) and "question" in card and "answer" in card:
                validated_cards.append({
                    "question": str(card["question"]),
                    "answer": str(card["answer"])
                })
        
        return validated_cards
        
    except json.JSONDecodeError as e:
        raise Exception(f"Failed to parse AI response as JSON: {str(e)}")
    except Exception as e:
        raise Exception(f"Failed to generate flashcards: {str(e)}")
